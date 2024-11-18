from __future__ import annotations

from workshop_b2.models import Device, Site, Country, Tag
from sqlmodel import Field, SQLModel, Relationship


class CountryModel(Country, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


class SiteModel(Site, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


# class DeviceTagLink(SQLModel, table=True):
#     device_id: int = Field(foreign_key="devicemodel.id", primary_key=True)
#     tag_id: int = Field(foreign_key="tagmodel.id", primary_key=True)


class DeviceModel(Device, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    site_id: int = Field(foreign_key="sitemodel.id")
    site: SiteModel = Relationship()
    # tags: list[TagModel] = Relationship(
    #     link_model=DeviceTagLink, back_populates="devices"
    # )


class TagModel(Tag, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # devices: list[DeviceModel] = Relationship(
    #     link_model=DeviceTagLink, back_populates="tags"
    # )
