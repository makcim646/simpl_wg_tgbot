from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import *

setting = get_config()

bot = Bot(setting['bot_token']) #Telegram bot token
admin = int(setting['admin_id']) #admin tgid
dp = Dispatcher(bot)


@dp.message_handler(commands=['adduser'])
async def add_user(message: types.Message):
    if message.chat.id == admin:
        try:
            client_name = message.text.split(' ')[1]
        except:
            await bot.send_message(message.chat.id, 'ты не ввел имя пользователя')
            return
        
        button1 = InlineKeyboardButton("Подключить с ipv6", callback_data=f'connect_{client_name}_yes')
        button2 = InlineKeyboardButton("Подключить без ipv6", callback_data=f'connect_{client_name}_no')
        otvet = InlineKeyboardMarkup().add(button1, button2)
        await message.answer(F"Подключить пользователя {client_name}", reply_markup=otvet)
            


@dp.callback_query_handler(lambda c: c.data[:7] == 'connect')
async def connect_user(callback: types.CallbackQuery):
    id_user = callback.from_user.id
    print(callback.data.split('_'))
    if id_user == admin:
        _, client_name, ygg = callback.data.split('_')
        if ygg == 'yes':
            print(client_name, ygg)
            """"if root_add(client_name, True):
                with open(f'png/{client_name}.png', 'rb') as pfoto:
                    await bot.send_photo(id_user, pfoto)
                with open(f'conf/{client_name}.conf', 'rb') as file:
                    await bot.send_document(id_user, file)
            else:
                await bot.send_message(id_user, 'Не удалось добавить')"""
        else:
            print(client_name, ygg)
            """if root_add(client_name):
                with open(f'png/{client_name}.png', 'rb') as pfoto:
                    await bot.send_photo(id_user, pfoto)
                with open(f'conf/{client_name}.conf', 'rb') as file:
                    await bot.send_document(id_user, file)
            else:
                await bot.send_message(id_user, 'Не удалось добавить')"""


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

        text = "Connected clients:\n "
        for c in clients:
            if c[0] != '':
                text += f'\- `{c[0]}`\n'
                for ip in c[1].split(','):
                    ip_adr, mask = ip.split('/') if '/' in ip else [ip, '']
                    ip_v = 'ipv6' if '::' in ip_adr else 'ipv4'
                    text += f'\t{ip_v}`{ip_adr}`/{mask}\n'

        await message.answer(text, parse_mode='MarkdownV2')


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
