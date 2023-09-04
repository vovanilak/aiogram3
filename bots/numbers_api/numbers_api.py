from aiogram import Bot, Dispatcher, filters, types
from aiogram import F
import requests
import logging
import os, dotenv

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(filters.Command('start'))
async def cmd_start(message):
    await message.answer('Отправь любую цифру и я пришлю тебе интересный факт')

@dp.message(F.text.isdigit())
async def fact(message):
    response = requests.get(f'http://numbersapi.com/{message.text}')
    ff = response.text
    await message.answer(ff)

@dp.message()
async def error(message):
    await message.answer('Вы отправили что-то не то')

if __name__ == "__main__":
    dp.run_polling(bot) 
