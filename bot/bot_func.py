from aiogram import Router, F
from aiogram.types import Message

from db.db_intertactions import tablesList as show

from main import cursor as cur

import psycopg2

router = Router()


@router.message(F.text)
async def message_with_text(message: Message):
    await message.answer(show(cur))
