from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.opt(exception=exc).error(
        "Unhandled exception on {method} {path}",
        method=request.method,
        path=request.url.path,
    )
    return JSONResponse(
        {"errors": ["Internal server error"]},
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
