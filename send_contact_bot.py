from aiogram import Bot, Dispatcher, types, executor
from config import token
import sqlite3, requests, logging, time

bot = Bot(token=token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

start_buttons = [
    types.KeyboardButton("Отправить номер", request_contact=True),
    types.KeyboardButton("Отправить локацию", request_location=True),
]

start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(
        f"Привет @{message.from_user.username}", reply_markup=start_keyboard
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Contact):
    print(message)
    await message.answer(f"{message.contact.phone_number}")


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def get_location(message: types.location):
    print(message)
    await message.answer(
        f"Долгота и широта:\n{message.location.latitude}, {message.location.longitude}"
    )


executor.start_polling(dp, skip_updates=True)
