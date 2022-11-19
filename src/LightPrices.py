from sqlalchemy import Integer, JSON, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LightPrices(Base):
    __tablename__ = "precios_luz"
    day = Column("precios_hora", Integer, primary_key=True, nullable=False)
    day_prices = Column(JSON, nullable=True)

    def create(self, prices):
        self.day = list(prices.keys())[0]
        self.day_prices = list(prices.values())[0]
