from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
import pytest

ALLOWED_ORIGIN = "http://testorigin.example"


@pytest.fixture
async def app_with_failing_route(app: FastAPI) -> FastAPI:
    async def _boom():
        raise RuntimeError("internal secret detail should not leak")

    app.add_api_route("/_test_boom", _boom, methods=["GET"])
    return app


@pytest.fixture
async def error_client(
    app_with_failing_route: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(
            app=app_with_failing_route, raise_app_exceptions=False
        ),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


async def test_5xx_response_includes_cors_header(error_client: AsyncClient):
    response = await error_client.get(
        "/_test_boom", headers={"Origin": ALLOWED_ORIGIN}
    )

    assert response.status_code == 500
    assert "access-control-allow-origin" in response.headers


async def test_5xx_response_does_not_leak_internal_detail(error_client: AsyncClient):
    response = await error_client.get(
        "/_test_boom", headers={"Origin": ALLOWED_ORIGIN}
    )

    assert response.status_code == 500
    assert "internal secret detail should not leak" not in response.text


async def test_200_response_still_includes_cors_header(client: AsyncClient):
    response = await client.get("/ping", headers={"Origin": ALLOWED_ORIGIN})

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
