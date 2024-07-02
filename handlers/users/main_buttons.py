from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.admin_keyboards import admins_panel
from keyboards.default.users_keyboards import main_menu
from loader import dp, types, _
from aiogram.dispatcher import FSMContext

from utils.db_api.database_settings import basket_functions, get_user, menu_functions, is_admin


@dp.message_handler(state='*', text=[f"🏘 Asosiy menyu", "🏘 主菜单", "🏘 Main menu", '🏘 Главное меню'])
async def back_main_menu(message: types.Message, state: FSMContext):
    if await is_admin(message.chat.id):
        await message.answer(text=message.text, reply_markup=admins_panel)
        await state.finish()
    else:
        user = await get_user(message.chat.id)
        await message.answer(message.text, reply_markup=await main_menu(lang=user[4]))
        await state.set_state('in_start')

@dp.message_handler(state='*', text=[f"❌ Отмена", f"❌ Cancel", f"❌ 取消", "❌ Bekor qilish"])
async def cancel_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    await message.answer(text=message.text, reply_markup=await main_menu(lang=user[4]))
    await state.set_state('in_start')

@dp.message_handler(state='*', text=[f"🛍 Корзина", f"🛍 Savat", f"🛍 Cart"])
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
        await message.answer(text=_(f"😕 Kechirasiz sizning savatingiz bosh"), reply_markup=await main_menu(user['lang']))
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

@dp.message_handler(state='*', text=[f"⬅️ Ortga", f"⬅️ Back", f"⬅️返回", f"⬅️ Назад"])
async def back_menu_handler(message: types.Message, state: FSMContext):
    now_state = await state.get_state()
    user = await get_user(message.chat.id)
    if now_state == 'get_food':
        await message.answer(text=_(f"🏘 Asosiy menyu", locale=user['lang']), reply_markup=await main_menu(user['lang']))
        await state.set_state('in_start')
    elif now_state == 'in_food':
        menu = await state.get_data()
        all_menu = await menu_functions(lang=user[4])
        foods = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        foods.insert(KeyboardButton(text=_("⬅️ Ortga", locale=user['lang'])))
        foods.insert(KeyboardButton(text=_(f"🛍 Savat", locale=user['lang'])))
        for food in all_menu:
            foods.insert(KeyboardButton(text=food['name']))
        userga = _(f"😊 Bizning menyu", locale=user['lang'])
        await message.answer(text=userga, reply_markup=foods)
        await state.set_state('get_food')


