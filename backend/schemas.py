from pydantic import BaseModel
import datetime


class CreateOrder(BaseModel):
    flat: int
    breed: str
    dog_name: str
    start_datetime: datetime.datetime


class Order(BaseModel):
    id: int
    flat: int
    breed: str
    dog_name: str
    start_datetime: datetime.datetime
    executor: str


