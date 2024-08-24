from Config import bot, UserState
from Keyboards.Admin import menu_kb


async def menu(chat_id):
    text = "Выберите действие:"
    kb = menu_kb
    await UserState.menu.admin.set()
    await bot.send_message(chat_id, text, reply_markup=kb)
