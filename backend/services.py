from functools import lru_cache
import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import get_async_session
from models import Order, Executor
from schemas import (
    CreateOrder,
    Order as OrderSchema,
)


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, order_data: CreateOrder):
        executors = (await self.session.scalars(
            select(Executor).options(
                selectinload(Executor.orders)
            ).filter(
                ~Executor.orders.any(Order.start_datetime == order_data.start_datetime)
            )
        )).all()
        if executors:
            executors.sort(key=lambda x: len(x.orders))
            new_order = Order(
                flat=order_data.flat,
                breed=order_data.breed,
                dog_name=order_data.dog_name,
                start_datetime=order_data.start_datetime,
                executor_id=executors[0].id
            )
            self.session.add(new_order)
            await self.session.flush()
            return OrderSchema(
                id=new_order.id,
                flat=new_order.flat,
                breed=new_order.breed,
                dog_name=new_order.dog_name,
                start_datetime=new_order.start_datetime,
                executor=new_order.executor.name,
            )
        else:
            raise HTTPException(
                status_code=400,
                detail='Нет свободных исполнителей.'
            )
        
    async def get_orders_on_date(self, date: datetime.date | None):
        query = select(Order).options(
            selectinload(Order.executor)
        )
        if date:
            query = query.filter(
                func.date(Order.start_datetime) == date
            )
        orders = (await self.session.scalars(query)).all()
        return [OrderSchema(
            id=order.id,
            flat=order.flat,
            breed=order.breed,
            dog_name=order.dog_name,
            start_datetime=order.start_datetime,
            executor=order.executor.name,
        ) for order in orders]


@lru_cache()
def get_order_service(
    session: AsyncSession = Depends(get_async_session),
) -> OrderService:
    return OrderService(session)