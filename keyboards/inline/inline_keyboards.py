from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🇺🇿 O'zbek", callback_data="uz")
        ],
        [
            InlineKeyboardButton(text=f"🇷🇺 Русский", callback_data='ru')
        ],
        [
            InlineKeyboardButton(text=f"🇺🇸 English", callback_data='en')
        ],
        [
            InlineKeyboardButton(text=f'🇨🇳 中文', callback_data='zh')
        ]
    ]
)


async def plus_minus(count, sum, food, price):
    plus_minus_quantity = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("➖", callback_data=f"minus_{food}_{price}"),
                InlineKeyboardButton(f"{count} | {sum}", callback_data="quantity"),
                InlineKeyboardButton("➕", callback_data=f"plus_{food}_{price}")
            ],
            [
                InlineKeyboardButton(text=_('🛍 Savat'), callback_data=f'basket')
            ]
        ]
    )
    return plus_minus_quantity
