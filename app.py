from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from loader import dp

user_message = 'Користувач'
admin_message = 'Адмін'


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer('''Вітання! 👋

🤖 Я бот-магазин з продажу товарів будь-якої категорії.

🛍️ Щоб перейти до каталогу і вибрати сподобалися
товари скористайтесь командою /menu.

❓ Виникли питання? Не проблема! Команда /sos допоможе
зв'язатися з адмінами, які постараються якнайшвидше відгукнутися.
    ''', reply_markup=markup)
