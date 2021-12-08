from pydantic import BaseModel


class Model(BaseModel):
    @classmethod
    def from_tuple(cls, data):
        return [cls(**{key: data[i] for i, key in enumerate(
                cls.__fields__.keys())})][0]


class Product(Model):
    __name__ = 'product'
    __table__ = "products"
    id: int
    product_name: str
    price: int
    created_at: str


class Price(Model):
    __name__ = 'price'
    __table__ = "prices"
    id: int
    price: int
    created_at: str
    product_id: int
