from aiogram import Router, Bot, Dispatcher, filters, types, F
import pandas as pd # install openpyxl
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os
import logging

TOKEN = '6681454469:AAHIEO_XgDn-awlOSAJ3I_szYGSEmFvPgBs'
EXCEL_FILE = "data.xlsx"
CATEGOR = ['health', 'food', 'entertaiment']

dp = Dispatcher()
user_dict = {}
class AddMoney(StatesGroup):
    name = State()
    amount = State()
    categor = State()
    somedel = State()

if not os.path.exists('data.xlsx'):
    col = ['id', 'date', 'name', 'amount', 'category']
    df = pd.DataFrame(columns=col)
    df.to_excel('data.xlsx')


@dp.message(filters.Command('start'), filters.StateFilter(default_state))
async def cmd_start(message: types.Message):
    await message.answer('type /add for appending new info')


@dp.message(filters.Command('add'), filters.StateFilter(default_state))
async def cmd_add(message: types.Message, state: FSMContext):
    await message.answer('Send me a name')
    await state.set_state(AddMoney.name)


@dp.message(filters.StateFilter(AddMoney.name))
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(id=message.from_user.id)
    await state.update_data(date=str(message.date).split()[0])
    await state.update_data(name=message.text)
    await message.answer('Set an amount')
    await state.set_state(AddMoney.amount)


@dp.message(filters.StateFilter(AddMoney.amount), F.text.isdigit())
async def set_amount(message: types.Message, state: FSMContext):
    await state.update_data(amount=message.text)
    builder = InlineKeyboardBuilder()
    kb = []
    for i in range(len(CATEGOR)):
        #kb.append([types.InlineKeyboardButton(text=CATEGOR[i], callback_data=str(i))])
        builder.button(text=CATEGOR[i], callback_data=CATEGOR[i])
    builder.adjust(1, len(CATEGOR))
    await state.set_state(AddMoney.categor)
    await message.answer('Choose a category', reply_markup=builder.as_markup())


@dp.message(filters.StateFilter(AddMoney.amount))
async def error_amount(message: types.Message):
    await message.answer('Incorrect value. Please, try again')


@dp.callback_query(filters.StateFilter(AddMoney.categor), F.data.in_(CATEGOR),)
async def set_categor(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    new = await state.get_data()
    new = pd.DataFrame(new, index=[0])
    data = pd.read_excel(EXCEL_FILE)
    data.drop(columns=data.columns[0], axis=1, inplace=True)
    data = pd.concat([data, new], ignore_index=True)
    data.to_excel(EXCEL_FILE)
    await state.clear()
    await callback.message.answer('Information is loaded\nLook at your result typing /info')
    await callback.answer()

@dp.message(filters.Command('del'), filters.StateFilter(default_state))
async def choose_del_row(message: types.Message, state: FSMContext):
    data = pd.read_excel(EXCEL_FILE)
    data.drop(columns=data.columns[0], axis=1, inplace=True)
    for_mes = data[data['id'] == message.from_user.id].iloc[:, 1:].tail()
    builder_del = InlineKeyboardBuilder()
    for i in for_mes['name']:
        builder_del.button(text=str(i), callback_data=str(i))
    builder_del.adjust(1, 1, repeat=True)
    await message.answer('Что удалить?', reply_markup=builder_del.as_markup())
    await state.set_state(AddMoney.somedel)


@dp.callback_query(filters.StateFilter(AddMoney.somedel))
async def del_row(call: types.CallbackQuery, state: FSMContext):
    for_del = call.message.text
    data = pd.read_excel(EXCEL_FILE)
    data.drop(data[data['name'] == for_del].index)
    data.to_excel(EXCEL_FILE)
    await call.message.answer(for_del, "удалён")
    await state.set_state(default_state)
    await call.answer()


@dp.message(filters.Command('info'), filters.StateFilter(default_state))
async def cmd_info(message: types.Message):
    data = pd.read_excel(EXCEL_FILE)
    data.drop(columns=data.columns[0], axis=1, inplace=True)
    for_mes = data[data['id'] == message.from_user.id].iloc[: , 1:]
    await message.answer(str(for_mes))

async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

