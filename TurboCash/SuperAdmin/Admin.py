from aiogram.types import Message
from Config import dp, UserState
from HelloMessages.SuperAdmin import add_admin, delete_admin, menu


@dp.message_handler(state=UserState.admin)
async def admin_edit_handler(message: Message):
    chat_id = message.chat.id

    if message.text == "➕ Добавить":
        await add_admin(chat_id)

    elif message.text == "➖ Удалить":
        await delete_admin(chat_id)

    elif message.text == "↩️ Вернуться в меню":
        await menu(chat_id)


import SuperAdmin.Add_Delete
