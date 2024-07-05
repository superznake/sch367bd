import asyncio
import sys

import logging
import psycopg2
from psycopg2 import Error

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db.db_intertactions import tablesList as show

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

TOKEN = "5657714150:AAGrv8nkIAq-F_miQu3ORY6vON76yUqJYII"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
cursor: psycopg2._psycopg.cursor
router = Router()


@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer(show(cursor))


async def main():
    try:
        # Подключение к существующей базе данных
        # TODO: заменить юзера на ентер юзернаме и с дб тож самое
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password=input("enter the password:\n"),
                                      host="localhost",
                                      port="5432",
                                      database="test")

        # Курсор для выполнения операций с базой данных
        global cursor
        cursor = connection.cursor()
        # Распечатать сведения о PostgreSQL
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")
        # Получить результат
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
        # show(cursor)
        dp = Dispatcher()
        dp.include_routers(router)
        await dp.start_polling(bot)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

if __name__ == "__main__":
    asyncio.run(main())
