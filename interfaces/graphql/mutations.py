from datetime import datetime

from ariadne import MutationType
from graphql import GraphQLError, GraphQLResolveInfo
from sqlalchemy.orm import Session

from infrastructure.db.models import MenuItem

mutation = MutationType()


@mutation.field("createMenuItem")
def resolve_create_menu_item(_, info: GraphQLResolveInfo, input: dict) -> dict:
    session: Session = info.context["session"]
    item = MenuItem(**input)
    session.add(item)
    session.commit()
    return item.to_dict()


@mutation.field("updateMenuItem")
def resolve_update_menu_item(
    _, info: GraphQLResolveInfo, id: int, input: dict
) -> dict | None:
    session: Session = info.context["session"]
    item = session.query(MenuItem).filter_by(id=id, is_deleted=False).first()

    if not item:
        return None

    for key, value in input.items():
        setattr(item, key, value)

    session.commit()
    return item.to_dict()


@mutation.field("deleteMenuItem")
def resolve_delete_menu_item(
    _, info: GraphQLResolveInfo, id: int, permanent: bool = False
) -> dict:
    session: Session = info.context["session"]
    item = session.query(MenuItem).filter_by(id=id, is_deleted=False).first()

    if not item:
        raise GraphQLError(f"MenuItem with id {id} not found.")

    if not item:
        return {"success": False, "isSoftDeleted": False}

    if permanent:
        session.delete(item)
        session.commit()
        return {"success": True, "isSoftDeleted": False}

    item.is_deleted = True
    item.deleted_at = datetime.utcnow()
    session.commit()
    return {"success": True, "isSoftDeleted": True}


@mutation.field("restoreMenuItem")
def resolve_restore_menu_item(_, info, id: int) -> dict:
    session: Session = info.context["session"]
    item = session.query(MenuItem).filter_by(id=id).first()

    if not item:
        raise GraphQLError(f"MenuItem with id {id} does not exist.")
    if not item.is_deleted:
        raise GraphQLError(
            f"MenuItem with id {id} is not deleted and cannot be restored."
        )

    item.is_deleted = False
    item.deleted_at = None
    session.commit()
    return item.to_dict()
