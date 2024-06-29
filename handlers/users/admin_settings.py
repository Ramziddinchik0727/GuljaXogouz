from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from keyboards.default.admin_keyboards import menu_settings, admins_panel
from keyboards.default.users_keyboards import cancel
from loader import dp, types
from translator import translations
from utils.db_api.database_settings import is_admin, menu_functions, user_settings, basket_functions
from utils.messages import you_are_not_admin, have_error


@dp.message_handler(text=f"🍴 Menyu sozlamalari")
async def menu_settings_handler(message: types.Message, state: FSMContext):
    if await is_admin(message.chat.id):
        await message.answer(text=f"😊 Menyu sozlamalari", reply_markup=menu_settings)
        await state.set_state("in_menu_settings")
    else:
        await you_are_not_admin(message)
        await state.finish()


@dp.message_handler(state='in_menu_settings')
async def menu_settings_handler(message: types.Message, state: FSMContext):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton(text='❌ Bekor qilish'))
    menu.row_width = 2
    for i in await menu_functions(lang='uz'):
        menu.add(i[1])
    if message.text[0] == "➕":
        await message.answer(text=f"😊 Yangi taomni qaysi menyuga qoshmoqchisiz?", reply_markup=menu)
        await state.set_state("select_menu")
    elif message.text[0] == "🚫":
        await message.answer(text=f"😊 Olib tashlamoqchi bo'lgan taomingiz qaysi menyuda joylashgan?", reply_markup=menu)
        await state.set_state('select_menu_to_delete_food')
    elif message.text[0:2] == "🔧💰":
        await message.answer(text=f"😊 Narxini oz'gartirmoqchi bo'lgan taomingiz qaysi menyuda joylashgan?",
                             reply_markup=menu)
        await state.set_state('select_menu_to_change_food_price')
    elif message.text[0:2] == "🍴➕":
        await message.answer(text=f"😊 Yangi menu nomini kiriting.", reply_markup=await cancel(lang='uz'))
        await state.set_state('enter_new_menu_name')
    elif message.text[0:2] == "🍴🚫":
        await message.answer(text=f"😊 Ochirmoqchi bo'lgan menyuingizni tanlang.", reply_markup=menu)
        await state.set_state('select_menu_to_delete')
    else:
        pass

@dp.message_handler(state='select_menu_to_delete', content_types=types.ContentTypes.TEXT)
async def select_menu_to_delete_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await menu_functions(work='DELETE_MENU', data=await state.get_data())
    await message.answer(text=f"😊 Menyu muvaffaqqiyatli ochirib yuborildi.", reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(state='enter_new_menu_name', content_types=types.ContentTypes.TEXT)
async def enter_new_menu_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await menu_functions(work='ADD_MENU', data=await state.get_data())
    await message.answer(text=f"😊 Yangi menu muvaffaqqiyatli qo'shildi.", reply_markup=admins_panel)
    await state.finish()




@dp.message_handler(state='select_menu_to_change_food_price')
async def select_menu_to_change_food_price_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu': message.text
    })
    foods = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    foods.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    foods.row_width = 2
    for food in await menu_functions(lang='uz', work='GET_FOODS', menu_name=message.text):
        foods.insert(KeyboardButton(text=food['name']))
    await message.answer(text=f"😊 {message.text} menyusidagi qaysi taomni narxini o'zgartirmoqchisiz?",
                         reply_markup=foods)
    await state.set_state('select_food_to_change_price')


@dp.message_handler(state='select_food_to_change_price', content_types=types.ContentTypes.TEXT)
async def select_food_to_change_price(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=f"😊 {message.text} taomiga yangi narx belgilang.", reply_markup=await cancel(lang='uz'))
    await state.set_state('enter_price_change_food_price')


@dp.message_handler(state='enter_price_change_food_price')
async def enter_price_change_food_price_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            'price': int(message.text)
        })
        data = await state.get_data()
        await menu_functions(work='CHANGE_PRICE', data=data)
        await message.answer(text=f"😊{data['name']} taom narxi {message.text} so'mga o'zgartirildi")
        await state.finish()
    except Exception as e:
        await message.answer(text=f"😕 Kechirasiz. Taom narxini faqat butun sonlarda kiritish mumkin.")
        await state.set_state('enter_price_change_food_price')


@dp.message_handler(state='select_menu_to_delete_food', content_types=types.ContentType.TEXT)
async def delete_food(message: types.Message, state: FSMContext):
    await state.update_data({
        'menu': message.text
    })
    foods = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    foods.insert(KeyboardButton(text=f"❌ Bekor qilish"))
    foods.row_width = 2
    for food in await menu_functions(lang='uz', work='GET_FOODS', menu_name=message.text):
        foods.insert(KeyboardButton(text=food['name']))
    await message.answer(text=f"😊 {message.text} menyudagi qaysi taomni olib tashamoqchisiz?", reply_markup=foods)
    await state.set_state('select_food_to_delete')


@dp.message_handler(state='select_food_to_delete', content_types=types.ContentType.TEXT)
async def select_food_to_delete_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await basket_functions(work='DELETE_FOR', name=message.text)
    await menu_functions(work='DELETE', data=await state.get_data())
    await message.answer(text=f"😊 Taom muvaffaqqiyatli ochirildi.", reply_markup=admins_panel)
    await state.finish()


@dp.message_handler(state='select_menu', content_types=types.ContentType.TEXT)
async def enter_new_meal_name_handler(message: types.Message, state: FSMContext):
    menu = await menu_functions(work='GET_MENU_TO_ADD_MEAL', menu_name=message.text)
    if menu is not None:
        await state.update_data({
            'menu': menu['name_to_get']
        })
        await message.answer(text=f'😊 Yangi taom nomini kiriting.', reply_markup=await cancel(lang='uz'))
        await state.set_state("enter_new_meal_name")
    else:
        await message.answer(text=f"😕 Kechirasiz menyu topilmadi.", reply_markup=admins_panel)
        await have_error(error='Menu not found', line='143')
        await state.finish()


@dp.message_handler(state='enter_new_meal_name', content_types=types.ContentType.TEXT)
async def enter_new_meal_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'name': message.text
    })
    await message.answer(text=f"😊 Yangi taom haqida ma'lumot kiriting.")
    await state.set_state("write_new_meal_description")


@dp.message_handler(state='write_new_meal_description', content_types=types.ContentType.TEXT)
async def write_new_meal_description_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'description': message.text
    })
    await message.answer(text=f"😊 Yangi taom narxini kiriting.")
    await state.set_state("enter_new_meal_price")


@dp.message_handler(state='enter_new_meal_price', content_types=types.ContentType.TEXT)
async def enter_new_meal_price_handler(message: types.Message, state: FSMContext):
    try:
        await state.update_data({
            'price': int(message.text)
        })
        await message.answer(text=f"😊 Yangi taom rasmini yuboring.")
        await state.set_state('send_new_meal_photo')
    except ValueError:
        await message.answer(text=f"😟 Kechirasiz. Taom narxini faqat butun sonlarda kiritish mumkin. \nMasalan: 50000")
        await state.set_state("enter_new_meal_price")
    except Exception as e:
        await have_error(error=e, message=message, line=177)
        await state.finish()


@dp.message_handler(state='send_new_meal_photo', content_types=types.ContentType.PHOTO)
async def send_new_meal_photo_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'photo': message.photo[-1].file_id
    })

    await menu_functions(work='ADD', data=await state.get_data())
    await message.answer(text=f"😊 Yangi taom qo'shildi.", reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(text=f"📝️ Xabar yuborish")
async def send_messages_for_users(message: types.Message, state: FSMContext):
    await message.answer(text=f"😊 Foydaanuvchilarga xabar kiriting.", reply_markup=await cancel(lang='uz'))
    await state.set_state("enter_text")

@dp.message_handler(state='enter_text')
async def enter_photo_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        'message': message.text
    })
    await message.answer(text=f"😊 Iltimos rasm kiriting", reply_markup=await cancel(lang='uz'))
    await state.set_state('send_photo')

@dp.message_handler(state='send_photo', content_types=types.ContentTypes.PHOTO)
async def send_for_users_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=f"😊 Foydalanuvchilarga xabar yuborilmoqda.", reply_markup=ReplyKeyboardRemove())
    for user in await user_settings(work='GET'):
        try:
            await dp.bot.send_photo(photo=message.photo[-1].file_id, caption=data['message'], chat_id=user['chat_id'])
        except:
            pass
    await message.answer(text=f"😊 Foydalanuvchilarga xabar yuborildi.", reply_markup=admins_panel)
    await state.finish()

@dp.message_handler(text='👥 Bot foydalanuvchilari')
async def bot_users_handler(message: types.Message, state: FSMContext):
    adminga = f"😊 Barcha userlar\n\n"
    users = await user_settings(work='GET')
    flag = ""
    count = 0
    for user in users:
        if user['lang'] == "zh":
            flag = f"🇨🇳"
        elif user['lang'] == "uz":
            flag = "🇺🇿"
        elif user['lang'] == "ru":
            flag = f"🇷🇺"
        else:
            flag = f"🇺🇸"
        count += 1
        adminga += f" {flag} <b>@{user['username']}</b> <b>{user['phone_number']}</b>\n"
    adminga += f"\n👥 Ja'mi: {count}"
    await message.answer(text=adminga)

