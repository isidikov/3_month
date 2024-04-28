from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from bs4 import BeautifulSoup
import requests

bot = Bot(token="6766057664:AAF7-fUaeWipdPGY1giFw-PiY3BZ_SguiKo")
dp = Dispatcher(bot)
basicConfig(level=INFO)

@dp.message_handler(commands="start")
async def start(message:types.Message):
    await message.answer(f"Hello  \n/Acer \n/All_products")

@dp.message_handler(commands="Acer")
async def start(message:types.Message): 
    await message.answer("Start parsing")
    url = 'https://barmak.store/category/Acer/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    

    titles = soup.find_all('div', class_ ='tp-product-tag-2')
    prices = soup.find_all('span', class_ ='tp-product-price-2 new-price')
    # print(prices)

    for title, price in zip(titles, prices):
        true_price = "".join(price.text.split())
        await message.answer(f"{title.text} - {true_price} \n")

@dp.message_handler(commands="All_products")
async def start(message:types.Message):
    await message.answer("Start parsing")
    url = 'https://barmak.store/products/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    

    titles = soup.find_all('div', class_ ='tp-product-tag-2')
    prices = soup.find_all('span', class_ ='tp-product-price-2 new-price')
    # print(prices)

    for title, price in zip(titles, prices):
        true_price = "".join(price.text.split())
        await message.answer(f"{title.text} - {true_price} \n")

@dp.message_handler(commands="news")
async def start(message:types.Message):
    await message.answer("Start parsing")
    url = 'https://new.vizitka.kg/blog'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    

    titles = soup.find_all('h4', class_ ='title ltspc--1 mb-10')
    dates = soup.find_all('li', class_ ='date me-5')
    # print(dates)

    for title, date in zip(titles, dates):
        true_date = "".join(date.text.split())
        await message.answer(f"{title.text} - {true_date} \n")

executor.start_polling(dp, skip_updates=False)
