from aiogram.types import Message, ReplyKeyboardMarkup
from loader import dp
from filters import IsAdmin, IsUser

catalog = '🛍️ Каталог'
cart = '🛒 Кошик'
delivery_status = '🚚 Статус замовлення'

settings = '⚙️ Налаштування каталогу'
orders = '🚚 Замовлення'
questions = '❓ Запитання'


@dp.message_handler(IsAdmin(), commands='menu')
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)

    await message.answer('Меню', reply_markup=markup)


@dp.message_handler(IsUser(), commands='menu')
async def user_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(cart)
    markup.add(delivery_status)

    await message.answer('Меню', reply_markup=markup)
