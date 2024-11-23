from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database_utils.models import Exchange
from starlette import status
from database_utils.utils import get_db
from schemas import Exchange as ExchangeSchema, ExchangeCreate

router = APIRouter(
    prefix='/exchanges',
    tags=['Exchanges']
)


@router.get("/", response_model=List[ExchangeSchema], status_code=status.HTTP_200_OK)
async def get_exchanges(db_session: AsyncSession = Depends(get_db)):
    result = await db_session.execute(select(Exchange))
    return result.scalars().all()


@router.get("/{exchange_id}", response_model=ExchangeSchema, status_code=status.HTTP_200_OK)
async def get_exchange_by_id(exchange_id: int, db_session: AsyncSession = Depends(get_db)):
    result = (await db_session.scalars(select(Exchange).where(Exchange.id == exchange_id))).first()
    if not result:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return result


@router.post("/", response_model=ExchangeSchema, status_code=status.HTTP_201_CREATED)
async def create_exchange(exchange: ExchangeCreate, db_session: AsyncSession = Depends(get_db)):
    new_exchange = Exchange(name=exchange.name)
    db_session.add(new_exchange)
    await db_session.commit()
    return new_exchange


@router.delete("/{exchange_id}", response_model=ExchangeSchema, status_code=status.HTTP_200_OK)
async def delete_exchange(exchange_id: int, db_session: AsyncSession = Depends(get_db)):
    exchange = await db_session.execute(select(Exchange).filter(Exchange.id == exchange_id))
    exchange = exchange.scalars().first()

    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")

    await db_session.delete(exchange)
    await db_session.commit()
    return exchange
