from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import logging
import sqlite3
import openai
import traceback
from deep_translator import GoogleTranslator
from glQiwiApi import QiwiWrapper, types as qiwi_types
from glQiwiApi import QiwiP2PClient
from glQiwiApi.qiwi.clients.p2p.types import Bill

openai.api_key = ''
model_engine = 'text-davinci-003'
max_tokens = 128

qiwi_p2p_client = QiwiP2PClient(secret_p2p="")

API_TOKEN = ''

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

kbadm = types.ReplyKeyboardMarkup(resize_keyboard=True)
kbadm.add(types.InlineKeyboardButton(text="Рассылка📤"))
kbadm.add(types.InlineKeyboardButton(text="Статистика💭"))
kbadm.add(types.InlineKeyboardButton(text="Обновить попытки🚨"))
kbadm.insert(KeyboardButton(text='БДшка✨'))
kbadm.insert(KeyboardButton(text='Пробив пользователя🧦'))

kbusr = ReplyKeyboardMarkup(resize_keyboard=True)
kbusr.add(types.KeyboardButton('Написать сочинение ⚡️'))
kbusr.add(types.KeyboardButton('Магазин 💰'))
kbusr.add(types.KeyboardButton('Помощь 🧑‍💻'))
kbusr.add(types.KeyboardButton('Пригласить друга 💗'))
kbusr.insert(KeyboardButton('Профиль 👤'))

ikbusr = InlineKeyboardMarkup()
ikbusr.add(types.InlineKeyboardButton('Написать саппорту🐱‍🚀', url='https://t.me/bluefish1488'))
ikbusr.add(types.InlineKeyboardButton('Наша группа⚡', url='https://t.me/FalafelNotBot'))

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, name INTEGER, quest INTEGER, attempts INTEGER, 
ref INTEGER, link INTEGER);""")
conn.commit()

class UserState(StatesGroup):
    name = State()
    spam = State()
    dialog = State()
    check = State()
    attempts = State()
    usrcheck = State()
    openaii = State()
    pay = State()
    oper = State()
    opermess = State()
    correct = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
        cur = conn.cursor()
        chat_admins = await bot.get_chat_administrators(-1001657487556)
        admid = list()
        for admins in chat_admins:
            userId = admins.user.id
            admid.append(userId)
        if message.from_user.id in admid:
            await message.answer('🎯Добро пожаловать в админку!', reply_markup=kbadm)
        else:
            try:
                ref = message.text.split('/start ')
                cur.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
                result = cur.fetchall()
                if len(result) == 0:
                    cur.execute(f'''INSERT INTO users (user_id, name, quest, attempts, ref, link) VALUES (
                    '{message.from_user.id}',
                    '{message.from_user.username}', 0, 3, {ref[1]}, 'https://ro8lox.com/groups/2002993832/')''')
                    cur.execute(f"SELECT name FROM users WHERE user_id = {ref[1]}")
                    refr = cur.fetchone()
                    conn.commit()
                    await message.answer("Привет✨", reply_markup=kbusr)
                    inline_ref = InlineKeyboardButton('🧥Промоутер', url=f'tg://openmessage?user_id={ref[1]}')
                    inline_ref2 = InlineKeyboardButton('🧤Реферал', url=f'tg://openmessage?user_id'
                                                                      f'={message.from_user.id}')
                    inref = InlineKeyboardMarkup().add(inline_ref, inline_ref2)
                    await bot.send_message(-1001657487556, f'{ref[1]} | #{refr[0]} привел реферала\n'
                                                       f'{message.from_user.id} | @{message.from_user.username}',
                                           reply_markup=inref)
                    cur.execute(f"UPDATE users SET attempts = attempts + 1 WHERE user_id = {ref[1]}")
                    await bot.send_message(ref[1], '✅Вы привели друга, за это мы начислили вам 1 попытку!')
                    conn.commit()
                else:
                    await message.answer("Привет✨", reply_markup=kbusr)
            except:
                    cur.execute(f"SELECT user_id FROM users WHERE user_id = {message.from_user.id}")
                    result = cur.fetchall()
                    if len(result) == 0:
                        cur.execute(f'''INSERT INTO users (user_id, name, quest, attempts, link) VALUES (
                        '{message.from_user.id}',
                        '{message.from_user.username}', 0, 1, 1)''')
                        conn.commit()
                        await message.answer("Привет✨", reply_markup=kbusr)
                    else:
                        await message.answer("Привет✨", reply_markup=kbusr)

@dp.message_handler(content_types=['text'], text='Магазин 💰')
async def process_help_text(message: types.Message, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        ikbpay= InlineKeyboardMarkup()
        ikbpay.add(types.InlineKeyboardButton('Купить 10 попыток💸', callback_data='29rub'))
        ikbpay.add(types.InlineKeyboardButton('Купить 50 попыток💸', callback_data='99rub'))
        ikbpay.add(types.InlineKeyboardButton('Купить 100 попыток💸', callback_data='159rub'))
        ikbpay.add(types.InlineKeyboardButton('Купить БЕЗЛИМИТ🪙', callback_data='349rub'))
        await message.reply('\n*➖➖➖💎Пр@йс💎➖➖➖*\n\n10 попыток | *29 ₽* |\n50 попыток | *99 ₽* |\n100 попыток | *159 '
                            '₽* |\nБЕЗЛИМИТ'
                            '| *349 ₽* |', parse_mode='markdown', reply_markup=ikbpay)
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.callback_query_handler(text='29rub')
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with qiwi_p2p_client:
        bill = await qiwi_p2p_client.create_p2p_bill(amount=29)
    ikbpayurl = InlineKeyboardMarkup()
    ikbpayurl.add(types.InlineKeyboardButton('Перейти на сайт оплаты🥇', url=bill.pay_url))
    ikbpayurl.add(types.InlineKeyboardButton('Проверить оплату✅', callback_data='paystatus'))
    ikbpayurl.add(types.InlineKeyboardButton('Отменить оплату❌', callback_data='payabort'))
    await callback.message.answer('*Вот ваша форма для оплаты*', reply_markup=ikbpayurl, parse_mode='markdown')
    await UserState.pay.set()
    await state.update_data(bill=bill)

@dp.callback_query_handler(text='payabort', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(f'Отказ оплаты', reply_markup=kbusr)
        await state.finish()

@dp.callback_query_handler(text='paystatus', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: Bill = data.get("bill")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await callback.message.answer(f'Спасибо братишка! Оплачу сервак и куплю поxавать!', reply_markup=kbusr)
        await state.finish()
        await bot.send_message(-1001657487556, f'🎃 @{callback.from_user.username} *закинул 29 рублев*',
                               parse_mode="Markdown")
        cur = conn.cursor()
        cur.execute(f'''UPDATE users SET attempts = attempts + 10 WHERE user_id = ('{callback.from_user.id}')''')
    else:
        await callback.message.answer(f'Счет не оплачен!', reply_markup=kbusr)

@dp.callback_query_handler(text='99rub')
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with qiwi_p2p_client:
        bill = await qiwi_p2p_client.create_p2p_bill(amount=99)
    ikbpayurl = InlineKeyboardMarkup()
    ikbpayurl.add(types.InlineKeyboardButton('Перейти на сайт оплаты🥇', url=bill.pay_url))
    ikbpayurl.add(types.InlineKeyboardButton('Проверить оплату✅', callback_data='paystatus'))
    ikbpayurl.add(types.InlineKeyboardButton('Отменить оплату❌', callback_data='payabort'))
    await callback.message.answer('*Вот ваша форма для оплаты*', reply_markup=ikbpayurl, parse_mode='markdown')
    await UserState.pay.set()
    await state.update_data(bill=bill)

@dp.callback_query_handler(text='payabort', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(f'Отказ оплаты', reply_markup=kbusr)
        await state.finish()

@dp.callback_query_handler(text='paystatus', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: Bill = data.get("bill")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await callback.message.answer(f'Спасибо братишка! Оплачу сервак и куплю поxавать!', reply_markup=kbusr)
        await state.finish()
        await bot.send_message(-1001657487556, f'🎃 @{callback.from_user.username} *закинул 99 рублев*',
                               parse_mode="Markdown")
        cur = conn.cursor()
        cur.execute(f'''UPDATE users SET attempts = attempts + 50 WHERE user_id = ('{callback.from_user.id}')''')
    else:
        await callback.message.answer(f'Счет не оплачен!', reply_markup=kbusr)

@dp.callback_query_handler(text='159rub')
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with qiwi_p2p_client:
        bill = await qiwi_p2p_client.create_p2p_bill(amount=159)
    ikbpayurl = InlineKeyboardMarkup()
    ikbpayurl.add(types.InlineKeyboardButton('Перейти на сайт оплаты🥇', url=bill.pay_url))
    ikbpayurl.add(types.InlineKeyboardButton('Проверить оплату✅', callback_data='paystatus'))
    ikbpayurl.add(types.InlineKeyboardButton('Отменить оплату❌', callback_data='payabort'))
    await callback.message.answer('*Вот ваша форма для оплаты*', reply_markup=ikbpayurl, parse_mode='markdown')
    await UserState.pay.set()
    await state.update_data(bill=bill)

@dp.callback_query_handler(text='payabort', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(f'Отказ оплаты', reply_markup=kbusr)
        await state.finish()

@dp.callback_query_handler(text='paystatus', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: Bill = data.get("bill")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await callback.message.answer(f'Спасибо братишка! Оплачу сервак и куплю поxавать!', reply_markup=kbusr)
        await state.finish()
        await bot.send_message(-1001657487556, f'🎃 @{callback.from_user.username} *закинул 159 рублев*',
                               parse_mode="Markdown")
        cur = conn.cursor()
        cur.execute(f'''UPDATE users SET attempts = attempts + 100 WHERE user_id = ('{callback.from_user.id}')''')
    else:
        await callback.message.answer(f'Счет не оплачен!', reply_markup=kbusr)

@dp.callback_query_handler(text='349rub')
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with qiwi_p2p_client:
        bill = await qiwi_p2p_client.create_p2p_bill(amount=349)
    ikbpayurl = InlineKeyboardMarkup()
    ikbpayurl.add(types.InlineKeyboardButton('Перейти на сайт оплаты🥇', url=bill.pay_url))
    ikbpayurl.add(types.InlineKeyboardButton('Проверить оплату✅', callback_data='paystatus'))
    ikbpayurl.add(types.InlineKeyboardButton('Отменить оплату❌', callback_data='payabort'))
    await callback.message.answer('*Вот ваша форма для оплаты*', reply_markup=ikbpayurl, parse_mode='markdown')
    await UserState.pay.set()
    await state.update_data(bill=bill)

@dp.callback_query_handler(text='payabort', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer(f'Отказ оплаты', reply_markup=kbusr)
        await state.finish()

@dp.callback_query_handler(text='paystatus', state=UserState.pay)
async def process_help_text(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        bill: Bill = data.get("bill")
    if await qiwi_p2p_client.check_if_bill_was_paid(bill):
        await callback.message.answer(f'Спасибо братишка! Оплачу сервак и куплю поxавать!', reply_markup=kbusr)
        await state.finish()
        await bot.send_message(-1001657487556, f'🎃 @{callback.from_user.username} *закинул 349 рублев*',
                               parse_mode="Markdown")
        
        cur = conn.cursor()
        cur.execute(f'''UPDATE users SET attempts = attempts + 9999999999999 WHERE user_id = (
        '{callback.from_user.id}')''')
    else:
        await callback.message.answer(f'Счет не оплачен!', reply_markup=kbusr)

@dp.message_handler(content_types=['text'], text='Профиль 👤')
async def process_help_text(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        cur = conn.cursor()
        cur.execute(f"SELECT attempts FROM users WHERE user_id = {message.from_user.id}")
        resatm = cur.fetchone()
        cur.execute(f"SELECT COUNT(ref) from users where ref = '{message.from_user.id}'")
        rescou = cur.fetchone()
        await message.answer(f"*└ Айди -* `{message.from_user.id}`\n*└ Попытки -* "f"{resatm[0]}\n*└ Рефералов - "
                             f"{rescou[0]}*",
                             parse_mode='markdown')
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(content_types=['text'], text='Помощь 🧑‍💻')
async def process_help_text(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.reply(f'*Правила обращения в Техническую Поддержку:\n🔹1. Представьтесь, изложите проблему своими '
                            'словами - мы постараемся Вам помочь\n🔹2. Напишите свой ID - нам это нужно, чтобы увидеть '
                            'ваш профиль, и узнать актуальность вашей проблемы.\n🔹3. Будьте вежливы, '
                            'наши консультанты не роботы, мы постараемся помочь Вам, и сделать все возможное, '
                            'чтобы сберечь ваше время и обеспечить максимальную оперативность в работе.\nНапишите '
                            f'нам, ответ Поддержки, не заставит вас долго ждать!\n🔹4. Ваш ID -* '
                            f'`{message.from_user.id}`',
                            reply_markup=ikbusr, parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.reply(f'*Правила обращения в Техническую Поддержку:\n🔹1. Представьтесь, изложите проблему своими '
                            'словами - мы постараемся Вам помочь\n🔹2. Напишите свой ID - нам это нужно, чтобы увидеть '
                            'ваш профиль, и узнать актуальность вашей проблемы.\n🔹3. Будьте вежливы, '
                            'наши консультанты не роботы, мы постараемся помочь Вам, и сделать все возможное, '
                            'чтобы сберечь ваше время и обеспечить максимальную оперативность в работе.\nНапишите '
                            f'нам, ответ Поддержки, не заставит вас долго ждать!\n🔹4. Ваш ID -* '
                            f'`{message.from_user.id}`',
                            reply_markup=ikbusr, parse_mode="Markdown")
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(commands=['menu'])
async def process_menu_command(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.answer('Кнопки', reply_markup=kbusr)
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(commands=['unmenu'])
async def process_menu_command(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.answer('Кнопки', reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(content_types=['text'], text='Пробив пользователя🧦')
async def oper(message: types.Message, state: FSMContext):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
        cadm = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cadm.add(types.InlineKeyboardButton(text="Назад"))
        await UserState.oper.set()
        await message.reply('🎭Напиши ID пользователя', reply_markup=cadm)

@dp.message_handler(state=UserState.oper)
async def probivOPER(message: types.message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('🔮Главное меню', reply_markup=kbadm)
        await state.finish()
    else:
        if message.text.isdigit():
            await state.update_data(oper=message.text)
            ikboper = InlineKeyboardMarkup()
            ikboper.add(types.InlineKeyboardButton(text="Написать от имени бота🎉", callback_data="messoper"))
            data = await state.get_data()
            cur = conn.cursor()
            cur.execute(f"SELECT attempts FROM users WHERE user_id = {data['oper']}")
            resatm = cur.fetchone()
            cur.execute(f"SELECT ref FROM users WHERE user_id = {data['oper']}")
            resref = cur.fetchone()
            cur.execute(f"SELECT name FROM users WHERE user_id = {data['oper']}")
            resname = cur.fetchone()
            await message.answer(f"*Айди -* `{data['oper']}`\n*Юзернейм -* @{resname[0]}\n*Рефка -*"
                                 f"{resref[0]}\n*Попытки -* "f"{resatm[0]}", parse_mode='markdown', reply_markup=kbadm)
            conn.commit()
        else:
            await message.answer(
                f"Вводишь не числа!", parse_mode='markdown', reply_markup=kbadm)
            await state.finish()

@dp.callback_query_handler(text="messoper")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    cadm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cadm.add(types.InlineKeyboardButton(text="Назад"))
    data = await state.get_data()
    await state.finish()
    await callback.message.answer('*Введи сообщение*', parse_mode='markdown', reply_markup=cadm)
    await state.update_data(id=data)

@dp.message_handler(state=UserState.oper, content_types=['any'])
async def probivOPER(message: types.message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('🔮Главное меню', reply_markup=kbadm)
        await state.finish()
    else:

        await message.send_copy(1)
        await message.answer('🔮Сообщение отправлено', reply_markup=kbadm)
        await state.finish()

@dp.message_handler(content_types=['text'], text='Рассылка📤')
async def spam(message: types.Message):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
      keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add(types.InlineKeyboardButton(text="Назад"))
      await UserState.spam.set()
      await message.answer('Напиши текст рассылки⌨', reply_markup=keyboard)
    else:
      await message.answer('🧨Чумба ты че еблан? Ты не админ🧨')

@dp.message_handler(state=UserState.spam, content_types=['any'])
async def start_spam(message: types.message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer('🔮Главное меню', reply_markup=kbadm)
    await state.finish()
  else:
    await state.update_data(mess=message["message_id"])
    cur = conn.cursor()
    cur.execute(f'''SELECT user_id FROM users''')
    spam_base = cur.fetchall()
    for z in range(len(spam_base)):
        try:
            await message.send_copy(spam_base[z][0])
            await state.finish()
        except:
            await state.finish()
    await bot.send_message(-1001657487556,
                           f'💊 *{message.from_user.id} | @{message.from_user.username} Сделал рассылку*',
                           parse_mode="Markdown")
    await message.answer('Рассылка завершена✔', reply_markup=kbadm)
    await state.finish()

@dp.message_handler(content_types=['text'], text='БДшка✨')
async def hfandler(message: types.Message, state: FSMContext):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
        await message.reply_document(open('db.db', 'rb'))
        cur = conn.cursor()
        cur.execute('''select * from users''')
        results = cur.fetchall()
        await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')
        for z in range(len(results)):
            await message.answer(f'@{results[z][1]} | {results[z][0]}')

@dp.message_handler(content_types=['text'], text='Обновить попытки🚨')
async def hfandler(message: types.Message, state: FSMContext):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
          keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
          keyboard.add(types.InlineKeyboardButton(text="Назад"))
          await message.answer(f'*🎢 Введи ID пользователя и попытки в формате:*\n `ID ATTEMPTS`',
                               reply_markup=keyboard, parse_mode="Markdown")
          await UserState.attempts.set()
    else:
        await message.answer('*🧨Чумба ты че еблан? Ты не админ🧨*', parse_mode="Markdown")

@dp.message_handler(state=UserState.attempts)
async def proc(message: types.Message, state: FSMContext):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
      if message.text == 'Назад':
        await message.answer('*🔮Главное меню*', reply_markup=kbadm, parse_mode="Markdown")
        await state.finish()
      else:
          data = message.text.split()
          cur = conn.cursor()
          cur.execute(f"SELECT attempts FROM users WHERE user_id = {data[0]}")
          result = cur.fetchall()
          conn.commit()
          if len(result) == 0:
            await message.answer('📂Такого пользователя нету', reply_markup=kbadm)
          else:
              data = message.text.split()
              cur = conn.cursor()
              cur.execute(f"UPDATE users SET attempts = {data[1]} WHERE user_id = {data[0]}")
              conn.commit()
              await message.answer('🔨 Пользователь успешно обновлен', reply_markup=kbadm)
              await bot.send_message(-1001657487556,
                                     f'💊 *{message.from_user.id} | @{message.from_user.username} обновил попытки*\n'
                                     f'*{data[0]},'
                                     f' {data[1]}*',
                                     parse_mode="Markdown")
              await bot.send_message(data[0], f'Новое кол-во вашиx попыток равно {data[1]}💣.')
      await state.finish()
    else:
      await message.answer('🧨Чумба ты че еблан? Ты не админ🧨')

@dp.message_handler(content_types=['text'], text='Статистика💭')
async def hfandler(message: types.Message, state: FSMContext):
    chat_admins = await bot.get_chat_administrators(-1001657487556)
    admid = list()
    for admins in chat_admins:
        userId = admins.user.id
        admid.append(userId)
    if message.from_user.id in admid:
        cur = conn.cursor()
        cur.execute('''select * from users''')
        results = cur.fetchall()
        await message.answer(f'Людей которые когда либо заходили в бота: {len(results)}')
    else:
        await message.answer('🧨Чумба ты че еблан? Ты не админ🧨')


@dp.message_handler(text=('Пригласить друга 💗'))
async def user_register(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await message.answer(f'✨Твоя реферальная ссылка:\n<code>https://t.me/FalafelRoBot?start='
                         f'{message.from_user.id}</code>',parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                     'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                               parse_mode='markdown')

@dp.message_handler(content_types=['text'], text='Написать сочинение ⚡️')
async def process_help_text(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id='-1001881792031', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.InlineKeyboardButton(text="Назад"))
            ikbmanual = InlineKeyboardMarkup()
            ikbmanual.add(types.InlineKeyboardButton('Инструкция ⚠️', url='https://telegra.ph/Pravila-napisaniya-zaprosov-02-24'))
            await bot.send_message(message.from_user.id, 'Введите ваш вопрос 🧵', reply_markup=keyboard)
            await bot.send_message(message.from_user.id, '*Не забудь про инструкцию*', reply_markup=ikbmanual,
                                   parse_mode='markdown')
            await UserState.openaii.set()
    else:
            await bot.send_message(message.from_user.id, '*Ой-ой, мы не нашли тебя в нашей группе! Подпишись, '
                                                         'чтобы дальше работать со мной!*', reply_markup=ikbusr,
                                   parse_mode='markdown')

@dp.message_handler(state=UserState.openaii)
async def get_username(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await message.answer('🔮Главное меню', reply_markup=kbusr)
        await state.finish()
    else:
        await state.update_data(check=message.text)
        await state.finish()
        cur = conn.cursor()
        cur.execute(f"SELECT attempts FROM users WHERE user_id = {message.from_user.id}")
        result = cur.fetchone()
        conn.commit()
        try:
            if result[0] > 0:
                cur.execute(f'''UPDATE users SET attempts = attempts - 1 WHERE user_id = ('{message.from_user.id}')''')
                cur.execute(f'''UPDATE users SET quest = ('{message.text}') WHERE user_id = ('{message.from_user.id}')''')
                conn.commit()
                await state.update_data(check=message.text)
                data = await state.get_data()
                messeng = GoogleTranslator(sourse='auto', target='en').translate(data['check'])
                await bot.send_message(-1001657487556, f'🎃 {message.from_user.id} | @{message.from_user.username} '
                                                       f'<b>выполнил запрос:</b>\n<code>{message.text}</code>',
                                       parse_mode="html")
                await message.reply(f'<b>⌚ Ожидайте от 5 секунд до 300 секунд</b>',
                                       parse_mode="html", reply_markup=types.ReplyKeyboardRemove())
                try:
                    completion = await openai.Completion.acreate(
                        engine=model_engine,
                        prompt=messeng,
                        max_tokens=1024,
                        temperature=1,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    messru = GoogleTranslator(sourse='auto', target='ru').translate(completion.choices[0].text)
                    await message.reply(messru, reply_markup=kbusr)
                    await bot.send_message(-1001657487556,
                                           f'♥ <b>Закончил работать по</b> {message.from_user.id} | '
                                           f'@{message.from_user.username}\n<code>{messru}</code>',
                                           parse_mode="html")
                except:
                    await message.reply('Не понимаю вас', reply_markup=kbusr)
                    await bot.send_message(-1001657487556,
                                           f'😔 <b>200 респонс на #{message.from_user.username}</b>\n<code>{messru}</code>',
                                           parse_mode="html")
            else:
                await message.reply('🎱Вы достигли лимита, купите подписку\n🎎Или приведите друга',
                                    reply_markup=kbusr)
        except Exception as e:
            await message.reply('🧨 Ой! Случился сбой, попробуй написать /start')
            await bot.send_message(-1001657487556,f'😔 <b>БДшка наебнулась на #{message.from_user.username}</b>\n<code>'
                                                  f'{traceback.format_exc()}</code>',
                                           parse_mode="html")

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)