from Config import bot, DB, dp, UserState
from Keyboards.SuperAdmin import conf_payment_kb, conf_payment_kb2
from aiogram.types import CallbackQuery
from HelloMessages.Client import thank_you
from Client.HelpFunctions import save_order
from LicenseKey import workplaces_keys
from aiogram.utils.exceptions import ChatNotFound


messages_ids = {}
messages_ids2 = {}
order_info = {}
conf_info = {}


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
    kb = await conf_payment_kb(user_id)
    text = (f"Пользователь {full_name} с ID {user_id} оплатил лицензию\n\n"
            f"*Срок:* {term} {month_word}\n"
            f"*Количество рабочих мест:* {workplace}\n"
            f"*Сумма:* {price}\n\n")

    if contact == '-':
        text += "У этого человека нет юзернейма"
        conf_info[user_id] = (full_name, None)
    else:
        text += f"Связаться с ним можно по {contact}"
        conf_info[user_id] = (full_name, contact)

    admin_ids = await get_admins()

    for admin_id in admin_ids:
        try:
            message = await bot.send_message(admin_id, text, 'Markdown', reply_markup=kb)
            message_id = message.message_id
            messages_ids[admin_id] = message_id
        except ChatNotFound:
            continue
    order_info[user_id] = (term, month_word, workplace, price)


async def get_common_data(call):
    admin_id = call.from_user.id

    user_id = int(call.data.split(':')[0])
    choice = call.data.split(':')[1]

    term, month_word, workplace, price = order_info[user_id]

    return admin_id, user_id, choice, term, month_word, price, workplace


async def handle_conf_payment(admin_id, user_id, term, month_word, workplace, price, keys):
    await save_order(user_id, term, workplace, price, keys)
    await thank_you(user_id, term, month_word, workplace, keys)
    full_name, contact = await get_user_info(user_id)

    header = "Оплата подтверждена"

    add_header = " другим администратором"
    body = (f"\n*Цена:* {price} рублей\n"
            f"*ФИО:* {full_name}\n")

    if contact == '-':
        body += "У этого пользователя нет юзернейма"
    else:
        body += f"*Юзернейм:* {contact}"

    text1 = header + body
    text2 = header + add_header + body

    for admin_chat, message_id in messages_ids.items():
        await bot.edit_message_reply_markup(admin_chat, message_id, reply_markup=None)
        if admin_chat == admin_id:
            await bot.send_message(admin_id, text1, 'Markdown')
        else:
            await bot.send_message(admin_chat, text2, 'Markdown')


async def handle_no_conf_payment(admin_id, user_id):
    await bot.send_message(admin_id, "Оплата отклонена")
    await bot.send_message(user_id, "Ваша оплата была отклонена администратором")
    for admin_chat, message_id in messages_ids.items():
        await bot.edit_message_reply_markup(admin_chat, message_id, reply_markup=None)


@dp.callback_query_handler(lambda call: True, state=UserState.payment_conf)
async def second_conf_handler(call: CallbackQuery, state):
    try:
        prev_choice = call.data.split(':')[2]
    except IndexError:
        await call.answer("Вам нужно действовать по порядку.\n"
                          "Сначала подтвердите/отклоните заявку человека, на которую уже нажали", show_alert=True)
        return

    admin_id, user_id, choice, term, month_word, price, workplace = await get_common_data(call)

    message_id = call.message.message_id

    if choice == "conf":
        if prev_choice == "yes":
            keys = await workplaces_keys(workplace)
            await handle_conf_payment(admin_id, user_id, term, month_word, workplace, price, keys)

        elif prev_choice == "no":
            await handle_no_conf_payment(admin_id, user_id)

        for admin_id, message_id in messages_ids2.items():
            await bot.delete_message(admin_id, message_id)

    else:
        await bot.delete_message(admin_id, message_id)

    await state.finish()


@dp.callback_query_handler(lambda call: call.data.endswith('payment'), state="*")
async def confirmation_handler(call: CallbackQuery):
    admin_id, user_id, choice, term, month_word, price, workplace = await get_common_data(call)
    full_name, contact = conf_info[user_id]

    if choice == "conf_payment":
        action, choice_key = "подтвердить", "yes"

    elif choice == "no_conf_payment":
        action, choice_key = "отклонить", "no"

    text = (f"Вы уверены, что хотите {action} оплату пользователя?\n\n"
            f"Цена: {price} рублей\n"
            f"ФИО: {full_name}\n")

    if contact == '-':
        text += "У этого пользователя нет юзернейма"
    else:
        text += f"Юзернейм: {contact}"

    message = await (bot.send_message(admin_id, text,
                     reply_markup=await conf_payment_kb2(user_id, choice_key)))
    message_id = message.message_id
    messages_ids2[admin_id] = message_id
    await UserState.payment_conf.set()
