import random
import string
import sqlite3
import logging
import time
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from config import token
import logging, time, sqlite3
from config import token

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect("logis.db")
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(100),
    region VARCHAR(30),
    client_code VARCHAR(10),
    created VARCHAR(30)
);
"""
)

start_buttons = [
    types.KeyboardButton("Регистрация"),
    types.KeyboardButton("Шаблон регистрации"),
    types.KeyboardButton("О нас"),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


def generate_client_code():
    prefix = "gcarg-"
    digits = "".join(random.choices(string.digits, k=4))
    return f"{prefix}{digits}"


class UserRegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    region = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(
        "Привет, я чат-бот карго компании Geeks!", reply_markup=start_keyboard
    )


@dp.message_handler(text="Шаблон регистрации")
async def register_template(message: types.Message):
    await message.answer(
        """Для того чтобы зарегистрироваться вам нужно:
1. Введите имя
2. Введите фамилию
3. Введите номер
4. Введите регион
Вот эти данные вам нужно для регистрации"""
    )


@dp.message_handler(text="Регистрация")
async def start_register(message: types.Message):
    await message.answer("Для регистрации в нашей карго нам нужны ваши данные:")
    await message.answer("Введите своё имя:")
    await UserRegisterState.first_name.set()


@dp.message_handler(state=UserRegisterState.first_name)
async def get_last_name(message: types.Message, state=FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await UserRegisterState.last_name.set()


@dp.message_handler(state=UserRegisterState.last_name)
async def get_phone(message: types.Message, state=FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await UserRegisterState.phone.set()


@dp.message_handler(state=UserRegisterState.phone)
async def get_region(message: types.Message, state=FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите ваш регион:")
    await UserRegisterState.region.set()


@dp.message_handler(state=UserRegisterState.region)
async def get_user_data(message: types.Message, state=FSMContext):
    await state.update_data(region=message.text)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone = data.get("phone")
    region = data.get("region")
    client_code = generate_client_code()
    cursor.execute(
        "INSERT INTO users (user_id, first_name, last_name, phone, region, client_code, created) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            message.from_user.id,
            first_name,
            last_name,
            phone,
            region,
            client_code,
            time.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    connection.commit()
    await message.answer(f"Спасибо за регистрацию! Ваш код клиента: {client_code}")


executor.start_polling(dp, skip_updates=True)
