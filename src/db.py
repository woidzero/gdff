from datetime import datetime
import logging
from typing import Any
import aiosqlite

import asyncio

logger = logging.getLogger("db")


class Database:
    def __init__(self, db_path: str = "gdff/users.sqlite3") -> None:
        self._db_path = db_path
        self._db = None
        self._schema = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT UNIQUE PRIMARY KEY, 
            name TEXT NOT NULL,
            category INT /* 1-talk; 2-host; 3-creator; 4-slayer; */,
            profile_details VARCHAR(1000),
            profile_picture TEXT,
            reg_timestamp BIGINT
        );"""

    @property
    def db(self) -> aiosqlite.Connection | None:
        return self._db

    async def setup(self) -> None:
        self._db = await aiosqlite.connect(self._db_path)
        await self._db.execute(self._schema)
        self._db.row_factory = aiosqlite.Row

    async def close(self) -> None:
        await self.db.close()

    async def fetch_user(self, user_id) -> dict[str, Any]:
        cur = await self.db.execute("SELECT * FROM `users` WHERE user_id = ?", user_id)
        row = await cur.fetchone()
        return {
            "user_id": row[0],
            "name": row[1],
            "category": row[2],
            "profile_details": row[3],
            "profile_picture": row[4],
            "reg_timestamp": row[5],
        }

    async def new_user(
        self, user_id: int, name: str, category: int, profile_details: str, profile_picture: str
    ) -> None:
        reg_timestamp = datetime.now().timestamp()

        await self.db.execute(
            "INSERT INTO `users` (user_id, name, category, profile_details, profile_picture, reg_timestamp) VALUES (?,?,?,?,?,?)",
            (user_id, name, category, profile_details, profile_picture, reg_timestamp),
        )
        await self.db.commit()

    async def edit_user(self, user_id: int, new_details: str) -> None:
        await self.db.execute(
            "UPDATE `users` SET profile_details = ? WHERE user_id = ? ", (new_details, user_id)
        )
        await self.db.commit()


db = Database()


async def test():
    print("setup")
    await db.setup()
    print(1)
    await db.new_user(1, "woidzero", 1, "kransiy svet", "none")
    print(1)


async def test1():
    user = await db.fetch_user(1)
    print(user)


try:
    asyncio.run(test1())
except Exception:
    asyncio.run(test())
    asyncio.run(test1())
