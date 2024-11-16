import uuid
from pathlib import Path

import httpx
from invoke import Context, task

from workshop_b2.lab1.database import models as Lab1Models
from workshop_b2.lab2.database import models as Lab2Models


MAIN_DIRECTORY_PATH = Path(__file__).parent


@task
def format(context: Context) -> None:
    """Run RUFF to format all Python files."""

    exec_cmds = ["ruff format .", "ruff check . --fix"]
    with context.cd(MAIN_DIRECTORY_PATH):
        for cmd in exec_cmds:
            context.run(cmd)


@task
def lint_yaml(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with yamllint")
    exec_cmd = "yamllint ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task
def lint_pyright(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with mypy")
    exec_cmd = "pyright workshop_b2"
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task
def lint_ruff(context: Context) -> None:
    """Run Linter to check all Python files."""
    print(" - Check code with ruff")
    exec_cmd = "ruff check ."
    with context.cd(MAIN_DIRECTORY_PATH):
        context.run(exec_cmd)


@task(name="lint")
def lint_all(context: Context) -> None:
    """Run all linters."""
    lint_yaml(context)
    lint_ruff(context)
    lint_pyright(context)


###
## Lab Commands
###
def create_lab1_devices(url: str, site_id: int) -> httpx.Response:
    dev = Lab1Models.DeviceModel(
        name=f"device-{str(uuid.uuid4())[-8:]}", manufacturer="cisco", site_id=site_id
    )
    with httpx.Client() as client:
        print(f"Creating device: {dev.model_dump()}")
        return client.post(f"{url}/api/devices/", json=dev.model_dump())


@task
def lab1_start(context: Context, reload: bool = True) -> None:
    """Start Lab1."""
    exec_cmd = "fastapi run workshop_b2/lab1/main.py"
    if reload:
        exec_cmd += " --reload"
    context.run(exec_cmd)


@task
def lab1_destroy(context: Context, reload: bool = False) -> None:
    """Destroy Lab1."""
    context.run("rm database.db")


@task
def lab1_load(
    context: Context, url: str = "http://localhost:8000", site_name: str = "site-1"
) -> None:
    """Load devices into Lab1."""
    with httpx.Client() as client:
        response = client.get(f"{url}/api/sites/")
        response.raise_for_status()
        site_id = [s["id"] for s in response.json() if s["name"] == site_name]
        if not site_id:
            response = client.post(
                f"{url}/api/sites/",
                json={
                    "name": site_name,
                    "site_id": site_id,
                    "address": "123 Wall Street",
                    "label": site_name,
                },
            )
            response.raise_for_status()
            site_id = response.json()["id"]

    for _ in range(0, 5):
        response = create_lab1_devices(url=url, site_id=site_id)
        response.raise_for_status()


@task
def lab1_test(context: Context) -> None:
    """Run pytest against Lab1."""
    exec_cmd = "pytest tests/lab1"
    context.run(exec_cmd)


def create_lab2_devices(url: str, site_name: str) -> httpx.Response:
    dev = Lab2Models.DeviceModel(
        name=f"device-{str(uuid.uuid4())[-8:]}",
        site={"name": site_name, "label": site_name, "address": "123 Wall Street"},
    )
    with httpx.Client() as client:
        print(f"Creating device: {dev.model_dump()}")
        return client.post(f"{url}/api/devices/", json=dev.model_dump())


@task
def lab2_start(context: Context, reload: bool = True) -> None:
    """Start Lab2."""
    exec_cmd = "fastapi run workshop_b2/lab2/main.py --port 8001"
    if reload:
        exec_cmd += " --reload"
    context.run("docker compose up -d")
    context.run(exec_cmd)


@task
def lab2_destroy(context: Context, reload: bool = False) -> None:
    """Destroy Lab2."""
    context.run("docker compose down -v")


@task
def lab2_load(
    context: Context, url: str = "http://localhost:8001", site_name: str = "site-1"
) -> None:
    """Load devices into Lab2."""
    with httpx.Client() as client:
        response = client.get(f"{url}/api/sites/")
        response.raise_for_status()
        site_id = [s["name"] for s in response.json() if s["name"] == site_name]
        if not site_id:
            response = client.post(
                f"{url}/api/sites/",
                json={
                    "name": site_name,
                    "label": site_name,
                    "address": "123 Wall Street",
                },
            )
            response.raise_for_status()

    for _ in range(0, 5):
        response = create_lab2_devices(url=url, site_name=site_name)
        response.raise_for_status()


# @task
# def lab2_test(context: Context) -> None:
#     """Run pytest against Lab2."""
#     exec_cmd = "pytest tests/lab2"
#     context.run(exec_cmd)
