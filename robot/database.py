import asyncio
import os
import aiosqlite
from datetime import datetime


class DataBase:
    def __init__(self):
        self.path_to_db = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "../robot.db"
        )

    async def execute(
        self,
        sql: str,
        parameters: tuple = None,
        fetchone=False,
        fetchall=False,
        commit=False,
    ):
        async with aiosqlite.connect(self.path_to_db) as db:
            if not parameters:
                parameters = ()
            data = None
            cursor = await db.cursor()
            await cursor.execute(sql, parameters)

            if commit:
                await db.commit()

            if fetchone:
                data = await cursor.fetchone()
            if fetchall:
                data = await cursor.fetchall()
            # await cursor.close()
            # await db.close()
            return data

    async def create_table_robots(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Robot(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_with INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now','localtime')),
        stope_at TEXT DEFAULT NULL
        )
        """
        await self.execute(sql=sql, commit=True)

    async def add_robot_to_table(self, start_with: int):
        sql = """
        INSERT INTO Robot(start_with) VALUES (?)
        """

        await self.execute(sql=sql, parameters=(start_with,), commit=True)

    async def update_robot_in_table(self):
        sql = """
        UPDATE Robot SET stope_at = ? where id = (SELECT MAX(id) FROM Robot)
        """

        await self.execute(sql=sql, parameters=(datetime.now(),), commit=True)

    async def get_all_robots(self):
        sql = """
        SELECT * FROM Robot
        """
        return await self.execute(sql=sql, fetchall=True)


if __name__ == "__main__":
    db = DataBase()
    asyncio.run(db.update_robot_in_table())
    print("stop")
