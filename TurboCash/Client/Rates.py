from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from Config import bot, dp, UserState
from HelloMessages.Client import workplace


@dp.callback_query_handler(lambda call: True, state=UserState.rates)
async def rates_handler(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id

    if call.data == "1_month":
        term = 1
        price = 10000*term
        month_word = "месяц"
        await state.update_data(month_word=month_word, term=term, price=price)
        await workplace(chat_id)

    elif call.data == "3_months":
        term = 3
        price = 10000*term
        month_word = "месяца"
        await state.update_data(month_word=month_word, term=term, price=price)
        await workplace(chat_id)

    elif call.data == "6_months":
        term = 6
        price = 10000*term
        month_word = "месяцев"
        await state.update_data(month_word=month_word, term=term, price=price)
        await workplace(chat_id)

    elif call.data == "12_months":
        term = 12
        price = 100000
        month_word = "месяцев"
        await state.update_data(month_word=month_word, term=term, price=price)
        await workplace(chat_id)

    await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

import Client.Workplace
