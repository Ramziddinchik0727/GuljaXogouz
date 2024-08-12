from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

async def main_menu(lang):
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('🍴 Menyu', locale=lang))
            ],
            [
                KeyboardButton(text=_('⚙️ Sozlamalar', locale=lang)),
                KeyboardButton(text="Location")
            ],
        ], resize_keyboard=True
    )
    return main_menu

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f"✅ Xa"),
            KeyboardButton(text=f"❌ Yo'q")
        ]
    ], resize_keyboard=True
)

async def payment_btn(lang):
    payment_btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("💸 Naqd")),
                KeyboardButton(text=f"💳 Kartaga to'lov")
            ],
            [
                KeyboardButton(text=_(f"❌ Bekor qilish"))
            ]
        ], resize_keyboard=True
    )
    return payment_btn
async def user_settings_menu(lang):
    settings = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_(f"👤 Ism Familyani O'zgartirish", locale=lang)),
                KeyboardButton(text=_(f"📞 Telefon Raqamni O'zgartirish", locale=lang)),
            ],
            [
                KeyboardButton(text=_(f"🇺🇿 🔁 🇷🇺 Tilni O'zgartirish", locale=lang)),
                KeyboardButton(text=_(f"🏘 Asosiy Menyu", locale=lang))
            ]
        ], resize_keyboard=True
    )
    return settings

async def send_phone_number(lang):
    send_phone_number = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('📞 Telefon Raqamni Yuborish', locale=lang), request_contact=True)
            ]
        ], resize_keyboard=True
    )
    return send_phone_number

async def my_locations(lang):
    locations = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_('📍 Joylashuv yuborish', locale=lang), request_location=True),
                KeyboardButton(text=_('❌ Bekor qilish', locale=lang))
            ]
        ], resize_keyboard=True
    )
    return locations

async def cancel(lang):
    cancel_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("❌ Bekor qilish", locale=lang))
            ]
        ], resize_keyboard=True
    )
    return cancel_button

async def back_button(lang):
    back_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🏘 Asosiy menyu", locale=lang)),
                KeyboardButton(text=_("🛍 Savat", locale=lang))
            ]
        ], resize_keyboard=True
    )
    return back_button
