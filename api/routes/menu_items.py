from flask import Blueprint, g, request

from infrastructure.db.models import MenuItem

bp = Blueprint("auth", __name__, url_prefix="/api/v1/menu")


@bp.route("/", methods=["GET"])
def list_menu_items():
    db = g.get("db")
    items = db.query(MenuItem).all()
    return [item.id for item in items]
