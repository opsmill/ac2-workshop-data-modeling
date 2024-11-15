from os import name
from typing import Dict, Sequence
from fastapi import APIRouter, Depends, HTTPException
from neo4j import Driver

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
def create_device(item: DeviceModel, db: Driver = Depends(get_db)):
    existing_device = db.execute_query(
        "MATCH (d:Device {name: $name}) RETURN d", {"name": item.name}
    )
    if existing_device.records:
        raise HTTPException(
            status_code=409, detail=f"Device {item.name} already exists"
        )

    query = ""
    query_params = item.model_dump()
    if item.site:
        query_filter = _build_filter_query(item.site.model_dump())
        site = db.execute_query(f"MATCH (s:Site {query_filter}) RETURN s")
        if not site.records:
            raise HTTPException(status_code=404, detail="Site not found")

        query_params.pop("site")
        query_params["site_name"] = site.records[0]["s"]["name"]
        query += """
        MATCH (s:Site {name: $site_name})
        CREATE (d:Device {name: $name, manufacturer: $manufacturer, status: $status})
        CREATE (d)-[:LOCATED_IN]->(s)
        """
    else:
        query += """
        CREATE (d:Device {name: $name, manufacturer: $manufacturer, status: $status})
        """
    db.execute_query(query, query_params)
    device = db.execute_query(
        "MATCH (d:Device {name: $name}) RETURN d", {"name": item.name}
    ).records[0]
    return device[0]


@router.get("/devices/")
def read_devices(db: Driver = Depends(get_db)):
    read_device_query = """
    MATCH (d:Device)
    RETURN d
    """
    result = db.execute_query(read_device_query)

    return result.records


# ------------------------------
# SITES
# ------------------------------
@router.post("/sites/")
def create_site(item: SiteModel, db: Driver = Depends(get_db)) -> SiteModel:
    create_site_query = """
    CREATE (s:Site {name: $name, label: $label, description: $description, address: $address})
    """
    db.execute_query(create_site_query, item.model_dump())
    site = db.execute_query(
        "MATCH (s:Site {name: $name}) RETURN s", {"name": item.name}
    ).records[0]
    return site[0]


@router.get("/sites/")
def read_sites(db: Driver = Depends(get_db)):
    read_device_query = """
    MATCH (s:Site)
    RETURN s
    """
    result = db.execute_query(read_device_query)

    return result.records


# ------------------------------
# COUNTRIES
# ------------------------------
# @router.post("/countries/")
# def create_country(
#     item: CountryModel, db: Session = Depends(get_session)
# ) -> CountryModel:
#     # db.add(item)
#     # db.commit()
#     # db.refresh(item)
#     return item
#
#
# @router.get("/countries/")
# def read_countries(db: Session = Depends(get_session)) -> Sequence[Country]:
#     items = db.exec(select(CountryModel)).all()
#     return items


# ------------------------------
# TAGS
# ------------------------------
# @router.post("/tags/")
# def create_tag(item: Tag, db: Session = Depends(get_session)) -> Tag:
#     # db.add(item)
#     # db.commit()
#     # db.refresh(item)
#     return item
#
#
# @router.get("/tags/")
# def read_tags(db: Session = Depends(get_session)) -> Sequence[Tag]:
#     # items = db.exec(select(TagModel)).all()
#     return items
