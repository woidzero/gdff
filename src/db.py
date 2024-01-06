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
        logger.info("Starting database ...")

        self._db = await aiosqlite.connect(self._db_path)
        await self._db.execute(self._schema)
        self._db.row_factory = aiosqlite.Row

    async def close(self) -> None:
        await self._db.close()

    async def fetch_user(self, uid) -> dict[str, Any]:
        cur = await self._db.execute("SELECT * FROM `users` WHERE uID = ?", uid)
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
        self, uid, name: str, category: int, details: str, image: str
    ) -> None:
        regTime = datetime.now().timestamp()

        await self._db.execute(
            "INSERT INTO `users` (id, uID, name, category, details, image, regTime) VALUES (?,?,?,?,?,?)",
            (uid, name, category, details, image, regTime),
        )
        await self._db.commit()
        logger.info("user commited %s;%s;%s;%s" % (uid, name, details, image))

    async def edit_user(self, uid, new_details: str) -> None:
        await self._db.execute(
            "UPDATE `users` SET details = ? WHERE uid = ? ", (new_details, uid)
        )
        await self._db.commit()


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
