from aiogram import Bot, Dispatcher, filters, Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import default_state
import pandas as pd
import asyncio
import logging
import os
from dotenv import load_dotenv
from utils.mail import send_gmail

load_dotenv()
TOKEN = os.getenv('TOKEN')
dp = Dispatcher()
router = Router()
USER_FILE = './data/users_info.xlsx'
GIFT_FILE = './data/gifts_info.csv'


class Registration(StatesGroup):
    login = State()
    name = State()
    inn = State()
    location = State()
    phone = State()
    mail = State()


info_konkurs = 'test'

@router.message(StateFilter(default_state), Command('editinfo'))
async def edit_info(message: Message):
    if message.from_user.username == os.getenv('ADMIN_NIK'):
        global info_konkurs
        insert = ' '.join(message.text.split()[1:])
        info_konkurs = insert
        await message.answer('Информация изменена')
    else:
        await message.answer('Я тебя не понимаю')


@router.message(StateFilter(default_state), Command('info'))
async def cmd_info(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Баланс'))
    builder.row(types.KeyboardButton(text='Подробности акции'))
    await message.answer('О чём хотеите узнать?', reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text('Подробности акции'), StateFilter(default_state))
async def get_info(message: Message):
     await message.answer(info_konkurs)


@router.message(F.text('Баланс'), StateFilter(default_state))
async def balance(message: Message):
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, pd.read_excel, GIFT_FILE)
    data.drop(columns=data.columns[0], axis=1, inplace=True)
    for_mes = data[data['Логин'] == message.from_user.username].iloc[: , 2:4]
    await message.answer(str(for_mes))


@router.message(Command('registration'), StateFilter(default_state))
async def cmd_registration(message: Message, state: FSMContext):
    await message.answer('Введите своё имя')
    await state.set_state(Registration.name)


@router.message(StateFilter(Registration.name))
async def set_login(message: Message, state: FSMContext):
    await state.update_data(login=message.from_user.username)
    await state.update_data(name=message.text)
    await message.answer('Введите свой ИНН')
    await state.set_state(Registration.inn)


@router.message(StateFilter(Registration.inn))
async def set_inn(message: Message, state: FSMContext):
    await state.update_data(inn=message.text)
    await message.answer('Введите свой регион')
    await state.set_state(Registration.location)


@router.message(StateFilter(Registration.location))
async def set_login(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer('Введите свой номер телефона')
    await state.set_state(Registration.phone)


@router.message(StateFilter(Registration.phone))
async def set_login(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('Введите свою почту')
    await state.set_state(Registration.mail)


@router.message(StateFilter(Registration.mail))
async def set_login(message: Message, state: FSMContext):
    data = pd.read_excel(USER_FILE)
    keys = data.columns
    vals = new.values()
    new = {k: v for k, v in zip(keys, vals)}
    send_gmail(fro=os.getenv('MAIL_ADDRESS'), to=os.getenv('MAIL_ADDRESS'), mes=str(new), pas=os.getenv('MAIL_PASSWORD'))
    new = pd.DataFrame(new, index=[0])
    data = pd.concat([data, new], ignore_index=True)
    data.to_excel(USER_FILE)
    await message.answer('Спасибо за регистрацию. Данные записаны')


@router.message(StateFilter(Registration.mail))
async def set_login(message: Message, state: FSMContext):
    await state.update_data(mail=message.text)
    loop = asyncio.get_event_loop()
    new = await state.get_data()
    data = await loop.run_in_executor(None, pd.read_excel, USER_FILE)
    keys = data.columns
    vals = new.values()
    new = {k: v for k, v in zip(keys, vals)}
    new = pd.DataFrame(new, index=[0])
    data = pd.concat([data, new], ignore_index=True)
    data.drop(columns=data.columns[0], axis=1, inplace=True)
    await loop.run_in_executor(None, data.to_excel, USER_FILE)
    await state.clear()
    await message.answer('Спасибо за регистрацию. Данные записаны')




async def main():
    bot = Bot(TOKEN)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())