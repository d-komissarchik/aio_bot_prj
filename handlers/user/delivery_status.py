from aiogram.types import Message
from loader import dp, db
from .menu import delivery_status
from filters import IsUser


@dp.message_handler(IsUser(), text=delivery_status)
async def process_delivery_status(message: Message):
    orders = db.fetchall('SELECT * FROM orders WHERE cid=?',
                         (message.chat.id,))


