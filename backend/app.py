from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from schemas import Order, CreateOrder
from services import get_order_service, OrderService
import datetime


app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def error_exception_handler(request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code, 
        content={'error': exception.detail}
    )


@app.post("/api/new_order")
async def create_order(
    order_data: CreateOrder,
    order_service: OrderService = Depends(get_order_service)
):
    async with order_service.session.begin():
        return (await order_service.create(order_data=order_data))


@app.get("/api/orders")
async def get_orders(
    date: datetime.date = Query(
        None,
        alias="date",
        description=("date"),
    ),
    order_service: OrderService = Depends(get_order_service)
):
    async with order_service.session.begin():
        return (await order_service.get_orders_on_date(date=date))


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
    )