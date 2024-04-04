import asyncio
import argparse
from typing import Optional
from asyncio import Task

from database import DataBase


db = DataBase()


class Robot:
    """Робот – это Python-скрипт.
    Его задача: каждую секунду выводить в консоль цифры от 0 и далее,
    прибавляя по единице, пока выполнение скрипта не будет прервано.
    Робот работает асинхронно.
    """

    def __init__(self, start_with: int = 0) -> None:
        """Инициализатор класса

        Args:
            start_with (int): начало отсчета (по умолчанию – с нуля)
            current (int): текущее значение
            is_running (bool): состояние робота
            script_task (Task) : задача робота
        """
        self.start_with: int = start_with
        self.current: int = start_with
        self.is_running: bool = False
        self.script_task: Optional[Task] = None

    async def start(self) -> None:
        """Запуск робота"""
        self.is_running: bool = True
        self.script_task: Task = asyncio.create_task(self.robot(), name="script_task")
        await db.create_table_robots()
        await db.add_robot_to_table(self.start_with)
        await self.script_task

    async def stop(self) -> None:
        """Остановка робота"""
        self.is_running: bool = False
        if self.script_task:
            await asyncio.wait([self.script_task], timeout=10)

    async def __show(self) -> None:
        """выводит в консоль цифры от 0 и далее,
        прибавляя по единице
        """
        await asyncio.sleep(1)
        print(self.current)
        self.current += 1

    async def robot(self) -> None:
        """Каждую секунду выводить в консоль цифры от 0 и далее,
        прибавляя по единице, пока выполнение скрипта не будет прервано
        """
        while self.is_running:
            await self.__show()

    def status(self) -> None:
        """Вывод состояния робота"""
        is_running = "запущен" if self.is_running else "остановлен"
        print(
            f"""Робот {is_running}\n
            Текущее значение - {self.start_with}"""
        )

    async def show_all_robots(self) -> None:
        """Вывод времени работы роботов"""
        robots = await db.get_all_robots()
        print(robots)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Робот – это Python-скрипт",
        description="""Его задача: каждую секунду выводить в консоль цифры от 0 и далее,
    прибавляя по единице, пока выполнение скрипта не будет прервано.
    Робот работает асинхронно.""",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="для изменения начала отсчета необходимо задать параметр start_with (int)",
    )
    parser.add_argument(
        "-sw",
        "--start_with",
        type=int,
        default=0,
        help="начало отсчета (по умолчанию – с нуля)",
    )
    args = parser.parse_args()
    robot = Robot(args.start_with)
    try:
        print("start")
        asyncio.run(robot.start())
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.run(db.update_robot_in_table())
        print("stop")
