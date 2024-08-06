from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from Config import dp, UserState
from HelloMessages.Client import rates_new
from Client.HelpFunctions import add_fullname


@dp.message_handler(state=UserState.full_name)
async def fullname_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    user_id = message.from_user.id
    full_name = message.text

    await add_fullname(user_id, full_name)
    await state.finish()
    await rates_new(chat_id)

import Client.Rates
