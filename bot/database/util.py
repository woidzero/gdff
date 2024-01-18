from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class SingletonMeta(type):
    _instance: Optional["SingletonMeta"] = None

    def __call__(cls, *args: Any, **kwargs: Any) -> Optional["SingletonMeta"]:
        if cls._instance:
            return cls._instance
        cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )
