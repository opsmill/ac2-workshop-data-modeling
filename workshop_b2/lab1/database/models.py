from workshop_b2.models import Device
from sqlmodel import Field, SQLModel


class DeviceModel(Device, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
