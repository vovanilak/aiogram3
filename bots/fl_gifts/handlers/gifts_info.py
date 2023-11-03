from aiogram import Router
from aiogram types import Message

FILE_GIFTS = ""



router = Router()

@router.message(message)
async def balance(message: Message):
    loop = asyncio.get_event_loop()
    df = await loop.run_in_executor(None, pd.read_excel, FILE_GIFTS)
    result = df[[df['id'] == message.from_user.id]]['sum']
    await message.answer(result)


