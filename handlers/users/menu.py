from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.users_keyboards import main_menu, back_button
from keyboards.inline.inline_keyboards import plus_minus
from loader import types, dp, _
from utils.db_api.database_settings import *


@dp.message_handler(state=f"get_food")
async def in_menu(message: types.Message, state: FSMContext):
    user = await get_user(chat_id=message.chat.id)
    menu_foods = await menu_functions(lang=user['lang'], work='GET_FOODS', menu_name=message.text)
    foods = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    await state.update_data({
        'loc': 'in_menu'
    })
    foods.insert(KeyboardButton(text=_(f"🏘 Asosiy menyu", locale=user[4])))
    foods.insert(KeyboardButton(text=_(f"🛍 Savat", locale=user[4])))
    userga = f"😋 {message.text} {_('menyu', locale=user[4])}"
    for food in menu_foods:
        foods.insert(KeyboardButton(text=food['name']))
    await message.answer(text=userga, reply_markup=foods)
    await state.set_state('in_food')


@dp.message_handler(state=f'in_food')
async def in_food_handler(message: types.Message, state: FSMContext):
    user = await get_user(message.chat.id)
    food = await menu_functions(lang=user[4], work='GET_FOOD', name=message.text)
    await state.update_data({
        'loc': 'got_food',
        'menu': food['menu'],
        'food': food['name'],
    })
    desc = _('Taom haqida', locale=user['lang'])
    userga1 = _(f"Taom", locale=user['lang'])
    price = _('Taom narxi', locale=user['lang'])
    userga = f"""
😋 {userga1}: {food['name']}

‼️ {desc} ‼️

- <b>{food['description']}</b>

💰 {price}: <b>{food['price']}</b>
"""
    await message.answer(text=userga1, reply_markup=await back_button(user[4]))
    await message.answer_photo(photo=food['photo'], caption=userga,
                               reply_markup=await plus_minus(count=0, sum=0, food=food['name'], price=food['price']))
    await state.set_state('got_food')


@dp.callback_query_handler(state='got_food')
async def plus_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = await get_user(call.message.chat.id)
    if call.data.split("_")[0] == "plus":
        await basket_functions(name=call.data.split("_")[1], chat_id=call.message.chat.id, work="ADD",
                               price=call.data.split('_')[2])
        new = await basket_functions(work="GET_FOOD", name=call.data.split("_")[1], chat_id=call.message.chat.id)
        await call.message.edit_reply_markup(
            reply_markup=await plus_minus(count=new['quantity'], sum=new['price'] * new['quantity'],
                                          food=call.data.split('_')[1], price=call.data.split('_')[2]))
        await state.set_state('got_food')
    elif call.data.split("_")[0] == "minus":
        food = await basket_functions(work='MINUS', name=call.data.split('_')[1], chat_id=call.message.chat.id, lang=user[4])
        if food == True:
            new = await basket_functions(work="GET_FOOD", name=call.data.split("_")[1], chat_id=call.message.chat.id)
            await call.message.edit_reply_markup(reply_markup=await plus_minus(count=new['quantity'], sum=new['price'] * new['quantity'],
                                              food=call.data.split('_')[1], price=call.data.split('_')[2]))
            await state.set_state('got_food')
        elif food == None:
            userga = _(f"😕 Kechirasiz. Mahsulotni 1 taga kamaytirish uchun, mahsulot kamida 1 dona bolishi kerak!",
                       locale=user['lang'])
            await call.answer(text=userga, show_alert=True)
            await state.set_state('got_food')
        else:
            await call.message.delete()
            await call.message.answer(text=_('✅ Mahsulot savatingizdan olib tashlandi.'), reply_markup=await main_menu(lang=user['lang']))
            await state.set_state('in_start')