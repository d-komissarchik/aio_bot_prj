from filters import IsUser
from aiogram.types import Message, CallbackQuery
from aiogram.types.chat import ChatActions

from .menu import catalog
from loader import dp, db, bot
from keyboards.inline.categories import categories_markup, category_cb
from keyboards.inline.products_from_catalog import product_markup
from keyboards.inline.products_from_catalog import product_cb


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


async def show_products(m, products):
    if len(products) == 0:
        await m.answer('Тут нічого нема 😢')
    else:
        await bot.send_chat_action(m.chat.id, ChatActions.TYPING)
        for idx, title, body, image, price, _ in products:
            markup = product_markup(idx, price)
            text = f'<b>{title}</b>\n\n{body}'
            await m.answer_photo(photo=image,
                                 caption=text,
                                 reply_markup=markup)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='add'))
async def add_product_callback_handler(query: CallbackQuery,
                                       callback_data: dict):
    db.query('INSERT INTO cart VALUES (?, ?, 1)',
             (query.message.chat.id, callback_data['id']))

    await query.answer('Товар доданий до кошика!')
    await query.message.delete()

