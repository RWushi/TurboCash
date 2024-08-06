from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from Config import dp, UserState
from SuperAdmin.Add_Delete import check_client_id, check_black_list
from SuperAdmin.BLRequest import delete_request


@dp.message_handler(state=UserState.delete_bl_req)
async def id_delete_bl_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        client_id = int(message.text)
        user_exists = await check_client_id(client_id)
        if user_exists:
            blacklist = await check_black_list(client_id)
            if blacklist:
                await state.update_data(client_id=client_id)
                fio, phone, adr = blacklist
                await message.answer("Этот клиент найден, а теперь укажите причину, по которой Вы хотите удалить его из черного списка"
                                     f"\n\n*ФИО:* {fio}\n*Телефон:* {phone}\n*Адрес:* {adr}", parse_mode='Markdown')
                await UserState.delete_cause_bl_req.set()
            else:
                await message.answer(f"Пользователя с ID {client_id} нет в черном списке")
        else:
            await message.answer(f"Пользователя с ID {client_id} не существует в базе данных")
    else:
        await message.answer(f"Введите числовой ID")


@dp.message_handler(state=UserState.delete_cause_bl_req)
async def delete_cause_bl_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cause = message.text
    data = await state.get_data()
    client_id = data['client_id']
    await delete_request(user_id, client_id, cause, state)
    await message.answer(f"Заявка на удаление пользователя с ID {client_id} в черный список отправлена администратору")
