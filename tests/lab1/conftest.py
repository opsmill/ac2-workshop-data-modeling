import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from workshop_b2.lab1.main import app
from workshop_b2.lab1.database import get_session
from workshop_b2.lab1.database.models import DeviceModel


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def device_data(session: Session):
    dev1 = DeviceModel(name="device1", manufacturer="Arista")
    dev2 = DeviceModel(name="device2", manufacturer="Nokia")
    session.add(dev1)
    session.add(dev2)
    session.commit()
