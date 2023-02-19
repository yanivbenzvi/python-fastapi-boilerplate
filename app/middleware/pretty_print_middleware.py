import json

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response


class PrettyPrintMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: callable):
        """
        This is the main entry point for the middleware.
        Depends on GlobalParametersMiddleware
        param request: The request object.
        param call_next: This is the next function in the chain.
        :return: Response
        :rtype: starlette.Response
        """

        # process the request and get the response
        response = await call_next(request)

        response = await self.post_processing(response, request)

        return response

    async def post_processing(self, response: Response, request: Request):
        """
        This is the post-processing step for the middleware.
        param response: The response object.
        param request: The request object.
        :return: response
        """

        pretty_print = request.query_params.get("pretty")
        should_pretty_print = str(pretty_print).lower() in ["1", "true"]

        if should_pretty_print:

            response_body = await self.extract_body_from_response(response)

            body_dict = json.loads(response_body.decode("utf-8")) if response_body else {}
            body_str = json.dumps(body_dict, indent=4).encode("utf-8")
            headers = dict(response.headers)
            headers["content-length"] = str(len(body_str))

            return Response(
                content=body_str,
                status_code=response.status_code,
                headers=headers,
                media_type=response.media_type,
            )

        return response

    async def extract_body_from_response(self, response: Response):
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        return response_body
