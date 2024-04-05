from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from forum.models import Post
from forum.schemas import PostRead, PostCreate

router = APIRouter(
    prefix="/forum",
    tags=["Forum"]
)

@router.post("/post")
async def add_post(new_post: PostCreate,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    post = insert(Post).values(**new_post.dict(), user_id=user.id)
    await session.execute(post)
    await session.commit()
    return {"status": "ok"}

@router.get("/my_posts", response_model=List[PostRead])
async def get_posts(user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/all_posts", response_model=List[PostRead])
async def get_posts(session: AsyncSession = Depends(get_async_session)):
    query = select(Post)
    result = await session.execute(query)
    return result.scalars().all()

