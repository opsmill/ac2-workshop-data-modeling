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


def create_initial_nodes() -> None:
    db = get_db()
    with db.session(database="neo4j") as session:
        session.run(
            """
            CREATE (c:Country {name: "United States"})
            CREATE (s:Site {name: "Site 1"})
            CREATE (d:Device {name: "Device 1"})
            CREATE (t:Tag {name: "Tag 1"})
            """
        )
        session.run(
            """
            MATCH (s:Site {name: "Site 1"})
            MATCH (c:Country {name: "United States"})
            CREATE (s)-[:LOCATED_IN]->(c)
            """
        )
        session.run(
            """
            MATCH (d:Device {name: "Device 1"})
            MATCH (s:Site {name: "Site 1"})
            CREATE (d)-[:LOCATED_AT]->(s)
            """
        )
        session.run(
            """
            MATCH (d:Device {name: "Device 1"})
            MATCH (t:Tag {name: "Tag 1"})
            CREATE (d)-[:TAGGED_WITH]->(t)
            """
        )
        session.run(
            """
            MATCH (d:Device {name: "Device 1"})
            MATCH (t:Tag {name: "Tag 1"})
            CREATE (t)-[:TAGS]->(d)
            """
        )
        session.run(
            """
            MATCH (t:Tag {name: "Tag 1"})
            MATCH (s:Site {name: "Site 1"})
            CREATE (t)-[:TAGGED_AT]->(s)
            """
        )
        session.run(
            """
            MATCH (t:Tag {name: "Tag 1"})
            MATCH (c:Country {name: "United States"})
            CREATE (t)-[:TAGGED_IN]->(c)
            """
        )
        session.run(
            """
            MATCH (s:Site {name: "Site 1"})
            MATCH (c:Country {name: "United States"})
            CREATE (s)-[:LOCATED_IN]->(c)
            """
        )
        session.run(
            """
            MATCH (d:Device {name: "Device 1"})
            MATCH (s:Site {name: "Site 1"})
            CREATE (d)-[:LOCATED_AT]->(s)
            """
        )
