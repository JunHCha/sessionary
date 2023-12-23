import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_ping(client: AsyncClient) -> None:
    # when
    response = await client.get("/api/ping")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content == {"ping": "pong!"}


async def test_auth_ping(authorized_client: AsyncClient) -> None:
    # when
    response = await authorized_client.get("/api/ping/auth")

    # then
    assert response.status_code == 200
    content = response.json()
    assert content.get("ping") == "pong!"
    assert content.get("user").get("nickname") == "test"
    assert True
