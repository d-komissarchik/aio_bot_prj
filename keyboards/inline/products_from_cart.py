from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

product_cb = CallbackData('product', 'id', 'action')


def product_markup(idx, count):
    global product_cb

    markup = InlineKeyboardMarkup()

    back_btn = InlineKeyboardButton('⬅️', callback_data=product_cb.new(id=idx,
                                                                       action='decrease'))


