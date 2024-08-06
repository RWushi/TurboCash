from aiogram.types import Message
from aiogram.utils import executor
from Config import dp
from DaysUpdate import everyday_task
from Keyboards.Client import support_kb
from Client.HelpFunctions import add_new_user, exists_check, get_contact, get_role, purchase_check
from HelloMessages.Admin import menu as admin
from HelloMessages.SuperAdmin import menu as superadmin
from HelloMessages.Client import full_name, rates_existing, rates_new, delete_black_list


@dp.message_handler(commands=['start', 'my_id', 'help', 'blacklist'], state="*")
async def role_check(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    role = await get_role(user_id)

    if message.text == '/start':
        contact = await get_contact(user_id)
        await add_new_user(user_id, contact)

        if role == 'admin':
            await admin(chat_id)
        elif role == 'superadmin':
            await superadmin(chat_id)
        elif role == 'client':
            user_exists = await exists_check(user_id)
            if user_exists:
                user_purchased = await purchase_check(user_id)
                if user_purchased:
                    await rates_existing(chat_id)
                else:
                    await rates_new(chat_id)
            else:
                await full_name(chat_id)
        else:
            await full_name(chat_id)

    elif message.text == '/my_id':
        await message.answer(f"Ваш ID: `{user_id}`", parse_mode="Markdown")

    elif message.text == '/help':
        await message.answer("По всем вопросам обращайтесь в поддержку", reply_markup=support_kb)

    elif message.text == '/blacklist':
        if role == 'admin':
            await message.answer("Поскольку Вы являетесь администратором, Вам не нужно отправлять заявки на удаление и добавление в ЧС")
        elif role == 'superadmin':
            await message.answer("Поскольку Вы являетесь супер-администратором, Вам не нужно отправлять заявки на удаление и добавление в ЧС")
        elif role == 'client':
            await delete_black_list(chat_id)


import Client.FullName, Client.BlackListRequest, SuperAdmin.Menu, Admin.Menu


async def on_startup(dp):
    await everyday_task()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
