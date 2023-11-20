from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from aiogram import executor
from logging import basicConfig, INFO

from data.config import ADMINS
from loader import dp, db, bot
import handlers

user_message = 'Покупець'
admin_message = 'Адмін'



@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''👋 Привіт геймер! 🎮 

🤖 Я бот-магазин з продажу ігор будь-якогу жанру.

🛍️ Щоб перейти до каталогу ігор, скористайтесь командою /menu.

❓ Виникли питання? Не проблема! Команда /sos допоможе
зв'язатися з адмінами, які постараються якнайшвидше відгукнутися.
    ''', reply_markup=markup)


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in ADMINS:
        ADMINS.append(cid)

    await message.answer('Увімкнено адмінський режим.',
                         reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in ADMINS:
        ADMINS.remove(cid)

    await message.answer('Увімкнено режим покупця.',
                         reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    basicConfig(level=INFO)
    db.create_tables()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
