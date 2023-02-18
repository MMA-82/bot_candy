from aiogram import types
from loader import dp 
import random

total = ''
newgame = False
set = False
chapters = ['/rules - правила игры ',
            '/help - что делать ',
            '/newgame - новая игра ']
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
    await message.answer('Введите /newgame чтобы начать игру. ' 
                        '\nДалее с помощью команды /set через пробел установите число конфет на столе')
    
@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global newgame
    global total
    global set
    global result
    set = True
    count = message.text.split()[1]
    if newgame:
        if result > 0: 
            await message.answer(f'{message.from_user.first_name}, нельзя менять правила во время игры!')
        else:
            if count.isdigit():
                total = int(count)
                await message.answer(f'На столе теперь {total} конфет. Введите еще раз /newgame')
                                    
            else:
                await message.answer(f'{message.from_user.first_name}, напишите цифрами!')
            if result > 0: 
                await message.answer(f'{message.from_user.first_name}, нельзя менять правила во время игры!')
    
        
            
    

@dp.message_handler(commands=['newgame'])
async def mes_newgame(message: types.Message):
    global newgame
    global lot
    global set
    newgame = True
    if set:
        await message.answer('Игра началась, бросаем жребий!')
        lot = random.randint(1, 2)
        if lot == 1:
            await message.answer(f'Выпало {lot}, {message.from_user.first_name}, твой первый ход, пиши сколько возьмешь конфет')
        else:
            await message.answer(f'Выпало {lot}, {message.from_user.first_name}, ты ходишь вторым')
            await bot_move(message)
    else: 
        await message.answer('Установите число конфет на столе, используя команду /set пробел и число')
    
     
@dp.message_handler()
async def mes_all(message: types.Message):
    global newgame
    global total
    global set
    global result
    if newgame:
        if message.text.isdigit() and 0 < int(message.text) < 29:
            total -= int(message.text)
            result += total
            if total <= 0:
                await message.answer(f'{message.from_user.first_name}, поздравляю, ты забрал последние конфеты и победил!')
                newgame = False
                set = False
                result = 0
                await message.answer('Введите /newgame чтобы сыграть еще')
            else:
                await message.answer(f'{message.from_user.first_name} взял {message.text} конфет, '
                                    f'на столе осталось {total}')
                await bot_move(message)
                
        else: 
            await message.answer(f'{message.from_user.first_name}, за раз можно взять максимум 28 конфет!')


async def bot_move(message: types.Message):
    global total
    global newgame
    global set
    global result
    bottake = 0
    if 0 < total < 29:
        bottake = total
        total -= bottake
        result += total
        await message.answer(f'Бот взял последние {bottake} конфет и победил!!!')
        newgame = False
        set = False
        result = 0
        await message.answer('Введите /newgame чтобы сыграть еще')
    else:
        remainder = total%29
        bottake = remainder if remainder != 0 else 28
        total -= bottake
        result += total
        await message.answer(f'Бот взял {bottake} конфет. '
                             f'На столе осталось {total}')
