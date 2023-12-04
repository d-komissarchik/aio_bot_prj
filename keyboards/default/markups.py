from aiogram.types import ReplyKeyboardMarkup

back_message = '👈 Назад'
all_right_message = '✅ Все вірно'
cancel_message = '🚫 Скасувати'
confirm_message = '✅ Підтвердити замовлення'


def back_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message)
    return markup


def check_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, all_right_message)
    return markup


def confirm_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(confirm_message)
    markup.add(back_message)
    return markup