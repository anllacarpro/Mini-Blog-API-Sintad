from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    posts = relationship("Post", back_populates="author", cascade="all,delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all,delete-orphan")
