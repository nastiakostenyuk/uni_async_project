import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()


# Database settings
db_url = URL.create(
    drivername=os.getenv("DB_DRIVER", "postgresql+asyncpg"),
    username=os.getenv("DB_USER", os.getenv("DB_USER", "postgres")),
    password=os.getenv("DB_PASSWORD", os.getenv("DB_PASSWORD", "postgres")),
    host=os.getenv("DB_HOST", os.getenv("DB_HOST", "localhost")),
    port=int(os.getenv("DB_PORT", os.getenv("DB_PORT", "5432"))),
    database=os.getenv("DB_NAME", os.getenv("DB_NAME", "my_orders")),
)

async_engine = create_async_engine(db_url)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
