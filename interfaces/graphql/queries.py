from ariadne import QueryType
from graphql import GraphQLResolveInfo
from sqlalchemy.orm import Session

from infrastructure.db.models import MenuItem

query = QueryType()


@query.field("menuItems")
def resolve_menu_items(
    _: object,
    info: GraphQLResolveInfo,
    nameContains: str | None = None,
    descriptionContains: str | None = None,
    category: str | None = None,
    orderBy: str | None = None,
    orderDirection: str | None = "asc",
) -> list[dict[str, str | float | bool]]:
    session: Session = info.context["session"]
    query = session.query(MenuItem).filter_by(is_deleted=False)

    if category:
        query = query.filter_by(category=category)
    if nameContains:
        query = query.filter(MenuItem.name.ilike(f"%{nameContains}%"))
    if descriptionContains:
        query = query.filter(MenuItem.description.ilike(f"%{descriptionContains}%"))

    if orderBy in {"price", "name", "id"}:
        field = getattr(MenuItem, orderBy, None)
        if field is not None:
            if orderDirection == "desc":
                query = query.order_by(field.desc())
            else:
                query = query.order_by(field.asc())

    return [item.to_dict() for item in query.all()]


@query.field("menuItem")
def resolve_menu_item(_, info: GraphQLResolveInfo, id: int) -> MenuItem | None:
    session = info.context["session"]
    return session.query(MenuItem).filter_by(id=id, is_deleted=False).first()
