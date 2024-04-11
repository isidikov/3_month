from aiogram import Bot, Dispatcher, types, executor
from config import token
import logging

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

start_buttons = [
    types.KeyboardButton("О нас"),
    types.KeyboardButton("Курсы"),
    types.KeyboardButton("Контакты"),
    types.KeyboardButton("Адрес"),
    types.KeyboardButton("Зарегистрировать"),
]
# , one_time_keyboard=True
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(
        f"Здравствуйте {message.from_user.first_name}!", reply_markup=start_keyboard
    )
    # await message.answer(f'{message}')


@dp.message_handler(text="О нас")
async def start(message: types.Message):
    await message.reply(
        "Geeks - это айти курсы в Бишкеке, Ташкенте и в Оше! Основано в 2019"
    )


@dp.message_handler(text="Контакты")
async def start(message: types.Message):
    await message.answer_contact("996777123456", "Али", "Алиев")
    await message.answer_contact("996559000711", "Исломжон", "Сидиков")
    await message.answer_contact("996700326598", "Geeks", "Админ")


@dp.message_handler(text="Адрес")
async def start(message: types.Message):
    await message.answer("Отправляю местоположение ....")
    await message.answer_location(440.51956308902688, 72.80300035767178)


@dp.message_handler(text="Зарегистрировать")
async def start(message: types.Message):
    await message.answer(
        """Для регистрации напишите:
                         1. Полное ФИО
                         2. Номер телефона для связи
                         3. Название курса
Мы с вами свяжемся"""
    )


courses_buttons = [
    types.KeyboardButton("Backend"),
    types.KeyboardButton("Frontend"),
    types.KeyboardButton("Android"),
    types.KeyboardButton("IOS"),
    types.KeyboardButton("UX/UI"),
    types.KeyboardButton("Назад"),
]

courses_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*courses_buttons)


@dp.message_handler(text="Курсы")
async def start(message: types.Message):
    await message.answer("Вот все наши курсы: ", reply_markup=courses_keyboard)


@dp.message_handler(text="Backend")
async def start(message: types.Message):
    await message.reply(
        """Backend — это внутренняя часть продукта, которая находится на сервере и скрыта от пользователей. 
Для ее разработки могут использоваться самые разные языки, например, Python, PHP, Go, JavaScript, Java, С#.
Так как самым лёгким и понятным языком является Python, мы обучаем студентов именно на этом языке"""
    )
    await message.answer_photo("https://ddi-dev.com/uploads/backend-is.png")
    await message.answer("Цена: 10 000 сом/месяц")


@dp.message_handler(text="Frontend")
async def start(message: types.Message):
    await message.reply(
        "Frontend — это публичная часть web-приложений (вебсайтов), с которой пользователь может взаимодействовать и контактировать напрямую. Во Frontend входит отображение функциональных задач, пользовательского интерфейса, выполняемые на стороне клиента, а также обработка пользовательских запросов. По сути, фронтенд — это всё то, что видит пользователь при открытии web-страницы."
    )
    await message.answer_photo(
        "https://cdn2.hexlet.io/assets/blog/program_promo/frontend-c41f8485a965e95822a9dcb3658380e6699ae42d34ed7f88226e31ae5c903e2b.svg"
    )
    await message.answer("Цена: 10 000 сом/месяц")


@dp.message_handler(text="Android")
async def start(message: types.Message):
    await message.reply(
        "Android – это наиболее популярная и распространенная мобильная платформа в мире. Плюс в отличие от iOS, она используется на самых разнообразных устройствах."
    )
    await message.answer_photo(
        "https://ocdn.eu/images/pulscms/OWU7MDA_/45cf12550521a6155abf6a64cdeae3b1.jpg"
    )
    await message.answer("Цена: 12 000 сом/месяц")


@dp.message_handler(text="IOS")
async def start(message: types.Message):
    await message.reply(
        "iOS-разработчик, или iOS developer, — это программист, который пишет сервисы и программы для айфонов. Из-за особенностей устройств Apple и их операционной системы для них нужно писать специальный код. Основной язык, на котором пишут код iOS-разработчики, — Swift."
    )
    await message.answer_photo(
        "https://www.kv.by/sites/default/files/pictures/userpictures/2019/03/03/2359/1_2dremomgtqmap6xrjtr-fq.jpeg"
    )
    await message.answer("Цена: 11 000 сом/месяц")


@dp.message_handler(text="UX/UI")
async def start(message: types.Message):
    await message.reply(
        "UI ― это user interface, пользовательский интерфейс, проще говоря ― оформление сайта: сочетания цветов, шрифты, иконки и кнопки. UX ― это функционал интерфейса, UI ― его внешний вид. В современном дизайне UX и UI практически всегда идут рядом, потому что они очень тесно связаны."
    )
    await message.answer_photo(
        "https://248006.selcdn.ru/main/iblock/b86/b86d11c68063164d729ed7f3ebe3d115/f5803bce51756d1650cac545d509324c.png"
    )
    await message.answer("Цена:  9000 сом/месяц")


@dp.message_handler(text="Назад")
async def start(message: types.Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=start_keyboard)


@dp.message_handler()
async def not_found(message: types.Message):
    await message.reply("Я вас не понял введите кнопку /start")


executor.start_polling(dp)
