from aiogram.types import CallbackQuery
from Config import bot, dp, UserState
from Client.HelpFunctions import purchase_check
from HelloMessages.Client import rates_new, rates_existing
from aiogram.dispatcher import FSMContext
from SuperAdmin.PurchaseNotification import purchase_notification


@dp.callback_query_handler(lambda call: True, state=UserState.confirmation)
async def confirmation_handler(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    data = await state.get_data()
    term = data['term']
    month_word = data['month_word']
    price = data['price']
    workplace = data['workplace']

    if call.data == "yes":
        await purchase_notification(user_id, term, month_word, workplace, price)
        await bot.send_message(chat_id, "Сообщение об оплате отправлено администратору, ожидайте...")
        await state.finish()

    elif call.data == "no":
        user_purchased = await purchase_check(user_id)
        if user_purchased:
            await rates_existing(chat_id)
        else:
            await rates_new(chat_id)

    await bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

