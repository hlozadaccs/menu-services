from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import Flask, jsonify, request
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from config import Config
from infrastructure.db import db
from interfaces.graphql.schema import schema


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/graphql", methods=["GET"])
    def graphql_playground():
        return ExplorerGraphiQL().html(None), 200

    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value={"request": request, "session": db.session},
            debug=True,
        )
        return jsonify(result), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
