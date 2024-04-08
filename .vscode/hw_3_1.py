import logging
import random
from config import token
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

bot = Bot(token=token)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def guess_number(message: types.Message):
    secret_number = random.randint(1, 3)
    user_number = int(message.text)
    if user_number == secret_number:
        await message.reply("Правильно, вы отгадали!")
        await message.reply_photo(
            "https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg"
        )
    else:
        await message.reply("Неправильно, попробуйте еще раз!")
        await message.reply_photo(
            "https://media.makeameme.org/created/sorry-you-lose.jpg"
        )


async def start(message: types.Message):
    await message.reply("Привет! Я загадал число от 1 до 3. Попробуйте угадать.")


async def echo(message: types.Message):
    await message.reply("Извините, я вас не понимаю.")


dp.register_message_handler(start, commands=["start"])
dp.register_message_handler(guess_number)
dp.register_message_handler(echo)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
