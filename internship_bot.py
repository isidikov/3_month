from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token
import logging, time, sqlite3  # Не забудьте sqlite3

bot = Bot(token=token)
memory = MemoryStorage()
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect("intership.dp")
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
               id INTEGER,
               username VARCHAR(255),
               first_name VARCHAR(255),
               Last_name VARCHAR (255),
               created VARCHAR(255)
);
"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS intership(
               first_name VARCHAR(100),
               last_name VARCHAR(100),
               created VARCHAR(100)
);
"""
)
start_inline_buttons = [
    types.InlineKeyboardButton("Стажировка", callback_data="intership_callback"),
    types.InlineKeyboardButton("Наш сайт", url="https://geeks.kg/"),
    types.InlineKeyboardButton("Наш инстаграм", url="https://instagram.com/geeks_osh/"),
]
start_keyboard = types.InlineKeyboardMarkup().add(*start_inline_buttons)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")
    result = cursor.fetchall()
    print(result)
    if result == []:
        cursor.execute(
            "INSERT INTO users VALUES(?,?,?,?,?);",
            (
                message.from_user.id,
                message.from_user.username,
                message.from_user.last_name,
                message.from_user.first_name,
                time.ctime(),
            ),
        )

    cursor.connection.commit()
    await message.answer(
        f"{message.from_user.full_name} привет!", reply_markup=start_keyboard
    )


@dp.callback_query_handler(lambda call: call.data == "intership_callback")
async def intership_callback(callback: types.CallbackQuery):
    await callback.answer("Кнопка работает")


executor.start_polling(dp, skip_updates=True)
