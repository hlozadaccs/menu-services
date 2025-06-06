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

    is_deleted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    deleted_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)

    def __init__(
        self,
        name: str,
        description: str,
        category: MenuCategory,
        price: float,
        available: bool = True,
    ):
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.available = available

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "price": self.price,
            "available": self.available,
        }
