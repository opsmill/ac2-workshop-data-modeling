import uuid
from pathlib import Path

import httpx
from invoke import Context, task

from workshop_b2.models import Device

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
def create_device(url: str) -> httpx.Response:
    dev = Device(name=f"device-{str(uuid.uuid4())[-8:]}")
    with httpx.Client() as client:
        return client.post(f"{url}/api/devices/", json=dev.model_dump())


@task
def start_lab1(context: Context, reload: bool = True) -> None:
    """Start lab1."""
    exec_cmd = "fastapi run workshop_b2/lab1/main.py"
    if reload:
        exec_cmd += " --reload"
    context.run(exec_cmd)


@task
def load_lab1(context: Context, url: str = "http://localhost:8000"):
    for idx in range(0, 5):
        response = create_device(url=url)
        response.raise_for_status()


@task
def start_lab2(context: Context, reload: bool = True) -> None:
    exec_cmd = "fastapi run workshop_b2/lab2/main.py --port 8001"
    if reload:
        exec_cmd += " --reload"
    context.run("docker compose up -d")
    context.run(exec_cmd)


@task
def destroy_lab2(context: Context, reload: bool = False) -> None:
    context.run("docker compose down -v")


@task
def load_lab2(context: Context, url: str = "http://localhost:8001") -> None:
    for idx in range(0, 5):
        response = create_device(url=url)
        response.raise_for_status()
