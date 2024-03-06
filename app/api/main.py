from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from api.middlewares.http_request_middleware import HttpRequestMiddleware
from api.routers import stocks, sales

app = FastAPI()
app.add_middleware(HttpRequestMiddleware)
app.include_router(stocks.router)
app.include_router(sales.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"message": "ERROR"}),
    )
