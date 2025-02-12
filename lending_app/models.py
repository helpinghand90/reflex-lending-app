from typing import List
import reflex as rx
import sqlalchemy

from datetime import datetime, timezone
from sqlmodel import Field, Relationship


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ChatSession(rx.Model, table=True):
    # id
    user_id: str = Field(default=None, nullable=False)
    messages: List["ChatSessionMessageModel"] = Relationship(back_populates="session")
    # todo: add user relationship , foreign_key='userdetailsmodel.user_id'
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    update_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )


class ChatSessionMessageModel(rx.Model, table=True):
    session_id: int = Field(default=None, foreign_key="chatsession.id")
    session: ChatSession = Relationship(back_populates="messages")
    content: str
    role: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )


class UserDetailsModel(rx.Model, table=True):
    # id
    user_id: str
    given_name: str
    family_name: str
    email: str
    picture: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        nullable=False,
    )
    update_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
        nullable=False,
    )
