from aiogram.dispatcher import FSMContext

from keyboards.default.admin_keyboards import admins_panel
from keyboards.inline.inline_keyboards import languages
from loader import dp, types, _
from states.states import RegisterState
from utils.db_api.database_settings import *
from keyboards.default.users_keyboards import *



@dp.message_handler(state='in_start', text="Location")
async def location(message:types.Message):
    await message.answer_location(41.349602257709535, 69.2261550858946)

@dp.message_handler(state='*', commands="start")
async def bot_start(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    if await is_admin(message.chat.id):
        await message.answer(text=f"Xush kelibsiz.", reply_markup=admins_panel)
        await state.finish()
    else:
        if user:
            await message.answer(text=_('😊 Assalomu alaykum. Xush kelibsiz.', locale=user[4]),
                                 reply_markup=await main_menu(lang=user[4]))
            await state.finish()
            await state.set_state('in_start')
        else:
            userga = f"""
🇺🇿 Assalomu alaykum. Botimizga xush kelibsiz. Iltimos o'zingizga qulay bo'lgan tilni tanlang.
🇷🇺 Привет. Добро пожаловать в наш Telegram-бот. Выберите предпочитаемый язык.
🇨🇳 你好呀。欢迎使用我们的 Telegram 机器人。选择您的首选语言。
🇺🇸 Hello there. Welcome to our Telegram bot. Choose your preferred language.
"""
            await message.answer(text=userga, reply_markup=languages)
            await RegisterState.get_lang.set()


@dp.message_handler(state='in_start')
async def in_start_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    if message.text[0] == "🍴":
        menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        menu.insert(KeyboardButton(text=_(f"⬅️ Ortga")))
        menu.insert(KeyboardButton(text=_(f"🛍 Savat")))
        userga = _('😋 Bizning menyu', locale=user[4])
        menu_ = await menu_functions(lang=user['lang'])
        for i in menu_:
            menu.insert(KeyboardButton(text=f"{i['name']}"))
        await message.answer(text=userga, reply_markup=menu)
        await state.set_state('get_food')
    elif message.text.split(" ")[0] == "✍️":
        await message.answer(text=_("😊 Izohingizni yozing", locale=user['lang']), reply_markup=await cancel(lang=user[4]))
        await state.set_state('send_comment')
    elif message.text.split(" ")[0] == "⚙️":
        await message.answer(text=_(f"⚙️ Sozlamalar"), reply_markup=await user_settings_menu(lang=user[4]))
        await state.set_state('in_settings')

@dp.message_handler(text=f"🍴 Menyu")
async def menu(message: types.Message, state: FSMContext):
    await state.update_data({
        'loc': 'in_menu'
    })
    user = await get_user(message.from_user.id)
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    menu.insert(KeyboardButton(text=_(f"⬅️ Ortga")))
    menu.insert(KeyboardButton(text=_(f"🛍 Savat")))
    userga = _('😋 Bizning menyu', locale=user['lang'])
    menu_ = await menu_functions(lang=user['lang'])
    for i in menu_:
        menu.insert(KeyboardButton(text=f"{i['name']}"))
    await message.answer(text=userga, reply_markup=menu)
    await state.set_state('get_food')


@dp.message_handler(state='in_settings')
async def in_settings_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    if message.text[0] == '👤':
        await message.answer(text=_(f"😊 To'liq ismingizni kiriting.", locale=user[4]), reply_markup=await cancel(lang=user[4]))
        await state.set_state('change_full_name')
    elif message.text[0] == '📞':
        await message.answer(text=_(f"😊 Telefon raqamingizni tugma orqali yuboring, yoki yozib yuboring."), reply_markup=await send_phone_number(lang=user[4]))
        await state.set_state('change_phone_number')
    else:
        await message.answer(text=_(f"😊 O'zingizga qulay tilni tanlang."), reply_markup=await cancel(lang=user[4]))
        await message.answer(text=_(f"Mavjud tillar"), reply_markup=languages)
        await state.set_state('change_lang')

@dp.callback_query_handler(state='change_lang')
async def change_lang_handler(call: types.CallbackQuery, state: FSMContext):
    await user_settings(lang=call.data, work='UPDATE_LANG', chat_id=call.message.chat.id)
    await call.message.answer(text=_(f"😊 Muloqot tili o'zgartirildi.", locale=call.data), reply_markup=await main_menu(call.data))
    await state.set_state('in_start')

@dp.message_handler(state='change_full_name')
async def change_full_name_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    await user_settings(work='UPDATE_FULL_NAME', full_name=message.text, chat_id=message.chat.id)
    await message.answer(text=_(f"😊 Ism muvaffaqqiyatli o'zgartirildi.", locale=user['lang']), reply_markup=await main_menu(user['lang']))
    await state.set_state('in_start')

@dp.message_handler(state='change_phone_number', content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def change_phone_number_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    await user_settings(work='UPDATE_PHONE_NUMBER', phone_number=message.contact.phone_number if message.contact else message.text, chat_id=message.chat.id)
    await message.answer(text=_(f"😊 Telefon raqam o'zgartirildi.", locale=user['lang']), reply_markup=await main_menu(user['lang']))
    await state.set_state('in_start')


@dp.message_handler(state='send_comment')
async def send_comment_handler(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    for admin in await get_admins():
        await dp.bot.send_message(chat_id=admin['chat_id'],
                                  text=f"Foydalanuvchidan izoh\n👤 To'liq ism: {user['full_name']}\n👤 Username: @{user['username']}\n💬 Izoh: {message.text}")
    await message.answer(text=f"✅ Izhongiz adminlarga yuborildi", reply_markup=await main_menu(user['lang']))
    await state.finish()

@dp.message_handler(commands='users')
async def users_to_programmer(message: types.Message, state: FSMContext):
    users = _("📰 Foydalanuvchilar ro'yxati: \n\nTil \t\t | Ism Familya   | Username |\n", locale=user['lang'])
    count = 0
    for i in await user_settings(work='GET'):
        flag = ""
        if i['lang'] == "zh":
            flag = f"🇨🇳"
        elif i['lang'] == "uz":
            flag = "🇺🇿"
        elif i['lang'] == "ru":
            flag = f"🇷🇺"
        else:
            flag = f"🇺🇸"
        full_name = i['full_name'] if len(i['full_name']) <= 10 else i['full_name'][:10] + "..."
        username = f"<a href='tg://user?id={i['chat_id']}'>User</a>"
        users += f"{flag} | {full_name:<12} | {username} | {i['phone_number']}\n"
        count += 1
    users += f"\n👥 Ja'mi foydalanuvchilar: "
    users += f"<b>{count}</b>"
    await message.answer(text=users, parse_mode='HTML')

