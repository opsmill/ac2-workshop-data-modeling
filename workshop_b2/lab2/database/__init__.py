from neo4j import GraphDatabase, Session

db_server = "localhost"
db_url = f"neo4j://{db_server}"

db = None


def get_db():
    global db
    if db:
        return db
    db = GraphDatabase.driver(db_url, auth=("neo4j", "admin"))
    return db


def get_session() -> Session:
    global db
    if db is None:
        db = get_db()
    with db.session(database="neo4j") as session:
        yield session


def create_initial_constraints() -> None:
    db = get_db()
    with db.session(database="neo4j") as session:
        session.run(
            """
            CREATE CONSTRAINT site_name IF NOT EXISTS FOR (s:Site) REQUIRE s.name IS UNIQUE;
            """
        )
        session.run(
            """
            CREATE CONSTRAINT device_name IF NOT EXISTS FOR (d:Device) REQUIRE d.name IS UNIQUE;
            """
        )
        session.run(
            """
            CREATE CONSTRAINT country_name IF NOT EXISTS FOR (c:Country) REQUIRE c.name IS UNIQUE;
            """
        )
        session.run(
            """
            CREATE CONSTRAINT tag_name IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE;
            """
        )
