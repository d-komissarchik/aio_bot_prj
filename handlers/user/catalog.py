from filters import IsUser
from aiogram.types import Message

from keyboards.inline.categories import categories_markup
from .menu import catalog
from loader import dp


@dp.message_handler(IsUser(), text=catalog)
async def process_catalog(message: Message):
    await message.answer('Виберіть розділ, щоб вивести список ігор:',
                         reply_markup=categories_markup())
