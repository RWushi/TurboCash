from Config import bot, UserState
from Keyboards.Client import rates_kb, payment_kb


async def full_name(chat_id):
    text = (
        "Введите Ваше **ФИО**:\n\n"
        "⚠️ **Внимание**: к Вашему ФИО, имени в телеграме и компьютеру будет привязана лицензия на программу!"
    )
    await UserState.full_name.set()
    await bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=None)


async def rates_new(chat_id):
    text = "Купить лицензию программы TurboCash:"
    kb = rates_kb
    await UserState.rates.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def rates_existing(chat_id):
    text = "Продлить лицензию программы TurboCash:"
    kb = rates_kb
    await UserState.rates.set()
    await bot.send_message(chat_id, text, reply_markup=kb)


async def workplace(chat_id):
    text = "Введите количество рабочих мест:\nСтоимость подключения более 1 рабочего места 2 000₽/место:"
    await UserState.workplace.set()
    await bot.send_message(chat_id, text)


async def confirmation(chat_id, term, month_word, workplace, workplace_word, price):
    text = ("Вы выбрали следующие параметры лицензии:\n"
            f"*Срок:* {term} {month_word}\n"
            f"*Количество рабочих мест:* {workplace}\n"
            f"*Сумма:* {price}\n\n"
            f"Отправьте {price} руб. на номер телефона `89220791980` на Сбер или Т-Банк (Тинькофф).\n"
            "После оплаты нажмите кнопку \"✅ Оплачено\"\n\nВ течение дня вам придет программа "
            "и лицензионный ключ для доступа к программе TurboCash.\n⚠️ Не останавливайте и не "
            "удаляйте бот.\n\nНажмите \"❌ Отменить\" для отмены.")
    kb = payment_kb

    await UserState.confirmation.set()
    await bot.send_message(chat_id, text, 'Markdown', reply_markup=kb)


async def thank_you(chat_id, term, month_word, workplace, keys):
    keys_str = '\n\n'.join([f'`{key}`' for key in keys])
    text = ("Спасибо за покупку\\!\n\n"
            f"*Срок:* {term} {month_word}\n"
            f"*Количество рабочих мест:* {workplace}\n\n"
            f"*Лицензионные ключи:*\n{keys_str}\n\n"
            "*Поддержка:* @rabat057\n"
            "*Канал для замечаний и предложений:* https://t\\.me/\\+81XAkkxZhPIyOWU6\n"
            "*Ссылка для скачивания файла:* https://drive\\.google\\.com/file/d/1ihtaGgwBxvZNPc6kye7P5lrMqaIJyqcs/view?usp\\=sharing")
    await bot.send_message(chat_id, text, parse_mode="MarkdownV2")


async def delete_black_list(chat_id):
    text = "Введите ID пользователя, которого хотите убрать из черного списка и администратор рассмотрит Вашу заявку"
    await UserState.delete_bl_req.set()
    await bot.send_message(chat_id=chat_id, text=text)


async def agreement(chat_id, client_id):
    text = f"Ваша заявка на удаление пользователя с ID: {client_id} из черного списка была одобрена администратором"
    await bot.send_message(chat_id, text)


async def disagreement(chat_id, client_id):
    text = f"Ваша заявка на удаление пользователя с ID: {client_id} из черного списка была отклонена администратором"
    await bot.send_message(chat_id, text)
