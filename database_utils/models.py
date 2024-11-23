from sqlalchemy import Float
from sqlalchemy import String, ForeignKey

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, Mapped, DeclarativeBase, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Exchange(Base):
    __tablename__ = "exchanges"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    orders = relationship("Order", back_populates="exchange")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    pair: Mapped[str] = mapped_column(String(10))
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"))
    take_profit: Mapped[float] = mapped_column(Float)
    stop_loss: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    pnl: Mapped[float] = mapped_column(Float)

    exchange = relationship("Exchange", back_populates="orders")
