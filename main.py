import asyncio
import sys

import logging
import psycopg2
from aiogram.filters import Command
from psycopg2 import Error

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from db.db_intertactions import tablesList as show
from db.db_intertactions import cartridge_seek as cabs
from db.db_intertactions import cartridge_replace as cabr
from db.db_intertactions import cab_list as cabl
from bot import comms as comms

import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv('PORT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DBNAME = os.getenv('DBNAME')
TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
cursor: psycopg2._psycopg.cursor
router = Router()


@router.message(F.text.lower().startswith(comms.seek))
async def message_with_text(message: Message):
    tos = message.text.lower()[len(comms.seek):]
    await message.answer(cabs(cursor, tos))


@router.message(F.text.lower().startswith(comms.replace))
async def message_with_text(message: Message):
    tor = message.text.lower()[len(comms.replace):]
    await message.answer(cabr(cursor, tor))


@router.message(F.text.lower().startswith(comms.cabs))
async def message_with_text(message: Message):
    await message.answer(cabl(cursor))


@router.message(Command("start"))
async def cmd_start(message: Message):
    result = ("""Доступные команды:\n"""
            + "- " + comms.cabs + "\nсписок названий кабинетов\n"
            + "- " + comms.seek + "[название кабинета]\nдает название картриджа в данном кабинете\n"
            + "- " + comms.replace + "[название кабинета]\nустанавливает дату замены картриджа в данном кабинете")
    await message.answer(result)


@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer(show(cursor))


async def main():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host="localhost",
                                      port=PORT,
                                      database=DBNAME)

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
