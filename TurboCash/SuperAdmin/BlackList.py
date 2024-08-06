from aiogram.types import Message
from Config import dp, UserState
from HelloMessages.SuperAdmin import add_black_list, delete_black_list, menu


@dp.message_handler(state=UserState.black_list)
async def black_list_edit_handler(message: Message):
    chat_id = message.chat.id

    if message.text == "➕ Добавить":
        await add_black_list(chat_id)

    elif message.text == "➖ Удалить":
        await delete_black_list(chat_id)

    elif message.text == "↩️ Вернуться в меню":
        await menu(chat_id)


import SuperAdmin.Add_Delete
