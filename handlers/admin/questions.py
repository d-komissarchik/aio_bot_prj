from handlers.user.menu import questions
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from keyboards.default.markups import all_right_message, cancel_message, submit_markup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.types.chat import ChatActions

from loader import dp, db, bot
from filters import IsAdmin
from states import AnswerState

question_cb = CallbackData('question', 'cid', 'action')

@dp.message_handler(IsAdmin(), text=questions)
async def process_questions(message: Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    questions = db.fetchall('SELECT * FROM questions')
    if len(questions) == 0:
        await message.answer('Немає питань.')
    else:
        for cid, question in questions:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(
                'Відповісти',
                callback_data=question_cb.new(cid=cid, action='answer')))
            await message.answer(question, reply_markup=markup)


@dp.callback_query_handler(IsAdmin(), question_cb.filter(action='answer'))
async def process_answer(query: CallbackQuery, callback_data: dict,
                         state: FSMContext):
    async with state.proxy() as data:
        data['cid'] = callback_data['cid']
    await query.message.answer('Напиши відповідь.',
                               reply_markup=ReplyKeyboardRemove())
    await AnswerState.answer.set()


@dp.message_handler(IsAdmin(), state=AnswerState.answer)
async def process_submit(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
    await AnswerState.next()
    await message.answer('Переконайтеся, що ви не помилилися у відповіді.',
                         reply_markup=submit_markup())

