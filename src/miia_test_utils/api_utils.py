import httpx
import pytest


def assert_response_status(resp: httpx.Response, expected_status: int = 200):
    assert resp.status_code == expected_status, \
           f"Unexpected {resp.request.method} {resp.request.url} response status code (response body: {resp.text})"

    return resp


_API_KEY_AUTH_ERROR_TEST_CASES = {
    "missing_api_key": {},
    "invalid_api_key": { "X-API-Key": "XinvalidXkeyXlorenXipsumX" }
}

def make_api_key_auth_error_test(method: str, url: str):
    """
    Create a test for API key errors (missing or invalid key returning).

    The API key is passed in the `X-API-Key` header, and a `403 Forbidden`
    response is expected.

    There must be an `api` fixture of type `httpx.Client` available to be used
    by the test case.

    E.g.:
    ```
    @pytest.fixture(scope="session")
    def api:
        return httpx.Client(…)

    test_get_example_auth_error = \\
        make_api_key_auth_error_test("GET", "/example")
    ```
    """

    @pytest.mark.parametrize('case', _API_KEY_AUTH_ERROR_TEST_CASES)
    def t(case, api):
        headers  = _API_KEY_AUTH_ERROR_TEST_CASES[case]

        resp = api.request(method, url, headers=headers)
        assert_response_status(resp, httpx.codes.FORBIDDEN)

    return t
