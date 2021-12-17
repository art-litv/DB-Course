from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date

import random
from faker import Faker


fake = Faker()
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Integer)
    created_at = Column(Date)

    @classmethod
    def generate(cls):
        fake_data = {}
        fake_data["product_name"] = fake.hexify(
            text='^^:^^:^^:^^:^^:^^', upper=True)
        fake_data["price"] = random.randint(1, 100)
        fake_data["created_at"] = fake.date()
        return cls(**fake_data)

    def __repr__(self):
        return "<Product(product_id={}, product_name='{}', price={}, created_at='{}')>"\
            .format(self.product_id, self.product_name, self.price, self.created_at)


class Price(Base):
    __tablename__ = 'prices'
    price_id = Column(Integer, primary_key=True)
    price = Column(Integer)
    created_at = Column(Date)
    product_id = Column(Integer, ForeignKey("products.product_id"))

    @classmethod
    def generate(cls, session):
        fake_data = {}
        product_ids = session.query(Product).all()
        fake_data["price"] = random.randint(1, 100)
        fake_data["created_at"] = fake.date()
        fake_data["product_id"] = random.choice(product_ids)
        return cls(**fake_data)

    def __repr__(self):
        return "<Product(price_id={}, price={}, created_at='{}', product_id={})>"\
            .format(self.price_id, self.price, self.created_at, self.product_id)
