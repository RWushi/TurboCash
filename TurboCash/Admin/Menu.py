from aiogram.types import Message
from Config import dp, UserState
from HelloMessages.SuperAdmin import add_black_list, delete_black_list
from SuperAdmin.Add_Delete import check_role


@dp.message_handler(state=UserState.menu.admin)
async def menu_handler(message: Message):
    chat_id = message.chat.id
    role = await check_role(chat_id)

    if role == 'admin':
        if message.text == "➕ Добавить в ЧС":
            await add_black_list(chat_id)

        elif message.text == "➖ Удалить из ЧС":
            await delete_black_list(chat_id)
    else:
        await message.answer("Вы не являетесь администратором")
