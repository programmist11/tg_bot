from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove

from config_reader import config
from create_bot import bot, dp
from data_base import sqlite_db
from keyboards import kb_client


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, "Приятного аппетита", reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply("Общение с ботом через ЛС, напишите ему:\nhttps://t.me/ignat_23_bot")


async def command_timetable(message: types.Message):
    await bot.send_message(message.from_user.id, "Пн-Сб с 8:00 до 17:00, Вс с 8:00 до 12:00")


async def command_place(message: types.Message):
    await bot.send_location(message.from_user.id,
                            latitude=config.latitude.get_secret_value(),
                            longitude=config.longitude.get_secret_value()
                            )


async def command_menu(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_timetable, commands=['Режим_работы'])
    dp.register_message_handler(command_place, commands=['Расположение'])
    dp.register_message_handler(command_menu, commands=['Меню'])