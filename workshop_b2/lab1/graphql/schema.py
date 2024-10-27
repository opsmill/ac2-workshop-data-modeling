import strawberry

from .models import DeviceType
from sqlmodel import select
from workshop_b2.lab1.database.models import DeviceModel


@strawberry.type
class Query:
    @strawberry.field()
    def devices(self, info: strawberry.Info) -> list[DeviceType]:
        session = info.context["session"]
        return session.exec(select(DeviceModel)).all()
        # return [ Device(**item.model_dump(ex)) for item in devices ]

        # return DeviceType.get_all()
