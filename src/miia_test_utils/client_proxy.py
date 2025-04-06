import httpx


class ClientProxy:
    """
    Proxy the requests to the HTTP client injecting predefined headers.

    Allows reusing a single client instance (i.e. a single TCP connection) with
    many different client-level configurations (e.g. authentication credentials)
    in isolation for each test context without messing with the global HTTP
    client state.

    E.g.:
    ```
    import httpx
    import pytest

    from miia_test_utils.client_proxy import ClientProxy

    @pytest.fixture
    def api():
        return httpx.Client(…)

    @pytest.fixture
    def auth_api(api):
        credentials = …
        resp = assert_response_status( api.post("/login", auth=credentials) )
        token = resp.json()["access_token"]

        headers = { "Authorization": f"Bearer {token}" }
        proxy = ClientProxy(api, headers)
    ```
    """

    def __init__(self, client: httpx.Client, headers: dict | httpx.Headers):
        self._client = client
        self._headers = headers.copy()

    def __getattr__(self, name):
        attr = getattr(self._client, name)

        if name in [ 'request', 'get', 'post', 'put', 'delete', 'head',
                     'options', 'patch' ]:
            return self._wrap_request_callable(attr)

        return attr

    def _wrap_request_callable(self, attr):
        def wrapper(*args, **kwargs):
            headers_arg = kwargs.setdefault('headers', self._headers)

            if headers_arg != self._headers:
                merged_headers = httpx.Headers(self._headers)
                merged_headers.update(headers_arg)
                kwargs['headers'] = merged_headers

            return attr(*args, **kwargs)

        return wrapper
