from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime
from sqlalchemy import ForeignKey
from database import Base


class Prompt(Base):

    __tablename__ = "prompts"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    title = Column(
        String,
        nullable=False
    )


    content = Column(
        String,
        nullable=False
    )


    category = Column(
        String,
        nullable=False
    )


    favorite = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
    Integer,
    ForeignKey("users.id")
)


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String,
        unique=True,
        nullable=False
    )


    password_hash = Column(
        String,
        nullable=False
    )


    