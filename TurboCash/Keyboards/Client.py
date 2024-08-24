from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


rates_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="1 мес - 10 000 ₽", callback_data="1_month"),
    InlineKeyboardButton(text="3 мес - 30 000 ₽", callback_data="3_months"),
    InlineKeyboardButton(text="6 мес - 60 000 ₽", callback_data="6_months"),
    InlineKeyboardButton(text="12 мес - 100 000 ₽", callback_data="12_months")
)

payment_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="✅ Оплачено", callback_data="yes"),
    InlineKeyboardButton(text="❌ Отменить", callback_data="no")
)

support_kb = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="📞 Поддержка", url="https://t.me/rabat057")
)
