from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from database import create_tables


# from operations.router import router as router_operation


@asynccontextmanager
async def lifespan(app: FastAPI):
   await create_tables()
   yield

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
