from fastapi.testclient import TestClient


def test_create_device(client: TestClient) -> None:
    # when
    response = client.get("/ping")

    # then
    content = response.json()
    assert response.status_code == 200
    assert content == {"ping": "pong!"}
