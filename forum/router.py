from typing import List, Union

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.base_config import current_user
from auth.models import User
from database import get_async_session
from forum.models import Post, Comment
from forum.schemas import PostRead, PostCreate, CommentCreate, OnePostRead

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
    return {"status": "post was created"}

@router.get("/my_posts", response_model=List[PostRead])
async def get_my_posts(user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(Post).where(Post.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/post/{post_id}")
async def get_post(post_id: int,
                   session: AsyncSession = Depends(get_async_session)) -> Union[OnePostRead, str]:
    query = select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
    result = await session.execute(query)
    post = result.scalars().first()
    if post:
        return post
    else:
        return f"There is no post with id {post_id}"

@router.get("/all_posts", response_model=List[PostRead])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    query = select(Post)
    result = await session.execute(query)
    return result.scalars().all()

@router.delete("/post/{post_id}")
async def delete_post(post_id: int,
                      user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    stmt = select(Post).where(Post.id == post_id, Post.user_id == user.id)
    result = await session.execute(stmt)
    if result.scalars().first():
        stmt = delete(Comment).where(Comment.post_id == post_id, Comment.user_id == user.id)
        await session.execute(stmt)
        stmt = delete(Post).where(Post.id == post_id, Post.user_id == user.id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "post was deleted"}
    else:
        return f"You don't have post with id {post_id}"

@router.post("/add_comment")
async def add_post(new_comment: CommentCreate,
                   user: User = Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    comment = insert(Comment).values(**new_comment.dict(), user_id=user.id)
    await session.execute(comment)
    await session.commit()
    return {"status": "comment was created"}