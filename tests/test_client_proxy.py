from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import pytest

from miia_test_utils.client_proxy import ClientProxy


@pytest.fixture
def api():
    app = FastAPI()

    @app.get("/")
    async def echo(req: Request):
        return { k: v for k, v in req.headers.items() if k.lower().startswith('x') }

    return TestClient(app)


def test_client_proxy(api):
    proxy_1_headers = { "x-header-1": "Loren" }
    proxy_1 = ClientProxy(api, proxy_1_headers)

    proxy_2_headers = { "x-header-2": "Ipsun" }
    proxy_2 = ClientProxy(api, proxy_2_headers)

    resp = proxy_1.get("/")
    assert resp.json() == proxy_1_headers

    resp = api.get("/")
    assert resp.json() == {}

    resp = proxy_2.get("/")
    assert resp.json() == proxy_2_headers
