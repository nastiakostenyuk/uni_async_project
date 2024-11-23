from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database_utils.models import Order, Exchange
from starlette import status
from database_utils.utils import get_db
from schemas import Order as OrdersSchema, OrderCreate

router = APIRouter(
    prefix='/orders',
    tags=['Orders']
)


@router.get("/", response_model=List[OrdersSchema], status_code=status.HTTP_200_OK)
async def get_orders(db_session: AsyncSession = Depends(get_db)):
    result = await db_session.execute(select(Order))
    return result.scalars().all()


@router.get("/{order_id}", response_model=OrdersSchema, status_code=status.HTTP_200_OK)
async def get_order_by_id(order_id: int, db_session: AsyncSession = Depends(get_db)):
    result = (await db_session.scalars(select(Order).where(Order.id == order_id))).first()
    if not result:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return result


@router.post("/", response_model=OrdersSchema, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db_session: AsyncSession = Depends(get_db)):
    exchange = (await db_session.scalars(select(Exchange).where(Exchange.id == order.exchange_id))).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    new_exchange = Order(pair=order.pair,
                         exchange_id=order.exchange_id,
                         take_profit=order.take_profit,
                         stop_loss=order.stop_loss,
                         price=order.price,
                         pnl=order.pnl
                         )
    db_session.add(new_exchange)
    await db_session.commit()
    return new_exchange


@router.delete("/{order_id}", response_model=OrdersSchema, status_code=status.HTTP_200_OK)
async def delete_order(order_id: int, db_session: AsyncSession = Depends(get_db)):
    exchange = await db_session.execute(select(Order).filter(Order.id == order_id))
    exchange = exchange.scalars().first()

    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    await db_session.delete(exchange)
    await db_session.commit()
    return exchange
