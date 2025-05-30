from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:password@127.0.0.1:5432/db"

engine = create_engine(DATABASE_URL)

SessionLocal = scoped_session(sessionmaker(bind=engine))


def init_db(app):
    @app.before_request
    def before_request():
        g.db = SessionLocal()

    @app.teardown_request
    def teardown_request(exception=None):
        db = g.pop("db", None)
        if db is not None:
            if exception:
                db.rollback()
            else:
                db.commit()

            db.close()
