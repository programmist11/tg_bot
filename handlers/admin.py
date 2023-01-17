from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, dp
from data_base.sqlite_db import sql_add_command
from keyboards import admin_kb

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(chat_id=ID, text="Что надо хозяин?", reply_markup=admin_kb.kb_admin)
    await message.delete()


async def cm_start(message: types.Message):
    if ID == message.from_user.id:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')


async def cancel_handlers(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


async def load_photo(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:

            data['photo'] = message.photo[0].file_id

        await FSMAdmin.next()
        await message.reply("Теперь введи название")


async def load_name(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание")


async def load_description(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи цену")


async def load_price(message: types.Message, state: FSMContext):
    if ID == message.from_user.id:
        async with state.proxy() as data:
            try:
                data['price'] = float(message.text)
            except:
                await state.finish()
                await message.reply('Ошибка')
                return

        await sql_add_command(state)
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handlers, state="*", commands='отмена')
    dp.register_message_handler(cancel_handlers, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
