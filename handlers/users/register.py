from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.users_keyboards import *
from loader import dp, bot, _
from states.states import RegisterState
from utils.db_api.database_settings import add_user


@dp.callback_query_handler(state=RegisterState.get_lang)
async def register_lang(call: types.CallbackQuery, state: FSMContext):
    await state.update_data({
        'lang': call.data
    })
    userga = _('Uzbek tili tanlandi. Iltimos ismingizni kiriting.', locale=call.data)
    await call.message.delete()
    await call.message.answer(text=userga)
    await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name, content_types=types.ContentType.TEXT)
async def process_full_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({
        'full_name': message.text,
        'lang': data['lang']
    })
    await message.answer(text=_(f"📞 Iltimos telefon raqamingizni yuboring.", locale=data['lang']),
                         reply_markup=await send_phone_number(lang=data['lang']))
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def register_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone_number = message.contact.phone_number if message.contact.phone_number else message.text
    if phone_number[0] != "+":
        phone_number = f"+{phone_number}"
    await state.update_data({
        'full_name': data['full_name'],
        'lang': data['lang'],
        'chat_id': message.chat.id,
        'phone_number': phone_number,
        'created_at': message.date,
        'username': message.from_user.username if message.from_user.username is not None else 'Mavjud emas'
    })
    if await add_user(data=await state.get_data()):
        userga = _("🥳 Tabriklaymiz", locale=data['lang'])
        usergaa = _('Siz muvaffaqqiyatli royxatdan otdingiz.', locale=data['lang'])
        await message.answer(
            text=f"{userga} {data['full_name']}. {usergaa}",
            reply_markup=await main_menu(lang=data['lang']))
        await state.set_state('in_start')
    else:
        await message.answer(
            text=f"😕 Kechirasiz. Botimizda hatolik yuz berdi. Iltimos qayta /start bosib urunib ko'ring.")
        await state.finish()
