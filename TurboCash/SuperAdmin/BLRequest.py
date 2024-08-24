from Config import dp, DB, bot
from aiogram.types import CallbackQuery
from Keyboards.SuperAdmin import confirmation_kb
from HelloMessages.Client import agreement, disagreement
from SuperAdmin.Add_Delete import delete_black_list
from aiogram.utils.exceptions import ChatNotFound


messages_ids = {}


async def get_admins():
    async with DB() as conn:
        rows = await conn.fetch("SELECT id FROM user_settings WHERE role = 'admin' OR role = 'superadmin'")
    admin_ids = [row['id'] for row in rows]
    return admin_ids


async def delete_request(user_id, client_id, cause):
    text = f"Заявка на удаление клиента из черного списка от пользователя {user_id}\nID: {client_id}\nПричина: {cause}"
    kb = confirmation_kb
    admin_ids = await get_admins()

    for admin_id in admin_ids:
        try:
            message = await bot.send_message(admin_id, text, reply_markup=kb)
            message_id = message.message_id
            messages_ids[admin_id] = (user_id, client_id, message_id)
        except ChatNotFound:
            continue


@dp.callback_query_handler(lambda call: call.data.endswith('conf'), state="*")
async def confirmation_handler(call: CallbackQuery):
    admin_id = call.from_user.id

    request_user_id = messages_ids[admin_id][0]
    client_id = messages_ids[admin_id][1]

    if call.data == "conf":
        await delete_black_list(client_id)
        await bot.send_message(admin_id, f"Пользователь {client_id} удален из черного списка")

        for admin_id, (user_id, client_id, message_id) in messages_ids.items():
            await bot.delete_message(admin_id, message_id)

        await agreement(request_user_id, client_id)

    elif call.data == "no_conf":
        for admin_id, (user_id, client_id, message_id) in messages_ids.items():
            await bot.delete_message(admin_id, message_id)

        await disagreement(request_user_id, client_id)
