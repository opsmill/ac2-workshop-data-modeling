from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from workshop_b2.lab1.database import create_db_and_tables
from workshop_b2.lab1.rest.router import router as rest_router
from workshop_b2.lab1.graphql.router import init_app

from graphql import print_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Autocon2 Workshopo B2 - Lab1",
    docs_url="/docs",
    lifespan=lifespan,
)

app.include_router(rest_router)

graphql_app = init_app()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/schema.graphql", include_in_schema=True)
async def get_graphql_schema() -> PlainTextResponse:
    return PlainTextResponse(content=print_schema(graphql_app.schema._schema))  # type: ignore
