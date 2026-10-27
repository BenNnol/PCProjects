from fastapi.testclient import TestClient

from app.main import APP_NAME, APP_VERSION, app

client = TestClient(app)


def test_index_serves_status_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert APP_NAME in response.text


def test_info_reports_app_metadata():
    response = client.get("/api/info")

    assert response.status_code == 200
    body = response.json()
    assert body["app"] == APP_NAME
    assert body["version"] == APP_VERSION
    assert body["server_time_utc"]
