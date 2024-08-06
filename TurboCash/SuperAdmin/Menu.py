from aiogram.types import Message, InputFile
from Config import bot, dp, UserState
from HelloMessages.SuperAdmin import admin, black_list
from .Statistics import get_file
from datetime import datetime, timezone


@dp.message_handler(state=UserState.menu)
async def menu_handler(message: Message):
    chat_id = message.chat.id

    if message.text == "⛔ Черный список":
        await black_list(chat_id)

    elif message.text == "🧑‍💻 Администраторы":
        await admin(chat_id)

    elif message.text == "📊 Статистика":
        await message.answer("Ваш файл готовится...")
        file = await get_file()
        current_date_utc = datetime.now(timezone.utc).date()
        formatted_date = current_date_utc.strftime("%d.%m.%Y")
        filename = f"{formatted_date} TurboCash статистика по пользователям.xlsx"
        file_input = InputFile(file, filename=filename)
        await bot.send_document(chat_id, file_input)


import SuperAdmin.Add_Delete, SuperAdmin.Admin, SuperAdmin.BlackList
