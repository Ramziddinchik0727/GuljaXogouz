from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admins_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"🍴 Menyu sozlamalari"),
        ],
        [
            KeyboardButton(text=f"📝️ Xabar yuborish"),
            KeyboardButton(text=f"👥 Bot foydalanuvchilari")
        ],
        [
            KeyboardButton(text='🍴 Menyu'),
            KeyboardButton(text='⚙️ Sozlamalar')
        ],
    ], resize_keyboard=True
)

menu_settings = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'➕🍴 Taom qoshish'),
            KeyboardButton(text=f'🚫🍴 Taom olib tashlash'),
        ],
        [
            KeyboardButton(text=f"🔧💰 Taom narxini o'zgartirish"),
            KeyboardButton(text=f"🍴➕ Yangi menyu qoshish"),
        ],
        [
            KeyboardButton(text=f'🍴🚫 Menyu ochirish'),
        ],
        [
            KeyboardButton(text=f"🏘 Asosiy menyu")
        ]
    ], resize_keyboard=True
)