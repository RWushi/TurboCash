from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить в ЧС")],
        [KeyboardButton(text="➖ Удалить из ЧС")]
    ],
    resize_keyboard=True
)
