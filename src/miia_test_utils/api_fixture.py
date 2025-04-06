from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from os import getenv
from typing import overload

import httpx
import pytest


_HTTP_TIMEOUT = httpx.Timeout(5.0, read=10.0)


# Helper types _________________________________________________________________
_ApiFixtureFunc = Callable[[], httpx.Client]


@dataclass
class _ApiFixtureMaker:
    env_var: str
    kwargs: dict

    def __call__(self, func: _ApiFixtureFunc):
        args = self.kwargs.copy()
        args.setdefault("name", func.__name__)

        @pytest.fixture(**args)
        def wrapped():
            host = getenv(self.env_var)

            if host:
                return httpx.Client(base_url=host, timeout=_HTTP_TIMEOUT)
            else:
                return func()

        return wrapped


# Function signature ___________________________________________________________
@overload
def api_fixture(
    f: _ApiFixtureFunc, *, env_var: str = ..., **kwargs
) -> _ApiFixtureFunc: ...

@overload
def api_fixture(
    f: None = ..., *, env_var: str = ..., **kwargs
) -> _ApiFixtureMaker: ...


# Function declaration _________________________________________________________
def api_fixture(
        f: Callable[[], httpx.Client] | None = None,
        *,
        env_var: str = "MIIA_HOST",
        **kwargs
):
    """
    Decorator to mark test server API Pytest fixtures.

    Allow alternating test runs between a local test server and a remotely
    deployed host (like in CI/CD runs).

    E.g.:
    ```
    from miia_test_utils.api_client import api_fixture

    @api_fixture
    def api():
        from fastapi.testclient import TestClient
        from main import app  # FastAPI app for the current repository
        return TestClient(app)
    ```
    """

    fixture_maker = _ApiFixtureMaker(env_var, deepcopy(kwargs))

    if f:
        return fixture_maker(f)
    else:
        return fixture_maker
