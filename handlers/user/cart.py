from filters import IsUser
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.types.chat import ChatActions
from aiogram.types import ReplyKeyboardMarkup

from loader import db, dp, bot
from .menu import cart
from keyboards.inline.products_from_cart import product_markup


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
