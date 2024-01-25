import logging

from sqlalchemy import func, select, update

from .base import Database, Int64
from .models import User

logger = logging.getLogger(name=__name__)


async def create_user(user_id: Int64, name: str) -> None:
    async with Database().session as session:
        if not (await session.execute(select(User.id).where(User.id == user_id))).scalar():
            session.add(User(id=user_id, name=name))
            await session.commit()
            logger.info(f"Created new user: <{user_id}> {name} ")


async def create_user_profile(user_id: int, name: str, category_id: int, description: str) -> None:
    async with Database().session as session:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                {
                    User.name: name,
                    User.category: category_id,
                    User.description: description,
                }
            )
        )
        await session.commit()
        logger.info(f"Created user profile: <{user_id}> {name}")


async def get_user(user_id: int) -> User:
    async with Database().session as session:
        return (await session.execute(select(User).where(User.id == user_id))).scalar()


async def get_random_user_id(exclude_user_id: int) -> int:
    async with Database().session as session:
        return (
            await session.execute(
                select(User.id).where(User.id != exclude_user_id).order_by(func.random()).limit(1)
            )
        ).scalar()
