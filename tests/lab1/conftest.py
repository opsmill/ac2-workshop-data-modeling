import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from workshop_b2.lab1.main import app
from workshop_b2.lab1.database import get_session
from workshop_b2.lab1.database.models import DeviceModel, SiteModel


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
def site_data(session: Session) -> list[SiteModel]:
    site1 = SiteModel(name="atl1", label="Atlanta 1")
    site2 = SiteModel(name="den1", label="Denver 1")
    session.add(site1)
    session.add(site2)
    session.commit()

    return [site1, site2]


@pytest.fixture
def device_data(session: Session, site_data: list[SiteModel]):
    dev1 = DeviceModel(name="device1", manufacturer="Arista", site_id=site_data[0].id)
    dev2 = DeviceModel(name="device2", manufacturer="Nokia", site_id=site_data[1].id)
    session.add(dev1)
    session.add(dev2)
    session.commit()
