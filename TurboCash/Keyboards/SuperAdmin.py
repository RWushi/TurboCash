from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⛔ Черный список")],
        [KeyboardButton(text="🧑‍💻 Администраторы")],
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)


add_delete_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить")],
        [KeyboardButton(text="➖ Удалить")],
        [KeyboardButton(text="↩️ Вернуться в меню")]
    ],
    resize_keyboard=True
)


back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩️ Вернуться назад")]
    ],
    resize_keyboard=True
)


confirmation_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="✅ Подтвердить", callback_data="conf"),
    InlineKeyboardButton(text="❌ Отклонить", callback_data="no_conf")
)


async def conf_payment_kb(user_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"{user_id}:conf_payment"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"{user_id}:no_conf_payment")
    )


async def conf_payment_kb2(user_id, choice):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"{user_id}:conf:{choice}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"{user_id}:no_conf:{choice}")
    )
