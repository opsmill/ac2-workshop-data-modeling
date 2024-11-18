import strawberry

from .models import DeviceType, SiteType, CountryType, TagType, LocationType
# from workshop_b2.lab1.database.models import (
#     DeviceModel,
#     SiteModel,
#     CountryModel,
#     TagModel,
# )


@strawberry.type
class Query:
    @strawberry.field()
    def devices(self, info: strawberry.Info) -> list[DeviceType]:
        session = info.context["session"]
        devices = session.execute_query(
            (
                "MATCH (d:Device)-[:LOCATED_IN]->(s:Site)"
                "OPTIONAL MATCH (d)-[:TAGGED]->(t:Tag)"
                "RETURN d, s, t"
            )
        ).records
        return [
            DeviceType(
                **d["d"], **{"site": SiteType(**d["s"]), "tags": [TagType(**t) for t in d["t"]])}
            )
            for d in devices
        ]

    @strawberry.field()
    def tags(self, info: strawberry.Info) -> list[TagType]:
        session = info.context["session"]
        tags = session.execute_query(
            ("MATCH (t:Tag) OPTIONAL MATCH (t)-[:TAGGED]->(d:Device) RETURN t")
        ).records
        return [TagType(**t["t"]) for t in tags]

    @strawberry.field()
    def sites(self, info: strawberry.Info) -> list[SiteType]:
        session = info.context["session"]
        sites = session.execute_query("MATCH (s:Site) RETURN s").records
        return [SiteType(**s["s"]) for s in sites]

    @strawberry.field()
    def countries(self, info: strawberry.Info) -> list[CountryType]:
        session = info.context["session"]
        countries = session.execute_query("MATCH (c:Country) RETURN c").records
        return [CountryType(**c["c"]) for c in countries]

    # @strawberry.field()
    # def locations(self, info: strawberry.Info) -> list[LocationType]:
    #     session = info.context["session"]
    #     sites = session.exec(select(SiteType)).all()
    #     countries = session.exec(select(CountryModel)).all()
    #     return sites + countries
