from aiogram import Bot, Dispatcher, types, executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("Привет")


@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.answer("Чем могу вам помочь?")


@dp.message_handler(text="Привет")
async def hello(message: types.Message):
    await message.reply("Привет, как дела?")


@dp.message_handler(commands="test")
async def test(message: types.Message):
    await message.answer_location(40.51921368734442, 72.80303897757761)
    await message.answer_photo(
        "https://sport.pibig.info/uploads/posts/2023-04/1681402603_sport-pibig-info-p-sportivnii-botan-vkontakte-54.jpg"
    )
    await message.answer_dice()


executor.start_polling(dp)
