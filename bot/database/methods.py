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
                    User.is_registered: True,
                }
            )
        )
        await session.commit()
        logger.info(f"Created user profile: <{user_id}> {name}")


async def delete_user_profile(user_id: int) -> None:
    async with Database().session as session:
        await session.execute(
            update(User).where(User.id == user_id).values({User.is_registered: False})
        )
        await session.commit()
        logger.info(f"Deleted user profile: <{user_id}>")


async def get_user(user_id: int) -> User:
    async with Database().session as session:
        return (await session.execute(select(User).where(User.id == user_id))).scalar()


async def get_random_user_id(exclude_user_id: int) -> int:
    async with Database().session as session:
        return (
            await session.execute(
                select(User.id)
                .where(User.id != exclude_user_id, User.is_registered == 1)
                .order_by(func.random())
                .limit(1)
            )
        ).scalar()


async def is_registered_user(user_id: int) -> bool:
    async with Database().session as session:
        return (
            await session.execute(select(User.is_registered).where(User.id == user_id))
        ).scalar()
