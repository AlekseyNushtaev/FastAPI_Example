from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    text: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class PostRead(PostCreate):
    id: int
    created_at: datetime
    user_id: int


class CommentCreate(BaseModel):
    post_id: int
    text: str


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class CommentRead(CommentCreate):
    id: int
    post_id: int
    text: str
    created_at: datetime


class OnePostRead(PostRead):
    comments: List[CommentRead]
