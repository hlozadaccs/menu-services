from flask import Flask

from api.routes.menu_items import bp as bp_menu_items
from config import init_db

app = Flask(__name__)
app.register_blueprint(bp_menu_items)
init_db(app)
