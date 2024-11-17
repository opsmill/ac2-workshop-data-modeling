from __future__ import annotations
from typing import Dict

from fastapi import HTTPException
from neo4j import Driver
from neo4j.exceptions import ConstraintError
from pydantic import Field

from workshop_b2.models import Device, Site, Country, Tag


def _build_filter_query(filters: Dict) -> str:
    query_filter = ", ".join(
        [f'{key}: "{value}"' for key, value in filters.items() if value]
    )
    query_filter = "{" + query_filter + "}" if query_filter else ""
    return query_filter


class TagMixin:
    tags: list[Tag] = Field(default_factory=list)

    def add_tags(self, db: Driver, tags: list[Tag]):
        """Add tags to a node.

        Args:
            db (Driver): Neo4j driver instance.
            tags (list[Tag]): List of tags to add.
        """
        node_label = self.__class__.__name__.replace("Model", "").title()
        node_short = node_label[0]
        tag = tags[0]
        query = (
            f"MATCH ({node_short}:{node_label}" + " {name: $name})"
            "OPTIONAL MATCH (t:Tag {name: " + f'"{tag.name}"' + "})"
            f"MERGE ({node_short})-[:TAGGED]->(t)"
        )
        db.execute_query(
            query, {"name": self.name, "tags": [t.model_dump() for t in tags]}
        )


class CountryModel(Country):
    @staticmethod
    def all(db: Driver):
        """Get all countries from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            list[CountryModel]: List of all countries.
        """
        query = """
        MATCH (c:Country)
        RETURN c
        """
        result = db.execute_query(query)

        return [CountryModel(**s["c"]) for s in result.records]

    def create(self, db: Driver):
        """Create a new country in the database.

        Args:
            db (Driver): Neo4j driver instance.
        """
        query = """
        CREATE (c:Country {name: $name, label: $label, description: $description, continent: $continent})
        """
        try:
            db.execute_query(query, self.model_dump())
        except ConstraintError:
            raise HTTPException(
                status_code=409, detail=f"Country ({self.name}) already exists"
            )

        country = self.get(db)

        return country

    def get(self, db: Driver):
        """Get a device from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            CountryModel: Country instance.
        """
        country = db.execute_query(
            "MATCH (c:Country {name: $name}) RETURN c", {"name": self.name}
        ).records[0]

        return CountryModel(**country[0])


class SiteModel(Site):
    @staticmethod
    def all(db: Driver):
        """Get all sites from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            list[SiteModel]: List of all sites.
        """
        query = """
        MATCH (s:Site)
        RETURN s
        """
        result = db.execute_query(query)

        return [SiteModel(**s["s"]) for s in result.records]

    def create(self, db: Driver):
        """Create a new site in the database.

        Args:
            db (Driver): Neo4j driver instance.
        """
        query = """
        CREATE (s:Site {name: $name, label: $label, description: $description, address: $address})
        """
        try:
            db.execute_query(query, self.model_dump())
        except ConstraintError:
            raise HTTPException(
                status_code=409, detail=f"Site ({self.name}) already exists"
            )

        site = self.get(db)

        return site

    def get(self, db: Driver):
        """Get a site from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            SiteModel: Site instance.
        """
        site = db.execute_query(
            "MATCH (s:Site {name: $name}) RETURN s", {"name": self.name}
        ).records[0]

        return SiteModel(**site[0])


class DeviceModel(Device, TagMixin):
    site: SiteModel

    @staticmethod
    def all(db: Driver):
        """Get all devices from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            list[DeviceModel]: List of devices.
        """
        query = """
        MATCH (d:Device)-[:LOCATED_IN]->(s:Site)
        OPTIONAL MATCH (d)-[:TAGGED]->(t:Tag)
        RETURN d, s, t
        """
        result = db.execute_query(query)
        return [
            DeviceModel(**device["d"], site=SiteModel(**device["s"]), tags=device["t"])
            for device in result.records
        ]

    def _find_site(self, db: Driver):
        """Find a site in the database.

        Args:
            db (Driver): Neo4j driver instance.
        """
        query_filter = _build_filter_query(self.site.model_dump())
        site = db.execute_query(f"MATCH (s:Site {query_filter}) RETURN s")
        if not site.records:
            raise HTTPException(status_code=404, detail="Site not found")

        return site.records[0]["s"]

    def create(self, db: Driver):
        """Create a new device in the database.

        Args:
            db (Driver): Neo4j driver instance.
        """
        query_params = self.model_dump()
        if not query_params["tags"]:
            query_params.pop("tags")
        if self.site:
            found_site = self._find_site(db)
            if found_site:
                query_params.pop("site")
                query_params["site_name"] = found_site["name"]
                query = """
                MATCH (s:Site {name: $site_name})
                CREATE (d:Device {name: $name, manufacturer: $manufacturer, status: $status})
                CREATE (d)-[:LOCATED_IN]->(s)
                """
        try:
            db.execute_query(query, query_params)
        except ConstraintError:
            raise HTTPException(
                status_code=409, detail=f"Device ({self.name})already exists"
            )

        self.add_tags(db, self.tags)
        return self.get(db)

    def get(self, db: Driver):
        """Get a device from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            DeviceModel: Device instance.
        """
        device = db.execute_query(
            "MATCH (d:Device {name: $name})-[:LOCATED_IN]->(s:Site) RETURN d, s",
            {"name": self.name},
        ).records[0]

        return DeviceModel(**device["d"], site=SiteModel(**device["s"]))


class TagModel(Tag):
    @staticmethod
    def all(db: Driver):
        """Get all tags from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            list[TagModel]: List of all tags.
        """
        query = """
        MATCH (t:Tag)
        RETURN t
        """
        result = db.execute_query(query)

        return [TagModel(**t["t"]) for t in result.records]

    def create(self, db: Driver):
        """Create a new tag in the database.

        Args:
            db (Driver): Neo4j driver instance.
        """
        query = """
        CREATE (t:Tag {name: $name, color: $color})
        """
        try:
            db.execute_query(query, self.model_dump())
        except ConstraintError:
            raise HTTPException(
                status_code=409, detail=f"Tag ({self.name}) already exists"
            )

        tag = self.get(db)

        return tag

    def get(self, db: Driver):
        """Get a tag from the database.

        Args:
            db (Driver): Neo4j driver instance.

        Returns:
            TagModel: Tag instance.
        """
        tag = db.execute_query(
            "MATCH (t:Tag {name: $name}) RETURN t", {"name": self.name}
        ).records[0]

        return TagModel(**tag[0])
