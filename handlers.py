from aiogram import types
from loader import dp 
import random

total = ''
newgame = False
chapters = ['/rules - правила игры ',
            '/help - что делать ',
            '/newgame - новая игра ',
            '/set - установить число конфет на столе',]
lot = 0
result = 0

@dp.message_handler(commands=['start', 'старт'])
async def mes_start(message: types.Message):
    #global chapters
    print(message)
    await message.answer(f'Привет, {message.from_user.first_name}, бот умеет играть в конфеты!')
    for item in chapters:
        await message.answer(f'\t{item}')

@dp.message_handler(commands=['rules'])
async def mes_rules(message: types.Message):
    await message.answer('На столе некоторое количество конфет. ' 
                        'Вы с ботом поочередно берете со стола конфеты. '
                        'За один ход можно взять не более 28 конфет. '
                        'Кто возьмет последние конфеты со стола, тот и выиграл!')

@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer('Перед началом игры введите /set и через пробел установите число конфет на столе. ' 
                        '\nХотите сыграть, введите /newgame')
    

@dp.message_handler(commands=['newgame'])
async def mes_newgame(message: types.Message):
    global newgame
    global lot
    newgame = True
    await message.answer('Игра началась, бросаем жребий!')
    lot = random.randint(1, 2)
    if lot == 1:
        await message.answer(f'Выпало {lot}, {message.from_user.first_name}, твой первый ход, пиши сколько возьмешь конфет')
    else:
        await message.answer(f'Выпало {lot}, {message.from_user.first_name}, ты ходишь вторым')
        await bot_move(message) 
  


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global newgame
    global total
    count = message.text.split()[1]
    if not newgame:
        if count.isdigit():
            total = int(count)
            await message.answer(f'На столе теперь {total} конфет')
        else:
            await message.answer(f'{message.from_user.first_name}, напишите цифрами!')
    else:
        await message.answer(f'{message.from_user.first_name}, нельзя менять правила во время игры!')

@dp.message_handler()
async def mes_all(message: types.Message):
    global newgame
    global total
    if newgame:
        if message.text.isdigit():
            total -= int(message.text)
            if total <= 0:
                await message.answer(f'{message.from_user.first_name}, ты забрал последние конфеты и победил!')
                newgame = False
            else:
                await message.answer(f'{message.from_user.first_name} взял {message.text} конфет, '
                                    f'на столе осталось {total}')


async def bot_move(message: types.Message):
    global total
    global newgame
    bottake = 0
    if 0 < total < 29:
        bottake = total
        total -= bottake
        await message.answer(f'Бот взял {bottake} конфет. '
                             f'На столе осталось {total} и бот одержал победу')
        newgame = False
    else:
        remainder = total%29
        bottake = remainder if remainder != 0 else 28
        total -= bottake
        await message.answer(f'Бот взял {bottake} конфет. '
                             f'На столе осталось {total}')
