import strawberry
from typing import Annotated
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from ..database import get_session, Session
from .schema import Query


def get_context(session: Annotated[Session, Depends(get_session)]) -> dict:
    return {"session": session}


def init_app():
    schema = strawberry.Schema(Query)
    graphql_app = GraphQLRouter(schema, context_getter=get_context)

    return graphql_app
