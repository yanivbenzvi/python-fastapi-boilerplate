from app.config import settings

from app.middleware.pack_request_parameters_middleware import PackRequestParametersMiddleware
from app.middleware.pretty_print_middleware import PrettyPrintMiddleware


def init_middlewares(app):
    middlewares = [
        dict(
            middleware_name=PackRequestParametersMiddleware,
            is_enabled=settings.feature_flags.pack_request_parameters
        ),
        dict(
            middleware_name=PrettyPrintMiddleware,
            is_enabled=settings.feature_flags.pretty_print
        ),
    ]

    for middleware in middlewares[::-1]:
        if middleware.get("is_enabled", True):
            app.add_middleware(middleware["middleware_name"])
