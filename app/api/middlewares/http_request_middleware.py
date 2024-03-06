import traceback
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class InvalidParamException(Exception):
    # デフォルトを400エラーとする
    default_status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        msg: str = "ERROR",
        status_code: int = default_status_code,
    ) -> None:
        self.status_code = status_code
        self.detail = {"message": msg}


class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response: Response = await call_next(request)
        except InvalidParamException as ipe:
            # カスタム例外
            response = JSONResponse(ipe.detail, status_code=ipe.status_code)

        return response