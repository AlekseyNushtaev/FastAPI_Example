from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    text: str

class PostRead(PostCreate):
    id: int
    created_at: datetime
    user_id: int

class CommentCreate(BaseModel):
    post_id: int
    text: str

class CommentRead(CommentCreate):
    id: int
    post_id: int
    text: str
    created_at: datetime



