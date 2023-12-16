from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message
from states import SosState
from filters import IsUser
from loader import dp, db


@dp.message_handler(commands='sos')
async def cmd_sos(message: Message):
    await SosState.question.set()
    await message.answer(
        "Опишіть якомога детальніше суть проблеми "
        "та адміністратор обов'язково вам відповість якнайшвидше",
        reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=SosState.question)
async def process_question(message: Message, state: FSMContext):
    async with state.proxy()as data:
        data['question'] = message.text
    await message.answer('Переконайтеся, що все правильно.',
                         reply_markup=submit_markup())
    await SosState.next()
