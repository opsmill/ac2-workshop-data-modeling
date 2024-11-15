from os import name
from typing import Dict, Sequence
from fastapi import APIRouter, Depends, HTTPException
from neo4j import Driver
from neo4j.exceptions import ConstraintError

from workshop_b2.lab2.database.models import (
    CountryModel,
    DeviceModel,
    SiteModel,
    TagModel,
)
from workshop_b2.lab2.database import get_db


router = APIRouter(prefix="/api")


def _build_filter_query(filters: Dict) -> str:
    query_filter = ", ".join(
        [f'{key}: "{value}"' for key, value in filters.items() if value]
    )
    query_filter = "{" + query_filter + "}" if query_filter else ""
    return query_filter


# ------------------------------
# DEVICES
# ------------------------------
@router.post("/devices/")
def create_device(item: DeviceModel, db: Driver = Depends(get_db)) -> DeviceModel:
    query_params = item.model_dump()
    if item.site:
        query_filter = _build_filter_query(item.site.model_dump())
        site = db.execute_query(f"MATCH (s:Site {query_filter}) RETURN s")
        if not site.records:
            raise HTTPException(status_code=404, detail="Site not found")

        query_params.pop("site")
        query_params["site_name"] = site.records[0]["s"]["name"]
        query = """
        MATCH (s:Site {name: $site_name})
        CREATE (d:Device {name: $name, manufacturer: $manufacturer, status: $status})
        CREATE (d)-[:LOCATED_IN]->(s)
        """
    else:
        query = """
        CREATE (d:Device {name: $name, manufacturer: $manufacturer, status: $status})
        """
    try:
        db.execute_query(query, query_params)
    except ConstraintError:
        raise HTTPException(
            status_code=409, detail=f"Device ({item.name})already exists"
        )
    device = db.execute_query(
        "MATCH (d:Device {name: $name})-[:LOCATED_IN]->(s:Site) RETURN d, s",
        {"name": item.name},
    ).records[0]

    return DeviceModel(**device["d"], site=SiteModel(**device["s"]))


@router.get("/devices/")
def read_devices(db: Driver = Depends(get_db)) -> Sequence[DeviceModel]:
    query = """
    MATCH (d:Device)-[:LOCATED_IN]->(s:Site)
    RETURN d, s
    """
    result = db.execute_query(query)

    return [
        DeviceModel(**device["d"], site=SiteModel(**device["s"]))
        for device in result.records
    ]


# ------------------------------
# SITES
# ------------------------------
@router.post("/sites/")
def create_site(item: SiteModel, db: Driver = Depends(get_db)) -> SiteModel:
    query = """
    CREATE (s:Site {name: $name, label: $label, description: $description, address: $address})
    """
    try:
        db.execute_query(query, item.model_dump())
    except ConstraintError:
        raise HTTPException(
            status_code=409, detail=f"Site ({item.name}) already exists"
        )
    site = db.execute_query(
        "MATCH (s:Site {name: $name}) RETURN s", {"name": item.name}
    ).records[0]

    return SiteModel(**site[0])


@router.get("/sites/")
def read_sites(db: Driver = Depends(get_db)) -> Sequence[SiteModel]:
    query = """
    MATCH (s:Site)
    RETURN s
    """
    result = db.execute_query(query)

    return [SiteModel(**s["s"]) for s in result.records]


# ------------------------------
# COUNTRIES
# ------------------------------
@router.post("/countries/")
def create_country(item: CountryModel, db: Driver = Depends(get_db)) -> CountryModel:
    query = """
    CREATE (c:Country {name: $name, label: $label, description: $description, continent: $continent})
    """
    try:
        db.execute_query(query, item.model_dump())
    except ConstraintError:
        raise HTTPException(
            status_code=409, detail=f"Country ({item.name}) already exists"
        )
    country = db.execute_query(
        "MATCH (c:Country {name: $name}) RETURN c", {"name": item.name}
    ).records[0]

    return CountryModel(**country[0])


@router.get("/countries/")
def read_countries(db: Driver = Depends(get_db)) -> Sequence[CountryModel]:
    query = """
    MATCH (c:Country)
    RETURN c
    """
    result = db.execute_query(query)

    return [CountryModel(**s["c"]) for s in result.records]


# ------------------------------
# TAGS
# ------------------------------
@router.post("/tags/")
def create_tag(item: TagModel, db: Driver = Depends(get_db)) -> TagModel:
    query = """
    CREATE (t:Tag {name: $name, color: $color})
    """
    try:
        db.execute_query(query, item.model_dump())
    except ConstraintError:
        raise HTTPException(status_code=409, detail=f"Tag ({item.name}) already exists")
    tag = db.execute_query(
        "MATCH (t:Tag {name: $name}) RETURN t", {"name": item.name}
    ).records[0]

    return TagModel(**tag[0])


@router.get("/tags/")
def read_tags(db: Driver = Depends(get_db)) -> Sequence[TagModel]:
    # items = db.exec(select(TagModel)).all()
    query = """
    MATCH (t:Tag)
    RETURN t
    """
    result = db.execute_query(query)

    return [TagModel(**s["t"]) for s in result.records]
