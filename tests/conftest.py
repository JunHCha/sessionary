from typing import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> Generator:
    from app.main import app

    with TestClient(app) as c:
        yield c
