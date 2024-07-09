from main.models import *
from main.database_set import database
from translator import translate_uz_to_ru, translate_uz_to_en, translate_uz_to_zh


async def add_user(data: dict):
    return await database.execute(query=users.insert().values(
        full_name=data.get('full_name'),
        phone_number=data.get('phone_number'),
        chat_id=data.get('chat_id'),
        username=data.get('username'),
        lang=data.get('lang'),
        created_at=data.get('created_at')
    ))

async def user_settings(lang=None, work=None, full_name=None, phone_number=None, username=None, chat_id=None):
    if work == f"UPDATE_LANG":
        return await database.execute(query=users.update().values(
            lang=lang,
        ).where(users.c.chat_id == chat_id))
    elif work == f"UPDATE_PHONE_NUMBER":
        return await database.execute(query=users.update().values(
            phone_number=phone_number
        ).where(users.c.chat_id == chat_id))
    elif work == 'UPDATE_FULL_NAME':
        return await database.execute(query=users.update().values(
            full_name=full_name
        ).where(users.c.chat_id == chat_id))
    elif work == None:
        return await database.execute(query=users.update().values(
            username=username
        ))
    elif work == 'GET':
        return await database.fetch_all(query=users.select())

async def payment_functions(work=None):
    if work == f"GET":
        return await database.fetch_all(query=payemnts.select())

async def menu_functions(lang=None, work=None, menu_name=None, name=None, data: dict = None, ):
    if work is None:
        return await database.fetch_all(query=menu.select().where(menu.c.lang == lang).order_by(menu.c.id))
    elif work == "GET_FOODS":
        menuu = await database.fetch_one(query=menu.select().where(menu.c.name == menu_name))
        return await database.fetch_all(query=foods.select().where(foods.c.menu == menuu['name_to_get'], foods.c.lang == lang).order_by(foods.c.id))
    elif work == "GET":
        return await database.fetch_all(query=foods.select().where(foods.c.lang == lang).order_by(foods.c.id))
    elif work == "GET_FOOD":
        return await database.fetch_one(query=foods.select().where(foods.c.name == name))
    elif work == "GET_MENU_TO_ADD_MEAL":
        return await database.fetch_one(query=menu.select().where(menu.c.name == menu_name, menu.c.name_to_get == menu_name))
    elif work == 'DELETE_MENU':
        return await database.execute(query=menu.delete().where(menu.c.name_to_get == data['name']))
    elif work == 'GET_FOR':
        food = await database.fetch_one(query=foods.select().where(foods.c.name == name))
        return await database.fetch_one(query=foods.select().where(foods.c.lang == 'uz', foods.c.photo == food['photo']))
    elif work == 'ADD_MENU':
        await database.execute(query=menu.insert().values(name=data['name'], lang='uz', name_to_get=data['name']))
        await database.execute(query=menu.insert().values(name=translate_uz_to_ru(text=data['name']), lang='ru', name_to_get=data['name']))
        await database.execute(query=menu.insert().values(name=translate_uz_to_en(text=data['name']), lang='en', name_to_get=data['name']))
        await database.execute(query=menu.insert().values(name=translate_uz_to_zh(text=data['name']), lang='zh', name_to_get=data['name']))
        return True
    elif work == 'DELETE':
        food = await database.fetch_one(query=foods.select().where(foods.c.name == data['name'], foods.c.menu == data['menu'], foods.c.lang=='uz'))
        return await database.execute(query=foods.delete().where(foods.c.photo == food['photo']))
    elif work == 'CHANGE_PRICE':
        food = await database.fetch_one(query=foods.select().where(foods.c.name == data['name'], foods.c.menu == data['menu'], foods.c.lang=='uz'))
        return await database.execute(query=foods.update().values(
            price=data['price']
        ).where(foods.c.photo == food['photo']))
    elif work == 'ADD':
        await database.execute(query=foods.insert().values(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            photo=data['photo'],
            menu=data['menu'],
            lang='uz'
        ))
        await database.execute(query=foods.insert().values(
            name=translate_uz_to_ru(text=data['name']),
            description=translate_uz_to_ru(text=data['description']),
            price=data['price'],
            photo=data['photo'],
            menu=data['menu'],
            lang='ru'
        ))
        await database.execute(query=foods.insert().values(
            name=translate_uz_to_en(text=data['name']),
            description=translate_uz_to_en(text=data['description']),
            price=data['price'],
            photo=data['photo'],
            menu=data['menu'],
            lang='en'
        ))
        await database.execute(query=foods.insert().values(
            name=translate_uz_to_zh(text=data['name']),
            description=translate_uz_to_zh(text=data['description']),
            price=data['price'],
            photo=data['photo'],
            menu=data['menu'],
            lang='zh'
        ))
        return True


async def update_menu_functions(lang=None, work=None, menu_name=None, photo=None):
    return await database.execute(query=foods.update().values(photo=photo))

async def get_admins():
    return await database.fetch_all(query=admins.select())

async def basket_functions(lang=None, work=None, name=None, chat_id=None, price=None):
    if work == 'GET_FOOD':
        return await database.fetch_one(
            query=basket.select().where(basket.c.product == name, basket.c.chat_id == chat_id))
    elif work == 'GET':
        return await database.fetch_all(query=basket.select().where(basket.c.chat_id == chat_id))
    elif work == 'DELETE_BASKET':
        return await database.execute(query=basket.delete().where(basket.c.chat_id == chat_id))
    elif work == 'DELETE_FOR': # This function also removes the food removed through the admin panel from the cart.
        food1 = await database.fetch_one(query=foods.select().where(basket.c.product == translate_uz_to_ru(text=name)))
        food2 = await database.fetch_one(query=foods.select().where(basket.c.product == translate_uz_to_en(text=name)))
        food3 = await database.fetch_one(query=foods.select().where(basket.c.product == translate_uz_to_zh(text=name)))
        await database.execute(query=basket.delete().where(basket.c.product == food1['name']))
        await database.execute(query=basket.delete().where(basket.c.product == food2['name']))
        await database.execute(query=basket.delete().where(basket.c.product == food3['name']))
        return True

    elif work == 'DELETE':
        return await database.execute(query=basket.delete().where(basket.c.product == name, basket.c.chat_id == chat_id))
    elif work == "ADD":
        food = await database.fetch_one(
            query=basket.select().where(basket.c.product == name, basket.c.chat_id == chat_id))
        if food is not None:
            return await database.execute(query=basket.update().values(
                quantity=food[2] + 1
            ).where(basket.c.product == name, basket.c.chat_id == chat_id))
        else:
            return await database.execute(query=basket.insert().values(
                quantity=1,
                chat_id=chat_id,
                product=name,
                price=int(price)
            ))
    elif work == "MINUS":
        food = await database.fetch_one(query=basket.select().where(basket.c.product == name, basket.c.chat_id == chat_id))
        if food is not None:
            if food[2] == 1:
                await database.execute(query=basket.delete().where(
                    basket.c.id == food['id']
                ))
                return False
            else:
                await database.execute(query=basket.update().values(
                    quantity=food[2] - 1
                ).where(basket.c.product == name, basket.c.chat_id == chat_id))
                return True
        else:
            return None



async def is_admin(user_id: int):
    return await database.fetch_one(query=admins.select().where(admins.c.chat_id == user_id))


async def get_user(chat_id: int):
    return await database.fetch_one(query=users.select().where(users.c.chat_id == chat_id))
