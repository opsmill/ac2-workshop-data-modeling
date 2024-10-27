import strawberry

from workshop_b2.models import Device, Country, Site, Location, Tag


@strawberry.experimental.pydantic.interface(model=Location, all_fields=True)
class LocationType: ...


@strawberry.experimental.pydantic.type(model=Country, all_fields=True)
class CountryType(LocationType): ...


@strawberry.experimental.pydantic.type(model=Site, all_fields=True)
class SiteType(LocationType): ...


@strawberry.experimental.pydantic.type(model=Device, all_fields=True)
class DeviceType:
    site: SiteType


@strawberry.experimental.pydantic.type(model=Tag, all_fields=True)
class TagType: ...
