from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admins_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"🍴 Menyu sozlamalari"),
        ],
        [
            KeyboardButton(text=f"🏷 Aksiya")
        ],
        [
            KeyboardButton(text=f"📝️ Xabar yuborish"),
            KeyboardButton(text=f"👥 Bot foydalanuvchilari")
        ],
        [
            KeyboardButton(text='🍴 Menyu'),
        ],
    ], resize_keyboard=True
)

stock_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"🏷 Aksiya yoqish o'chirish"),
            KeyboardButton(text=f"➕🏷 Aksiya qoshish")
        ],
        [
            KeyboardButton(text=f"❌ Bekor qilish")
        ]
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