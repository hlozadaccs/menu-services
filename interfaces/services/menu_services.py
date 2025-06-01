from datetime import datetime

import grpc

from infrastructure.db import db
from infrastructure.db.models import MenuCategory, MenuItem
from interfaces.grpc.generated import menu_pb2, menu_pb2_grpc
from main import app


class MenuService(menu_pb2_grpc.MenuServiceServicer):
    CATEGORY_MAPPING = {
        menu_pb2.MenuCategory.APPETIZER: MenuCategory.APPETIZER,
        menu_pb2.MenuCategory.MAIN_COURSE: MenuCategory.MAIN_COURSE,
        menu_pb2.MenuCategory.DESSERT: MenuCategory.DESSERT,
        menu_pb2.MenuCategory.SOFT_DRINK: MenuCategory.SOFT_DRINK,
        menu_pb2.MenuCategory.JUICE: MenuCategory.JUICE,
        menu_pb2.MenuCategory.ALCOHOLIC_BEVERAGE: MenuCategory.ALCOHOLIC_BEVERAGE,
        menu_pb2.MenuCategory.OTHER: MenuCategory.OTHER,
    }

    REVERSE_MAPPING = {v: k for k, v in CATEGORY_MAPPING.items()}

    def CreateMenuItem(self, request, context):
        with app.app_context():
            try:
                db_category = self.CATEGORY_MAPPING.get(request.category)
                if not db_category:
                    context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        f"Categoría inválida: {request.category}",
                    )

                new_item = MenuItem(
                    name=request.name,
                    category=db_category,
                    price=request.price,
                    available=request.available,
                    description=request.description,
                )
                db.session.add(new_item)
                db.session.commit()

                return menu_pb2.MenuItemResponse(item=self._item_to_proto(new_item))

            except Exception as e:
                context.abort(
                    grpc.StatusCode.INTERNAL, f"Error al crear ítem: {str(e)}"
                )

    def GetMenuItem(self, request, context):
        with app.app_context():
            item = MenuItem.query.filter(
                MenuItem.id == request.id, MenuItem.is_deleted.is_(False)
            ).first()
            if not item:
                context.abort(grpc.StatusCode.NOT_FOUND, "Menu item not found")
            return menu_pb2.MenuItemResponse(item=self._item_to_proto(item))

    def ListMenuItems(self, request, context):
        with app.app_context():
            query = MenuItem.query.filter(MenuItem.is_deleted.is_(False))

            # Filtro por categoría
            if request.HasField("category"):
                db_category = self.CATEGORY_MAPPING.get(request.category)
                if db_category:
                    query = query.filter(MenuItem.category == db_category)

            # Filtro por rango de precios
            if request.HasField("min_price"):
                query = query.filter(MenuItem.price >= request.min_price)
            if request.HasField("max_price"):
                query = query.filter(MenuItem.price <= request.max_price)

            # Filtro por disponibilidad
            if request.HasField("available"):
                query = query.filter(MenuItem.available == request.available)

            # Búsqueda en nombre/descripción (case-insensitive)
            if request.HasField("search_query"):
                search = f"%{request.search_query}%"
                query = query.filter(
                    db.or_(
                        MenuItem.name.ilike(search), MenuItem.description.ilike(search)
                    )
                )

            items = query.all()

            return menu_pb2.ListMenuItemsResponse(
                items=[self._item_to_proto(item) for item in items]
            )

    def UpdateMenuItem(self, request, context):
        with app.app_context():
            item = MenuItem.query.filter(
                MenuItem.id == request.id, MenuItem.is_deleted.is_(False)
            ).first()
            if not item:
                context.abort(grpc.StatusCode.NOT_FOUND, "Menu item not found")

            if request.HasField("name"):
                item.name = request.name
            if request.HasField("category"):
                item.category = request.category
            if request.HasField("price"):
                item.price = request.price
            if request.HasField("available"):
                item.available = request.available
            if request.HasField("description"):
                item.description = request.description

            db.session.commit()
            return menu_pb2.MenuItemResponse(item=self._item_to_proto(item))

    def DeleteMenuItem(self, request, context):
        with app.app_context():
            item = MenuItem.query.get(request.id)
            if not item:
                return menu_pb2.DeleteMenuItemResponse(
                    success=False, message="Item Not found"
                )

            if not request.permanent:
                item.is_deleted = True
                item.deleted_at = datetime.utcnow()
                db.session.commit()
                return menu_pb2.DeleteMenuItemResponse(
                    success=True,
                    message="Item marcado como eliminado",
                    is_soft_deleted=True,
                )

            db.session.delete(item)
            db.session.commit()
            return menu_pb2.DeleteMenuItemResponse(
                success=True, message="Deleted successfully", is_soft_deleted=False
            )

    def _item_to_proto(self, item):
        return menu_pb2.MenuItem(
            id=item.id,
            name=item.name,
            category=self.REVERSE_MAPPING[item.category],
            price=item.price,
            available=item.available,
            description=item.description,
        )

    def RestoreMenuItem(self, request, context):
        with app.app_context():
            item = MenuItem.query.get(request.id)
            if not item:
                context.abort(grpc.StatusCode.NOT_FOUND, "Item no encontrado")

            if not item.is_deleted:
                context.abort(
                    grpc.StatusCode.FAILED_PRECONDITION, "El item no está eliminado"
                )

            item.is_deleted = False
            item.deleted_at = None
            db.session.commit()

            return menu_pb2.MenuItemResponse(item=self._item_to_proto(item))
