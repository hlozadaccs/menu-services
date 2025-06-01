import enum

import sqlalchemy

from infrastructure.db import db


class MenuCategory(enum.Enum):
    APPETIZER = "APPETIZER"
    MAIN_COURSE = "MAIN_COURSE"
    DESSERT = "DESSERT"
    SOFT_DRINK = "SOFT_DRINK"
    JUICE = "JUICE"
    ALCOHOLIC_BEVERAGE = "ALCOHOL"
    OTHER = "OTHER"


class MenuItem(db.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)
    category = sqlalchemy.Column(
        sqlalchemy.Enum(MenuCategory), default=MenuCategory.OTHER, nullable=False
    )
    price = sqlalchemy.Column(sqlalchemy.Numeric(10, 2))
    available = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
