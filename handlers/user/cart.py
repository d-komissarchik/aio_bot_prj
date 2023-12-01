from filters import IsUser
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types.chat import ChatActions
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import CallbackQuery

from loader import db, dp, bot
from .menu import cart
from keyboards.inline.products_from_cart import product_markup
from keyboards.inline.products_from_catalog import product_cb
from states import CheckoutState
from keyboards.default.markups import *


@dp.message_handler(IsUser(), text=cart)
async def process_cart(message: Message, state: FSMContext):
    cart_data = db.fetchall(
        'SELECT * FROM cart WHERE cid=?', (message.chat.id,))
    if len(cart_data) == 0:
        await message.answer('Ваш кошик порожній.')
    else:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        async with state.proxy() as data:
            data['products'] = {}
        order_cost = 0
        for _, idx, count_in_cart in cart_data:
            product = db.fetchone('SELECT * FROM products WHERE idx=?', (idx,))
            if product == None:
                db.query('DELETE FROM cart WHERE idx=?', (idx,))
            else:
                _, title, body, image, price, _ = product
                order_cost += price
                async with state.proxy() as data:
                    data['products'][idx] = [title, price, count_in_cart]
                markup = product_markup(idx, count_in_cart)
                text = f'<b>{title}</b>\n\n{body}\n\n Ціна: {price} гривень.'
                await message.answer_photo(photo=image,
                                           caption=text,
                                           reply_markup=markup)
        if order_cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('📦 Оформити замовлення')
            await message.answer('Перейти до оформлення?',
                                 reply_markup=markup)


@dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict,
                                   state: FSMContext):
    idx = callback_data['id']
    action = callback_data['action']

    if 'count' == action:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await process_cart(query.message, state)
            else:
                await query.answer('Кількість - ' + data['products'][idx][2])
    else:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await process_cart(query.message, state)
            else:
                data['products'][idx][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][idx][2]
                if count_in_cart == 0:
                    db.query('''DELETE FROM cart
                    WHERE cid = ? AND idx = ?''', (query.message.chat.id, idx))
                    await query.message.delete()
                else:
                    db.query('''UPDATE cart 
                    SET quantity = ? 
                    WHERE cid = ? AND idx = ?''',
                             (count_in_cart, query.message.chat.id, idx))
                    await query.message.edit_reply_markup(
                        product_markup(idx, count_in_cart))



@dp.message_handler(IsUser(), text='📦 Оформити замовлення')
async def process_checkout(message: Message, state: FSMContext):

    await CheckoutState.check_cart.set()
    await checkout(message, state)

async def checkout(message, state):
    answer = ''
    total_price = 0

    async with state.proxy() as data:
        for title, price, count_in_cart in data['products'].values():
            tp = count_in_cart * price
            answer += f'<b>{title}</b> * {count_in_cart}шт. = {tp}грн\n'
            total_price += tp
    await message.answer(f'{answer}\nЗагальна сума замовлення: {total_price}грн.',
                         reply_markup=check_markup())
