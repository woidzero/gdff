import asyncio
import contextlib
import logging
from datetime import datetime
from typing import Any, Optional, Tuple

import aiosqlite
from config import Config

logger = logging.getLogger("db")
logger.setLevel(logging.DEBUG)


class Database:
    def __init__(self) -> None:
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> None:
        with contextlib.suppress(aiosqlite.Error):
            self.conn = await aiosqlite.connect(Config.DB_FILE)

    @property
    def is_connected(self) -> bool:
        return self.conn is not None

    @staticmethod
    async def _fetch(cursor, mode="one") -> Optional[Any]:
        if mode == "one":
            return await cursor.fetchone()
        if mode == "many":
            return await cursor.fetchmany()
        if mode == "all":
            return await cursor.fetchall()

        return None

    async def execute(self, query: str, values: Tuple = (), *, fetch: str = "one") -> Optional[Any]:
        cursor = await self.conn.cursor()

        await cursor.execute(query, values)
        data = await self._fetch(cursor, fetch)
        await self.conn.commit()

        await cursor.close()
        return data


DB: Database = Database()


async def create_db() -> None:
    await DB.execute(
        """CREATE TABLE IF NOT EXISTS users (
            userID INT UNIQUE PRIMARY KEY,
            fullName TEXT,
            category INT /* 1-talk; 2-host; 3-creator; 4-slayer; */,
            userDetails VARCHAR(1000),
            userPicture TEXT,
            regTime BIGINT
        );"""
    )
    logger.info("db created")


async def new_user(
    user_id: int,
    full_name: str,
    category: int,
    user_details: str,
    user_picture: str,
    reg_time: float = datetime.now().timestamp(),
) -> None:
    await DB.execute(
        "INSERT INTO users (userID, fullName, category, userDetails, userPicture, regTime) VALUES (?,?,?,?,?,?)",
        (user_id, full_name, category, user_details, user_picture, reg_time),
    )


async def get_user(user_id: int) -> dict[str, Any]:
    row = await DB.execute("SELECT * FROM users WHERE userID = ?", (user_id,), fetch="one")
    return {
        "user_id": row[0],
        "full_name": row[1],
        "category": row[2],
        "user_details": row[3],
        "user_picture": row[4],
        "reg_time": row[5],
    }


async def edit_user(user_id: int, key: str, value: str) -> None:
    await DB.execute(
        "UPDATE users SET ? = ? WHERE userID = ?",
        (key, value, user_id),
    )


# test suite
#
async def test() -> None:
    await DB.connect()

    if not DB.is_connected:
        raise logger.error("Database isn't connected")

    await create_db()
    logger.info("Database created")

    await new_user(1, "woidzero", 1, "kransiy svet", "none")
    print("user created")
    user = await get_user(1)
    print(user)


if __name__ == "__main__":
    asyncio.run(test())

# todo: remove public variables
asyncio.run(DB.connect())
if not DB.is_connected:
    raise logger.error("Database isn't connected")

asyncio.run(create_db())
