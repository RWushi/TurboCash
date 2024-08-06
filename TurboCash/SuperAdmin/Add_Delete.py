from aiogram.types import Message
from Config import dp, UserState, DB
from HelloMessages.SuperAdmin import admin, black_list as bl


async def check_id(user_id):
    async with DB() as conn:
        result = await conn.fetchrow('SELECT 1 FROM user_settings WHERE ID = $1', user_id)
    return result is not None


async def check_client_id(client_id):
    async with DB('kirill') as conn:
        result = await conn.fetchrow('SELECT 1 FROM clients WHERE ID = $1', client_id)
    return result is not None


async def check_role(user_id):
    async with DB() as conn:
        role = await conn.fetchval('SELECT role FROM user_settings WHERE ID = $1', user_id)
    return role


async def check_black_list(client_id):
    async with DB('kirill') as conn:
        black_list = await conn.fetchval('SELECT blacklist FROM clients WHERE ID = $1', client_id)
        if black_list:
            info = await conn.fetchrow('SELECT fio, phone, adr FROM clients WHERE ID = $1', client_id)
            info_tuple = (info['fio'], info['phone'], info['adr'])
            return info_tuple
    return False


async def add_admin(user_id):
    async with DB() as conn:
        async with conn.transaction():
            await conn.execute('''
                UPDATE user_settings 
                SET role = 'admin'
                WHERE ID = $1
            ''', user_id)
            await conn.execute('DELETE FROM client WHERE ID = $1', user_id)


async def delete_admin(user_id):
    async with DB() as conn:
        await conn.execute('DELETE FROM user_settings WHERE ID = $1', user_id)


async def add_black_list(client_id):
    async with DB('kirill') as conn:
        await conn.execute('UPDATE clients SET blacklist = True WHERE ID = $1', client_id)


async def delete_black_list(client_id):
    async with DB('kirill') as conn:
        await conn.execute('UPDATE clients SET blacklist = False WHERE ID = $1', client_id)


@dp.message_handler(state=UserState.add_admin)
async def add_admin_handler(message: Message):
    chat_id = message.chat.id

    if message.text.isdigit():
        user_id = int(message.text)
        user_exists = await check_id(user_id)
        if user_exists:
            role = await check_role(user_id)
            if role == 'client':
                await add_admin(user_id)
                await message.answer(f"Пользователь с ID {user_id} добавлен, как администратор, чтобы применилась новая роль, ему нужно перезапустить бота")
            elif role == 'admin':
                await message.answer(f"Пользователь с ID {user_id} итак является администратором")
        else:
            await message.answer(f"Пользователя с ID {user_id} в этом боте не существует")

    elif message.text == "↩️ Вернуться назад":
        await admin(chat_id)

    else:
        await message.answer("Введите числовой ID")


@dp.message_handler(state=UserState.delete_admin)
async def delete_admin_handler(message: Message):
    chat_id = message.chat.id

    if message.text.isdigit():
        user_id = int(message.text)
        user_exists = await check_id(user_id)

        if user_exists:
            role = await check_role(user_id)
            if role == 'client':
                await message.answer(f"Пользователь с ID {user_id} является клиентом, а не администратором")
            elif role == 'admin':
                await delete_admin(user_id)
                await message.answer(f"Пользователь с ID {user_id} больше не является администратором")
        else:
            await message.answer(f"Пользователя с ID {user_id} в этом боте не существует")

    elif message.text == "↩️ Вернуться назад":
        await admin(chat_id)

    else:
        await message.answer("Введите числовой ID")


@dp.message_handler(state=UserState.add_black_list)
async def add_black_list_handler(message: Message):
    chat_id = message.chat.id

    if message.text.isdigit():
        client_id = int(message.text)
        user_exists = await check_client_id(client_id)
        if user_exists:
            blacklist = await check_black_list(client_id)
            if blacklist:
                await message.answer(f"Пользователь с ID {client_id} итак находится в черном списке")
            else:
                await add_black_list(client_id)
                await message.answer(f"Пользователь с ID {client_id} добавлен в черный список")
        else:
            await message.answer(f"Пользователя с ID {client_id} не существует в базе данных")

    elif message.text == "↩️ Вернуться назад":
        await bl(chat_id)

    else:
        await message.answer("Введите числовой ID")


@dp.message_handler(state=UserState.delete_black_list)
async def delete_black_list_handler(message: Message):
    chat_id = message.chat.id

    if message.text.isdigit():
        client_id = int(message.text)
        user_exists = await check_client_id(client_id)
        if user_exists:
            blacklist = await check_black_list(client_id)
            if blacklist:
                await delete_black_list(client_id)
                await message.answer(f"Пользователь с ID {client_id} удален из черного списка")
            else:
                await message.answer(f"Пользователя с ID {client_id} нет в черном списке")
        else:
            await message.answer(f"Пользователя с ID {client_id} не существует в базе данных")

    elif message.text == "↩️ Вернуться назад":
        await bl(chat_id)

    else:
        await message.answer("Введите числовой ID")
