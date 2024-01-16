import logging

from sqlalchemy import select, update

from .base import Database, Int16, Int64
from .models import User


async def create_user(user_id: Int64, name: str) -> None:
    async with Database().session as session:
        if not (await session.execute(select(User.id).filter(User.id == user_id))).scalar():
            session.add(User(id=user_id, name=name))
            await session.commit()
            logging.info(f"Created new user: {name} <{user_id}>")


async def create_user_profile(user_id: int, category: Int16, description: str):
    async with Database().session as session:
        await session.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                {
                    User.category: category,
                    User.description: description,
                }
            )
        )
        await session.commit()
        logging.info(f"Created user profile: {user_id} ({category})")
