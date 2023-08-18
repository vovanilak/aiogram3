from aiogram import Bot, Dispatcher, filters, types     # фильтры для отработки сообщений, типы для создания разных объектов
from aiogram import F       # для создания фильтров сообщений с разными типами
import logging              # для получения состояния бота

# запуск логирования
logging.basicConfig(level=logging.INFO)

# Токен нужен для привязки кода к телеграм-боту
# https://t.me/BotFather - бот для создания ботов. После /start вести /newbot.
# Задать название и ник. Получить токен
TOKEN=''

bot = Bot(token=TOKEN)      # создание бота
dp = Dispatcher()           # диспетчер предназначен для обработки апдейтов ("помощник" бота)

# Фильтр на команду /start
@dp.message(filters.Command("start"))
async def cmd_start(message):
    await message.answer("/start - команды\n/clava - кнопочки")

@dp.message(filters.Command("clava"))
async def cmd_clava(message):
    await message.answer("Нажмите на кнопку", reply_markup=keyboard) # отправка текста с клавиатурой (см. ниже)

# Фильтр на сообщения со значением 'текст'
@dp.message(F.text('тест'))         # аналогичен этому:  filter.Text('тест')
async def text_msg(message):
    # Конкретное значение
    await message.answer(f'Вы отправил {message.text}')

# Фильтр на сообщения со значением 'фото'
@dp.message(filters.Text('фото'))         # аналогичен этому:  F.text('фото')
async def text_msg(message):
    img = types.FSInputFile('picture_air.png')  # указывается имя файла, который находится в ТОЙ ЖЕ папке, что и код
    await message.answer_photo(img)

# Фильтр на сообщения со значением 'стикер'
@dp.message(filters.Text('стикер'))
async def text_msg(message):
    # Для нахождения id стикера использовать бот https://t.me/idstickerbot
    await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEKDRdk3gABZWVzZYUKFX5W8tdo5RO_1hEAAicYAAKXeeFL1gEWEt7F308wBA')

# Фильтр на сообщения со значениями "р" ИЛИ "л"
@dp.message(F.text.in_(['р', 'л']))
async def text_msg(message):
    # Конкретное значение
    await message.answer(f'Вы отправили букву {message.text}')

# Фильтр на все текстовые сообщения
# Если его расположить выше дургих текстовых обработчиков, то они не будут работать
@dp.message(F.text)                 # аналогично этому:  filter.Text
async def text_msg(message):
    # Эхо
    await message.answer(message.text)
    # Конкретное значение
    await message.answer('Вы отправили какой-то текст')

# Фильтр на все фото
@dp.message(F.photo)
async def photo_msg(message):
    # Эхо
    # Фото с индексом -1 берёт фото с наилучшим качеством
    await message.answer_photo(message.photo[-1].file_id)

# Фильтр на все стикеры
@dp.message(F.sticker)
async def sticker_msg(message):
    # Эхо
    await message.answer_sticker(message.sticker.file_id)


# КНОПКИ
# создание кнопок
btn1 = types.KeyboardButton(text='тест')
btn2 = types.KeyboardButton(text='р')
btn3 = types.KeyboardButton(text='л')
btn4 = types.KeyboardButton(text='фото')
btn5 = types.KeyboardButton(text='стикер')
# настройка порядка кнопок (сколько списков столько и рядов)
kb = [
    [btn1, btn2, btn3],
    [btn4, btn5]
]
# создание клавиатуры с кнопками
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True    # делает кнпки компактными
)



# если файл запускается, а не импортируется (если этого не сделать, то при импорте файла он будет запускаться)
if __name__ == "__main__":
    dp.run_polling(bot)     # ЗАПУСК БОТА
