from datetime import datetime
from pydantic import BaseModel, validator


class ConsumerGoods(BaseModel):
    id: int
    name: str
    created_at: datetime
    price: int

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value.length > 0:
            raise ValueError('name must not be an empty string')
        return value

    @validator('price')
    def price_must_be_positive(cls, value):
        if not value > 0:
            raise ValueError('price must be positive')
        return value


class Sales(BaseModel):
    id: int
    sales_count: int
    consumer_goods_id: int

    @validator('sales_count')
    def sales_count_must_be_positive(cls, value):
        if not value > 0:
            raise ValueError('sales count must be positive')
        return value
