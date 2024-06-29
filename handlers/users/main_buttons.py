from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.users_keyboards import main_menu
from loader import dp, types, _
from aiogram.dispatcher import FSMContext

from utils.db_api.database_settings import basket_functions, get_user


@dp.message_handler(state='*', text=f"🏘 Asosiy menyu")
async def back_main_menu(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=await main_menu(lang='uz'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text='🏘 主菜单')
async def back_main_menu(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=await main_menu(lang='zh'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text='🏘 Main menu')
async def back_main_menu(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=await main_menu(lang='en'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text='🏘 Главное меню')
async def back_main_menu(message: types.Message, state: FSMContext):
    await message.answer(message.text, reply_markup=await main_menu(lang='ru'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=f"❌ Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=await main_menu(lang='ru'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=f"❌ Cancel")
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=await main_menu(lang='en'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=f"❌ 取消")
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=await main_menu(lang='zh'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=f"❌ Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    await message.answer(text=message.text, reply_markup=await main_menu(lang='ru'))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=f"🛍 Корзина")
async def show_basket_handler(message: types.Message, state: FSMContext):
    savat = await basket_functions(chat_id=message.chat.id, work='GET')
    user = await get_user(message.chat.id)
    if savat:
        userga = _("😊 Savatingiz", locale=user['lang'])
        userga += '\n'
        user_basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        user_basket.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        user_basket.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        count = 0
        for basket in savat:
            userga += f"\n<b>{basket['product']}</b> \t | \t <b>{basket['quantity']} * {basket['price']}</b> = <b>{basket['quantity'] * basket['price']}</b>"
            count += basket['price'] * basket['quantity']
            user_basket.insert(KeyboardButton(text=f"❌ {basket['product']}", locale=user['lang']))
        userga += "\n"
        userga += "\n"
        userga += _(f"💰 Ja'mi: ", locale=user['lang'])
        userga += f"<b>{count}</b>"
        await message.answer(text=userga, reply_markup=user_basket)
        await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu('ru'))
        await state.set_state('in_start')

@dp.message_handler(state='*', text=f"🛍 Savat")
async def show_basket_handler(message: types.Message, state: FSMContext):
    savat = await basket_functions(chat_id=message.chat.id, work='GET')
    user = await get_user(message.chat.id)
    if savat:
        userga = _("😊 Savatingiz", locale=user['lang'])
        userga += '\n'
        user_basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        user_basket.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        user_basket.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        count = 0
        for basket in savat:
            userga += f"\n<b>{basket['product']}</b> \t | \t <b>{basket['quantity']} * {basket['price']}</b> = <b>{basket['quantity'] * basket['price']}</b>"
            count += basket['price'] * basket['quantity']
            user_basket.insert(KeyboardButton(text=f"❌ {basket['product']}", locale=user['lang']))
        userga += "\n"
        userga += "\n"
        userga += _(f"💰 Ja'mi: ", locale=user['lang'])
        userga += f"<b>{count}</b>"
        await message.answer(text=userga, reply_markup=user_basket)
        await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu('uz'))
        await state.set_state('in_start')

@dp.message_handler(state='*', text=f"🛍 Cart")
async def show_basket_handler(message: types.Message, state: FSMContext):
    savat = await basket_functions(chat_id=message.chat.id, work='GET')
    user = await get_user(message.chat.id)
    if savat:
        userga = _("😊 Savatingiz", locale=user['lang'])
        userga += '\n'
        user_basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        user_basket.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        user_basket.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        count = 0
        for basket in savat:
            userga += f"\n<b>{basket['product']}</b> \t | \t <b>{basket['quantity']} * {basket['price']}</b> = <b>{basket['quantity'] * basket['price']}</b>"
            count += basket['price'] * basket['quantity']
            user_basket.insert(KeyboardButton(text=f"❌ {basket['product']}", locale=user['lang']))
        userga += "\n"
        userga += "\n"
        userga += _(f"💰 Ja'mi: ", locale=user['lang'])
        userga += f"<b>{count}</b>"
        await message.answer(text=userga, reply_markup=user_basket)
        await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu('en'))
        await state.set_state('in_start')

@dp.message_handler(state='*', text=f"🛍 篮子")
async def show_basket_handler(message: types.Message, state: FSMContext):
    savat = await basket_functions(chat_id=message.chat.id, work='GET')
    user = await get_user(message.chat.id)
    if savat:
        userga = _("😊 Savatingiz", locale=user['lang'])
        userga += '\n'
        user_basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        user_basket.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        user_basket.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        count = 0
        for basket in savat:
            userga += f"\n<b>{basket['product']}</b> \t | \t <b>{basket['quantity']} * {basket['price']}</b> = <b>{basket['quantity'] * basket['price']}</b>"
            count += basket['price'] * basket['quantity']
            user_basket.insert(KeyboardButton(text=f"❌ {basket['product']}", locale=user['lang']))
        userga += "\n"
        userga += "\n"
        userga += _(f"💰 Ja'mi: ")
        userga += f"<b>{count}</b>"
        await message.answer(text=userga, reply_markup=user_basket)
        await state.set_state('in_basket')
    else:
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu('zh'))
        await state.set_state('in_start')

@dp.callback_query_handler(state='*', text='basket')
async def basket_handler(call: types.CallbackQuery, state: FSMContext):
    user = await get_user(call.message.chat.id)
    savat = await basket_functions(chat_id=call.message.chat.id, work='GET')
    if savat:
        userga = _("😊 Savatingiz", locale=user['lang'])
        userga += '\n'
        user_basket = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        user_basket.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user['lang'])))
        user_basket.insert(KeyboardButton(text=_(f"🛒 Buyurtma berish", locale=user['lang'])))
        count = 0
        for basket in savat:
            userga += f"\n<b>{basket['product']}</b> \t | \t {basket['quantity']} | \t <b>{basket['quantity']} * {basket['price']}</b> = <b>{basket['quantity'] * basket['price']}</b>"
            count += basket['price'] * basket['quantity']
            user_basket.insert(KeyboardButton(text=f"❌ {basket['product']}", locale=user['lang']))
        userga += f"\n"
        userga += f"\n"
        userga += _(f"💰 Ja'mi: ", locale=user['lang'])
        userga += f"<b>{count}</b>"
        await call.message.answer(text=userga, reply_markup=user_basket)
        await state.set_state('in_basket')
    else:
        await call.message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu(user['lang']))
        await state.set_state('in_start')
