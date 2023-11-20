from loader import dp, db
from filters import IsAdmin
from handlers.user.menu import settings
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

category_cb = CallbackData('category', 'id', 'action')


@dp.message_handler(IsAdmin(), text=settings)
async def process_settings(message: Message):

    markup = InlineKeyboardMarkup()

    for idx, title in db.fetchall('SELECT * FROM categories'):

        markup.add(InlineKeyboardButton(
            title, callback_data=category_cb.new(id=idx, action='view')))

    markup.add(InlineKeyboardButton(
        '+ Додати категорію', callback_data='add_category'))

    await message.answer('Налаштування категорій:', reply_markup=markup)
