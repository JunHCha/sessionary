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
