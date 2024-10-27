from contextlib import asynccontextmanager
from fastapi import FastAPI

from workshop_b2.lab1.database import create_db_and_tables
from workshop_b2.lab1.rest.router import router as rest_router
from workshop_b2.lab1.graphql.router import init_app


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
