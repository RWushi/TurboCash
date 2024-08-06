from aiogram.types import Message
from Config import dp, UserState
from HelloMessages.SuperAdmin import add_black_list, delete_black_list


@dp.message_handler(state=UserState.menu)
async def menu_handler(message: Message):
    chat_id = message.chat.id

    if message.text == "➕ Добавить в ЧС":
        await add_black_list(chat_id)

    elif message.text == "➖ Удалить из ЧС":
        await delete_black_list(chat_id)


import SuperAdmin.Add_Delete
