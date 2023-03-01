from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db import *



bot = Bot("") #Telegram bot token
admin = 000000 #admin tgid
dp = Dispatcher(bot)


@dp.message_handler(commands=['adduser'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await bot.send_message(message.chat.id, 'ты не ввел имя пользователя')
            return
      
        if root_add(id_user):
            with open(f'png/{id_user}.png', 'rb') as pfoto:
                await bot.send_photo(message.chat.id, pfoto)
            with open(f'conf/{id_user}.conf', 'rb') as file:
                await bot.send_document(message.chat.id, file)
           
        else:
            await bot.send_message(message.chat.id, 'Не удалось добавить')
            


@dp.message_handler(commands=['remove'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await message.answer('ты не ввел имя пользователя')
            return

        if deactive_user_db(id_user):
            await message.answer(f'пользователь {id_user} удален')
        else:
            await message.answer('неудалось удалить')
       


@dp.message_handler(commands=['client'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        clients = get_client_list()

        text = "Connected clients:\n- "
        for c in clients:
            if c[0] != '':
                ipv4, ipv6 = c[1].split(',')
                text += f'{c[0]}\n'
                text += f'\t{ipv4}\n'
                text += f'\t{ipv6}\n'

        await message.answer(text)


@dp.message_handler(commands=['getconfig'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            id_user = message.text.split(' ')[1]
        except:
            await message.answer('ты не ввел имя пользователя')
            return

        try:
            with open(f'png/{id_user}.png', 'rb') as pfoto:
                await bot.send_photo(message.chat.id, pfoto)
            with open(f'conf/{id_user}.conf', 'rb') as file:
                await bot.send_document(message.chat.id, file)
        except:
            await message.answer('неудалось найти конфиг')


@dp.message_handler(commands=['help'])
async def send_curs(message: types.Message):
    if message.chat.id == admin:
        text = """команды бота:
        /adduser user_name добавлять пользователя и отпраляет .conf файл и qr-code
        /remove user_name удаляет пользователя
        /getconfig user_name прищлет конфиг пользователя
        /client выводит список клиентов"""
        await message.answer(text)


@dp.message_handler()
async def send_curs(message: types.Message):
    if message.chat.id == admin:
        await message.answer('Я жив')


if __name__ == '__main__':
    executor.start_polling(dp)
