from typing import Callable

from app.main import app


def get_routes() -> dict[str, str]:
    """Getting dict of paths of app."""

    routes = {}
    for route in app.routes:
        routes[route.endpoint.__name__] = route.path
    return routes


def reverse(
    func: Callable,
    routes: dict[str, str] = get_routes(),
    **kwargs
) -> str:
    """Getting url from routes."""

    path = routes[func.__name__]
    return path.format(**kwargs)
