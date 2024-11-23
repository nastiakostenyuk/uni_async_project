from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

import uvicorn
from fastapi import FastAPI

import exchanges_endpoints
import orders_endpoints
from database_utils.utils import init_models, check_connection_to_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    """Run tasks before and after the server starts."""
    await check_connection_to_db()
    await init_models()
    yield


app = FastAPI(lifespan=lifespan, title="My orders")
app.include_router(exchanges_endpoints.router)
app.include_router(orders_endpoints.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
