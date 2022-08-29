import pytest

from fastapi.testclient import TestClient
from main_auth import app_auth


@pytest.mark.auth
@pytest.mark.skip(reason="TODO: clear db")
def test_dron_signin():
    with TestClient(app=app_auth) as client:
        data = {"login": "testdron", "password": "123"}
        response = client.post(url="/api/v1/userdrons/signin", json=data)
        resp = response.json()
        assert response.status_code == 200
        assert resp["name"] == data["login"], resp
        assert resp["hashed_password"] is not None


@pytest.mark.auth
def test_dron_login():
    with TestClient(app=app_auth) as client:
        data = {"login": "testdron", "password": "123"}
        response = client.post(url="/api/v1/userdrons/signin", json=data)
        resp = response.json()
        assert response.status_code == 200
        print(resp)
        assert resp["name"] == data["login"], resp

        data = {"login": "testdron", "password": "123"}
        response = client.post(url="/api/v1/userdrons/login", json=data)
        resp = response.json()
        assert response.status_code == 200
        assert resp["access_token"] is not None
        assert resp["refresh_token"] is not None
