from pydantic import BaseModel


class Exchange(BaseModel):
    id: int
    name: str


class ExchangeCreate(BaseModel):
    name: str


class Order(BaseModel):
    id: int
    pair: str
    take_profit: float
    stop_loss: float
    price: float
    pnl: float
    exchange_id: int


class OrderCreate(BaseModel):
    pair: str
    take_profit: float
    stop_loss: float
    price: float
    pnl: float
    exchange_id: int
