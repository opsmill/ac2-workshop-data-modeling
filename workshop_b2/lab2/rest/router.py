from typing import Sequence
from fastapi import APIRouter, Depends
from neo4j import Driver

from workshop_b2.lab2.database.models import (
    CountryModel,
    DeviceModel,
    SiteModel,
    TagModel,
)
from workshop_b2.lab2.database import get_db


router = APIRouter(prefix="/api")


# ------------------------------
# DEVICES
# ------------------------------
@router.post("/devices/")
def create_device(item: DeviceModel, db: Driver = Depends(get_db)) -> DeviceModel:
    device = item.create(db)

    return device


@router.get("/devices/")
def read_devices(db: Driver = Depends(get_db)) -> Sequence[DeviceModel]:
    return DeviceModel.all(db)


# ------------------------------
# SITES
# ------------------------------
@router.post("/sites/")
def create_site(item: SiteModel, db: Driver = Depends(get_db)) -> SiteModel:
    site = item.create(db)

    return site


@router.get("/sites/")
def read_sites(db: Driver = Depends(get_db)) -> Sequence[SiteModel]:
    return SiteModel.all(db)


# ------------------------------
# COUNTRIES
# ------------------------------
@router.post("/countries/")
def create_country(item: CountryModel, db: Driver = Depends(get_db)) -> CountryModel:
    country = item.create(db)

    return country


@router.get("/countries/")
def read_countries(db: Driver = Depends(get_db)) -> Sequence[CountryModel]:
    return CountryModel.all(db)


# ------------------------------
# TAGS
# ------------------------------
@router.post("/tags/")
def create_tag(item: TagModel, db: Driver = Depends(get_db)) -> TagModel:
    tag = item.create(db)

    return tag


@router.get("/tags/")
def read_tags(db: Driver = Depends(get_db)) -> Sequence[TagModel]:
    return TagModel.all(db)
