from loader import dp, db
from filters import IsAdmin
from handlers.user.menu import settings
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery
from states import CategoryState
from hashlib import md5
from aiogram.dispatcher import FSMContext

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


@dp.callback_query_handler(IsAdmin(), text='add_category')
async def add_category_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Введіть назву категорії')
    await CategoryState.title.set()



@dp.message_handler(IsAdmin(), state=CategoryState.title)
async def set_category_title_handler(message: Message, state: FSMContext):

    category = message.text
    idx = md5(category.encode('utf-8')).hexdigest()
    db.query('INSERT INTO categories VALUES (?, ?)', (idx, category))

    await state.finish()
    await process_settings(message)

@dp.callback_query_handler(IsAdmin(), category_cb.filter(action='view'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict,
                                    state: FSMContext):
    category_idx = callback_data['id']

    products = db.fetchall('''SELECT * FROM products product
    WHERE product.tag = (SELECT title FROM categories WHERE idx=?)''',
                           (category_idx,))

    await query.message.delete()
    await query.answer('Усі додані товари до цієї категорії.')
    await state.update_data(category_index=category_idx)
    await show_products(query.message, products, category_idx)
