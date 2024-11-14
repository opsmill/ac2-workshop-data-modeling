import strawberry

from .models import DeviceType, SiteType, CountryType, TagType, LocationType
from sqlmodel import select
from workshop_b2.lab1.database.models import (
    DeviceModel,
    SiteModel,
    CountryModel,
    TagModel,
)


@strawberry.type
class Query:
    @strawberry.field()
    def devices(self, info: strawberry.Info) -> list[DeviceType]:
        session = info.context["session"]
        return session.exec(select(DeviceModel)).all()

    @strawberry.field()
    def tags(self, info: strawberry.Info) -> list[TagType]:
        session = info.context["session"]
        return session.exec(select(TagModel)).all()

    @strawberry.field()
    def sites(self, info: strawberry.Info) -> list[SiteType]:
        session = info.context["session"]
        return session.exec(select(SiteModel)).all()

    @strawberry.field()
    def countries(self, info: strawberry.Info) -> list[CountryType]:
        session = info.context["session"]
        return session.exec(select(CountryModel)).all()

    @strawberry.field()
    def locations(self, info: strawberry.Info) -> list[LocationType]:
        session = info.context["session"]
        sites = session.exec(select(SiteType)).all()
        countries = session.exec(select(CountryModel)).all()
        return sites + countries
