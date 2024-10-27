from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from workshop_b2.lab1.database.models import DeviceModel
from workshop_b2.lab1.database import get_session

router = APIRouter(prefix="/api")


@router.post("/devices/")
def create_device(device: DeviceModel, db: Session = Depends(get_session)):
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


@router.get("/devices/")
def read_devices(db: Session = Depends(get_session)):
    devices = db.exec(select(DeviceModel)).all()
    return devices
