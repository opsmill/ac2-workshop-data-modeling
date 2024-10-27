import typer
import httpx
import uuid

from workshop_b2.models import Device

app = typer.Typer()


def create_device(url: str):
    dev = Device(name=f"device-{str(uuid.uuid4())[-8:]}")
    with httpx.Client() as client:
        return client.post(f"{url}/api/devices/", json=dev.model_dump())


@app.command()
def lab1(url: str = "http://localhost:8000"):
    for idx in range(0, 5):
        response = create_device(url=url)
        response.raise_for_status()


@app.command()
def lab2(url: str = "http://localhost:8000"):
    pass


if __name__ == "__main__":
    app()
