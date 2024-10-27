import strawberry

from workshop_b2.models import Device


@strawberry.experimental.pydantic.type(model=Device, all_fields=True)
class DeviceType: ...
