from aiogram import Bot, Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
import requests,time,logging,sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect('ojak_kebap.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_joined VARCHAR(255)
);
""")

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(100),
    order_food VARCHAR(255),
    phone INTEGER,
    address VARCHAR(100),
    created VARCHAR(255)
);
""")

start_buttons = [
    types.KeyboardButton('Меню'),
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Заказать еду')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}; ")
    result = cursor.fetchall()
    if result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);",
                       (message.from_user.id, message.from_user.username, message.from_user.first_name,
                        message.from_user.last_name, time.ctime()))
        cursor.connection.commit()
    await message.answer(f"{message.from_user.first_name}, Здравствуйте", reply_markup=start_keyboard)
    await message.answer("Добро пожаловать в чат-бот 'GEEKS_OJAK'")

@dp.message_handler(text='Меню')
async def menu(message:types.Message):
    await message.answer_photo("https://plovnaya1.com/thumb/2/4u536ODndldp0QgIbKuM_A/r/d/lyulya-kebab_iz_govyadiny.jpg")
    await message.answer("Люля Кебаб - 180 сом")

    await message.answer_photo("https://nambafood.kg/dish_image/163137.png")
    await message.answer("Форель на мангале целиком - 710 сом")

    await message.answer_photo("https://nambafood.kg/dish_image/163145.png")
    await message.answer("Форель на мангале кусочками - 1140 сом")

    await message.answer_photo("https://nambafood.kg/dish_image/48353.png")
    await message.answer("Шашлык из курицы - 400 сом")

    await message.answer_photo("https://nambafood.kg/dish_image/150933.png")
    await message.answer("Шашлык из баранины - 460 сом")

@dp.message_handler(text = "О нас")
async def start(message: types.Message):
    await message.answer("""  Кафе 'Ожак Кебап' на протяжении 18 лет радует своих гостей изысканными турецкими блюдами в особенности своим кебабом.
  Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.
  В 2016 году по голосованию на сайте "Horeca" были удостоены "Лучшее кафе на каждый день" и мы стараемся оправдать доверие наших гостей.
  Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е». 
  У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции.
  Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.""")

@dp.message_handler(text = "Адрес")
async def start(message: types.Message):
    await message.answer("Отправляю местоположение ....")
    await message.answer("Филиал 1: Курманжакн Датка, 209 ")
    await message.answer_location(40.52656581921117, 72.79538520388482)
    await message.answer("Отправляю местоположение ....")
    await message.answer("Филиал 2: Курманжакн Датка, 89 ")
    await message.answer_location(40.512222298487224, 72.80692908562825)
    await message.answer("Отправляю местоположение ....")
    await message.answer("Филиал 3: Аскар Шакиров, 275/1Б")
    await message.answer_location(40.532166380255426, 72.80688813272462)


class UserRegisterState(StatesGroup):
    first_name = State()
    order_food = State()
    phone = State()
    address = State()

@dp.message_handler(text = "Заказать еду")
async def start(message: types.Message):  
    await message.answer("Чтобы заказать еду,введите ваши данные:")
    await UserRegisterState.first_name.set()
    await bot.send_message(message.from_user.id, "Введите ваше имя:")

@dp.message_handler(state=UserRegisterState.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text
    await UserRegisterState.next()
    await message.answer("Теперь введите ваш заказ:")

@dp.message_handler(state=UserRegisterState.order_food)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['order_food'] = message.text
    await UserRegisterState.next()
    await message.answer("Введите ваш номер телефона:")

@dp.message_handler(state=UserRegisterState.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await UserRegisterState.next()
    await message.answer("Введите ваш  адрес:")
    
group_chat_id = -4143412669 

@dp.message_handler(state=UserRegisterState.address)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
        await bot.send_message(group_chat_id, f"Новый заказ на доставку:\n\n"
                                              f"Имя: {data['first_name']}\n"
                                              f"Заказ: {data['order_food']}\n"
                                              f"Телефон: {data['phone']}\n"
                                              f"Адрес: {data['address']}")
        cursor.execute("INSERT INTO orders (first_name, order_food, phone, address, created) VALUES (?, ?, ?, ?, ? );",
                       (data['first_name'], data['order_food'], data['phone'], data['address'], time.ctime()))
        cursor.connection.commit()
    await bot.send_message(message.from_user.id, "Ваш заказ  успешно оформлен \nМы с вами свяжемся")  
    await state.finish()

executor.start_polling(dp, skip_updates=True)