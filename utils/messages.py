from keyboards.default.admin_keyboards import admins_panel
from loader import dp, types


async def have_error(message=None, error=None, line=None):
    error_message = f"Error: \n\n{error}\n\nBot: GuljaXogo\n\nLine: {line}"
    if message:
        await message.answer(text=f"😕 Kechirasiz botda xatolik yuz berdi.", reply_markup=admins_panel)
    await dp.bot.send_message(chat_id=-1002075245072, text=error_message)

async def you_are_not_admin(message: types.Message):
    await message.answer(text='😕 Kechirasiz siz adminik huquqiga ega emassiz. Bu funksiya faqat adminlar uchun!')