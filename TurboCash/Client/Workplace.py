from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from Config import dp, UserState
from HelloMessages.Client import confirmation
from Client.HelpFunctions import get_workplace_word


@dp.message_handler(state=UserState.workplace)
async def workplace_handler(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    if message.text.isdigit():
        workplace = int(message.text)
        workplace_word = await get_workplace_word(workplace)
        data = await state.get_data()
        term = data['term']
        month_word = data['month_word']
        price = data['price']

        if workplace < 2:
            updated_price = price
        elif workplace >= 2:
            updated_price = price + (workplace-1) * 2000

        await state.update_data(workplace=workplace, price=updated_price)
        await confirmation(chat_id, term, month_word, workplace, workplace_word, updated_price)
    else:
        await message.answer("Введите число рабочих мест")


import Client.Confirmation
