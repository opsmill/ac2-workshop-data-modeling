from __future__ import annotations

from workshop_b2.models import Device, Site, Country, Tag
from sqlmodel import Field, SQLModel, Relationship


class CountryModel(Country, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SiteModel(Site, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


class DeviceModel(Device, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    site_id: int = Field(foreign_key="sitemodel.id")
    site: SiteModel = Relationship()


class TagModel(Tag, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
