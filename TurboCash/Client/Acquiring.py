#функция отправки инвойса, нужно переместить в HM/Client
async def payment(chat_id, user_id, term, month_word, workplace, workplace_word, price):
    await UserState.payment.set()

    title = "Лицензия Turbocash"
    description = f"Подписка на срок {term} {month_word} на {workplace} {workplace_word}"
    current_order_number = await get_current_order_number(user_id)
    order_number = current_order_number + 1
    payload = f"{user_id}-{order_number}"

    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=payment_token,
        currency='RUB',
        prices=[LabeledPrice(label="Лицензия", amount=price)]#домножить на сто
    )


#нужно заменить на настоящий в Config
payment_token = '381764678:TEST:86937'


#получение текущего номера заказа для пейлоуда Client/HelpFunctions
async def get_current_order_number(user_id):
    async with DB() as conn:
        current_order_number = await conn.fetchval('SELECT order_number FROM client WHERE ID = $1', user_id)
    return current_order_number


#обработчики платежа Client/Payment
@dp.pre_checkout_query_handler(lambda query: True, state=UserState.payment)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT, state=UserState.payment)
async def process_successful_payment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id

    data = await state.get_data()
    term = data['term']
    month_word = data['month_word']
    workplace = data['workplace']
    price = data['price']

    keys = await workplaces_keys(workplace)

    await save_order(user_id, term, workplace, price, keys)
    await thank_you(chat_id, term, month_word, workplace, keys)
    await purchase_notification(user_id, term, month_word, workplace, price)


#этап перед отправкой инвойса
async def confirmation(chat_id, term, month_word, workplace, price):
    formatted_price = "{:,}".format(price).replace(',', ' ')
    text = f"Срок: {term} {month_word}\nКоличество рабочих мест: {workplace}\nОбщая сумма: {formatted_price}₽\n\nПодтвердите или отмените покупку"
    kb = confirmation_kb
    await UserState.confirmation.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


#дополнительный скрипт подтверждения
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from Config import dp, UserState
from Client.HelpFunctions import exists_check, get_workplace_word
from HelloMessages.Client import rates_new, rates_existing


@dp.callback_query_handler(lambda call: True, state=UserState.confirmation)
async def confirmation_handler(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if call.data == "yes":
        data = await state.get_data()
        term = data['term']
        month_word = data['month_word']
        workplace = data['workplace']
        workplace_word = await get_workplace_word(workplace)
        price = data['price']
        await payment(chat_id, term, month_word, workplace, workplace_word, price)

    elif call.data == "no":
        user_exists = await exists_check(user_id)
        if user_exists:
            await rates_existing(chat_id)
        else:
            await rates_new(chat_id)


import Client.Payment


#скрипт для уведомления админов
from Config import bot, DB


async def get_admins():
    async with DB() as conn:
        rows = await conn.fetch("SELECT id FROM user_settings WHERE role = 'admin'")
    admin_ids = [row['id'] for row in rows]
    return admin_ids


async def get_user_info(user_id):
    async with DB() as conn:
        full_name = await conn.fetchval('SELECT full_name FROM client WHERE ID = $1', user_id)
        contact = await conn.fetchval('SELECT contact FROM client WHERE ID = $1', user_id)
    return full_name, contact


async def purchase_notification(user_id, term, month_word, workplace, price):
    full_name, contact = await get_user_info(user_id)
    text = (f"Пользователь {full_name} с ID {user_id} только что приобрёл лицензию\n"
            f"*Срок:* {term} {month_word}\n"
            f"*Количество рабочих мест:* {workplace}\n"
            f"*Сумма:* {price}\n")

    if contact:
        text += f"\nСвязаться с ним можно по {contact}"
    else:
        text += "У этого человека нет юзернейма"

    admin_ids = await get_admins()
    for admin_id in admin_ids:
        await bot.send_message(admin_id, text)

#убрать payment_kb