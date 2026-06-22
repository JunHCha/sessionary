from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
import pytest

from app.core.middlewares import AuthSessionMiddleware

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


@pytest.fixture
async def auth_session_error_client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """AuthSessionMiddleware.dispatch가 RuntimeError를 던지는 클라이언트.

    ServerErrorMiddleware가 AuthSession보다 바깥에 있을 때만 CORS 헤더가 붙는다.
    미들웨어 순서가 잘못되면 이 테스트는 CORS 헤더 없이 500을 받아 실패한다.
    """

    async def _raise(*args, **kwargs):
        raise RuntimeError("simulated AuthSessionMiddleware failure")

    with patch.object(AuthSessionMiddleware, "dispatch", new=AsyncMock(side_effect=_raise)):
        async with AsyncClient(
            transport=ASGITransport(app=app, raise_app_exceptions=False),
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


async def test_auth_session_middleware_error_includes_cors_header(
    auth_session_error_client: AsyncClient,
):
    """AuthSessionMiddleware 내부 예외 시에도 5xx 응답에 CORS 헤더가 붙어야 한다.

    수정 전(ServerError가 AuthSession 안쪽): 이 테스트는 FAIL.
    수정 후(ServerError가 AuthSession 바깥): 이 테스트는 PASS.
    """
    response = await auth_session_error_client.get(
        "/ping", headers={"Origin": ALLOWED_ORIGIN}
    )

    assert response.status_code == 500
    assert "access-control-allow-origin" in response.headers
