from os import environ

import httpx

from miia_test_utils.api_fixture import api_fixture


FASTAPI_RESP = { "msg": "Loren ipsum" }


@api_fixture
def testserver_api():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()
    @app.get("/")
    async def dummy_route():
        return FASTAPI_RESP

    return TestClient(app)


ENV_VAR = "TEST_MAKE_API_FIXTURE_TEST_HOST"
environ[ENV_VAR] = "https://httpbin.org"

@api_fixture(env_var=ENV_VAR)
def env_var_api():
    raise RuntimeError("Should not have been called")


def test_make_api_fixture_env_var(env_var_api: httpx.Client):
    assert env_var_api.base_url == "https://httpbin.org"

    status_code = 234
    resp = env_var_api.get(f"/status/{status_code}")
    assert resp.status_code == status_code


def test_make_api_fixture_testserver_api(testserver_api: httpx.Client):
    assert testserver_api.base_url == "http://testserver"

    resp = testserver_api.get("/")
    assert resp.status_code == 200
    assert resp.json() == FASTAPI_RESP
