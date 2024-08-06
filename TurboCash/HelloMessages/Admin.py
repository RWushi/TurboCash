from Config import bot
from Keyboards.Admin import menu_kb


async def menu(chat_id):
    text = "Выберите действие:"
    kb = menu_kb
    await bot.send_message(chat_id, text, reply_markup=kb)
