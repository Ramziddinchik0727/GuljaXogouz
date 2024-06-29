import random
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.users_keyboards import main_menu, my_locations
from loader import dp, types, _
from utils.db_api.database_settings import basket_functions, get_user, get_admins, menu_functions
from data.config import env

@dp.message_handler(state='in_basket')
async def in_basket_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    if message.text[0] == "❌":
        await basket_functions(work='DELETE', chat_id=message.chat.id, name=message.text[2:])
        savat = await basket_functions(work='GET', chat_id=message.chat.id)
        if savat:
            basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            basket.add(KeyboardButton(text=_(f"🏘 Asosiy menyu")))
            basket.add(KeyboardButton(text=_(f"🛒 Buyurtma berish")))
            for food in savat:
                basket.add(KeyboardButton(text=f"❌ {food['product']}"))
            await message.answer(_(f"✅ Mahsulot savatingizdan muvaffaqqiyatli olib tashlandi."), reply_markup=basket)
        else:
            await message.answer(_(f"✅ Mahsulot savatingizdan muvaffaqqiyatli olib tashlandi."), reply_markup=await main_menu(user['lang']))
            await state.set_state('in_start')
    elif message.text[0] == "🛒":
        await message.answer(text=_(f"📍 Yetkazib berish joylashuvini yuboring"), reply_markup=await my_locations(user[4]))
        await state.set_state('send_or_select_location')

@dp.message_handler(state='send_or_select_location', content_types=types.ContentType.LOCATION)
async def send_or_select_location_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'latitude': message.location.latitude,
        'longitude': message.location.longitude
    })
    user = await get_user(chat_id=message.chat.id)
    adminga = f"🛍 Yangi buyurtma:\n\n"
    adminga += f"👤 Toliq ism: {user['full_name']}\n"
    adminga += f"📞 Telefon raqam: {user['phone_number']}\n"
    flag = ""
    if user['lang'] == "uz":
        flag = f"🇺🇿"
    elif user['lang'] == "en":
        flag = f"🇺🇸"
    elif user['lang'] == "ru":
        flag = f"🇷🇺"
    else:
        flag = f"🇨🇳"
    adminga += f"{flag} Tanlangan til: {flag}\n\n"
    adminga += f"🛍 Mahsulotlar \n\n"
    count = 0
    order_number = ""
    for i in range(8):
        order_number += str(random.choice(range(10)))
    for basket in await basket_functions(chat_id=message.chat.id, work='GET'):
        food = await menu_functions(work='GET_FOR', name=basket['product'])
        count += basket['quantity'] * basket['price']
        adminga += f"<b>{food['name']}</b> \t | \t <b>{basket['quantity']}</b> \t | \t <b> {basket['quantity']}  * {basket['price']} = {basket['quantity'] * basket['price']}</b>\n"
    adminga += f"\n💰 Ja'mi: {count} so'm"
    await dp.bot.send_location(chat_id=env.str('GROUP_ID'), latitude=message.location.latitude, longitude=message.location.longitude)
    await dp.bot.send_message(chat_id=env.str('GROUP_ID'), text=adminga)
    await basket_functions(chat_id=message.chat.id, work='DELETE_BASKET')
    usergaa = _(f"✅ Buyurtmangiz qabul qilindi.", locale=user['lang'])
    usergaa += "\n"
    usergaa += _(f"🆔 Buyurtma raqamingiz: ", locale=user['lang'])
    usergaa += order_number
    await message.answer(usergaa, reply_markup=await main_menu(lang=user['lang']))
    await state.set_state('in_start')