from filters import IsUser
from aiogram.types import Message
from aiogram.types import CallbackQuery

from .menu import catalog
from loader import dp, db
from keyboards.inline.categories import categories_markup, category_cb


@dp.message_handler(IsUser(), text=catalog)
async def process_catalog(message: Message):
    await message.answer('Виберіть розділ, щоб вивести список ігор:',
                         reply_markup=categories_markup())




@dp.callback_query_handler(IsUser(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict):

    products = db.fetchall('''SELECT * FROM products product
    WHERE product.tag = (SELECT title FROM categories WHERE idx=?) 
    AND product.idx NOT IN (SELECT idx FROM cart WHERE cid = ?)''',
                           (callback_data['id'], query.message.chat.id))

    await query.answer('Усі доступні ігри.')
    await show_products(query.message, products)
