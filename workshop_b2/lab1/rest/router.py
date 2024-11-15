from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from workshop_b2.lab1.database.models import (
    DeviceModel,
    SiteModel,
    CountryModel,
    TagModel,
)
from workshop_b2.lab1.database import get_session

router = APIRouter(prefix="/api")


# ------------------------------
# DEVICES
# ------------------------------
@router.post("/devices/")
def create_device(item: DeviceModel, db: Session = Depends(get_session)) -> DeviceModel:
    db.add(item)
    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    db.refresh(item)
    return item


@router.get("/devices/")
def read_devices(db: Session = Depends(get_session)) -> Sequence[DeviceModel]:
    items = db.exec(select(DeviceModel)).all()
    return items


# ------------------------------
# SITES
# ------------------------------
@router.post("/sites/")
def create_site(item: SiteModel, db: Session = Depends(get_session)) -> SiteModel:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/sites/")
def read_sites(db: Session = Depends(get_session)) -> Sequence[SiteModel]:
    items = db.exec(select(SiteModel)).all()
    return items


# ------------------------------
# COUNTRIES
# ------------------------------
@router.post("/countries/")
def create_country(
    item: CountryModel, db: Session = Depends(get_session)
) -> CountryModel:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/countries/")
def read_countries(db: Session = Depends(get_session)) -> Sequence[CountryModel]:
    items = db.exec(select(CountryModel)).all()
    return items


# ------------------------------
# TAGS
# ------------------------------
@router.post("/tags/")
def create_tag(item: TagModel, db: Session = Depends(get_session)) -> TagModel:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/tags/")
def read_tags(db: Session = Depends(get_session)) -> Sequence[TagModel]:
    items = db.exec(select(TagModel)).all()
    return items
