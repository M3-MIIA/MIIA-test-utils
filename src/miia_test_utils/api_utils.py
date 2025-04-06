import httpx


def assert_response_status(resp: httpx.Response, expected_status: int = 200):
    assert resp.status_code == expected_status, \
           f"Unexpected {resp.request.method} {resp.request.url} response status code (response body: {resp.text})"

    return resp
