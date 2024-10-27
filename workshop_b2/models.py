from pydantic import BaseModel, Field


from enum import Enum


class Continent(str, Enum):
    EUROPE = "europe"
    ASIA = "asia"
    AMERICA = "america"
    AFRICA = "africa"


class DeviceStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"


class Location(BaseModel):
    name: str = Field(description="Unique identifier of a location")
    label: str
    description: str | None


class Country(Location):
    continent: Continent


class Site(Location):
    address: str | None


class Device(BaseModel):
    name: str
    manufacturer: str | None = None
    status: DeviceStatus = DeviceStatus.ACTIVE


class Tag(BaseModel):
    name: str
    color: str
