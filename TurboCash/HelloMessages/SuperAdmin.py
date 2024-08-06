from Config import bot, UserState
from Keyboards.SuperAdmin import menu_kb, back_kb, add_delete_kb


async def menu(chat_id):
    text = "Выберите действие:"
    kb = menu_kb
    await UserState.menu.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def admin(chat_id):
    text = "Выберите действие:"
    kb = add_delete_kb
    await UserState.admin.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def black_list(chat_id):
    text = "Выберите действие:"
    kb = add_delete_kb
    await UserState.black_list.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def add_admin(chat_id):
    text = "Введите ID пользователя, которого хотите сделать администратором (для того, чтобы сделать пользователя администратором, этот человек уже должен пользоваться этим ботом)"
    kb = back_kb
    await UserState.add_admin.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def delete_admin(chat_id):
    text = "Введите ID администратора, которого хотите удалить"
    kb = back_kb
    await UserState.delete_admin.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def add_black_list(chat_id):
    text = "Введите ID пользователя, которого хотите внести в черный список"
    kb = back_kb
    await UserState.add_black_list.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def delete_black_list(chat_id):
    text = "Введите ID пользователя, которого хотите убрать из черного списка"
    kb = back_kb
    await UserState.delete_black_list.set()
    await bot.send_message(chat_id, text, reply_markup=kb)
