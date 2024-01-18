from __future__ import annotations

from aiogram import html
from aiogram.utils.link import create_tg_link
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ..enums import Locale
from .base import Base, Int16, Int64
from .util import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(length=50))
    category: Mapped[Int16] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(String(length=1000), nullable=True)
    locale: Mapped[str] = mapped_column(String(length=2), default=Locale.DEFAULT)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
