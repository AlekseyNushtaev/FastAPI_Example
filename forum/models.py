import datetime

from sqlalchemy import String, func, DateTime, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from auth.models import User
from database import Base


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    text: Mapped[str] = mapped_column(String(3000))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    comments: Mapped[list["Comment"]] = relationship()


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"), nullable=False, index=True)



