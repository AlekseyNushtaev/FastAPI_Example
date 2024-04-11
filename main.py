from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from config import REDIS_HOST, REDIS_PORT
from database import create_tables
from forum.router import router as router_forum


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
   FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
   yield
   await redis.close()

app = FastAPI(
    title="Forum",
    lifespan=lifespan
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    router_forum
)
