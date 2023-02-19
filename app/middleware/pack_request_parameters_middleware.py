import collections
import dataclasses
import json
import logging
from typing import ClassVar

import starlette
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, Request

logger = logging.getLogger(__name__)


async def get_request_body(request: Request) -> bytes:
    body = await request.body()

    request._receive = ReceiveProxy(receive=request.receive, cached_body=body)
    return body


async def get_request_json(request: Request) -> dict:
    body = await get_request_body(request)
    return json.loads(body)


@dataclasses.dataclass
class ReceiveProxy:
    """Proxy to starlette.types.Receive.__call__ with caching first receive call."""
    receive: starlette.types.Receive
    cached_body: bytes
    _is_first_call: ClassVar[bool] = True

    async def __call__(self):
        # First call will be for getting request body => returns cached result
        if self._is_first_call:
            self._is_first_call = False
            return {"type": "http.request", "body": self.cached_body, "more_body": False}

        return await self.receive()


class PackRequestParametersMiddleware(BaseHTTPMiddleware):
    """
    This is a middleware that packs the request parameters into the request object.
    Old name: SearchMiddleware
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """
        This is the main entry point for the middleware.
        param request: The request object.
        param call_next: This is the next function in the chain.
        :return: Response
        :rtype: starlette.Response
        """

        response = await self.pre_processing(request)
        if response.status_code == 200:
            # process the request and get the response
            response = await call_next(request)

        return response

    async def pre_processing(self, request: Request):
        """
        This is the pre-processing step for the middleware.
        param request: The request object.
        :return: request
        """

        consolidated_params = [request.query_params]

        if "application/json" in [
            request.headers.get("accept"),
            request.headers.get("content-type"),
        ]:
            try:
                json_data = await get_request_json(request)
                consolidated_params.append(json_data)

            except json.JSONDecodeError:
                request.state.REQUEST = collections.ChainMap(*consolidated_params)
                logger.error("Invalid JSON in request body", extra={"request": request})
                return Response("Bad JSON format", status_code=400)

        request.state.REQUEST = collections.ChainMap(*consolidated_params)
        return Response("OK", status_code=200)
