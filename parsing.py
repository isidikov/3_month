from bs4 import BeautifulSoup
import requests

def parsing_barmak():
    url = 'https://barmak.store/category/Acer/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    

    titles = soup.find_all('div', class_ ='tp-product-tag-2')
    prices = soup.find_all('span', class_ ='tp-product-price-2 new-price')
    # print(prices)
    with open('laptops.txt', 'w', encoding='utf-8') as file:

        for title, price in zip(titles, prices):
            true_price = "".join(price.text.split())
            file.write(f"{title.text} - {true_price} \n")

parsing_barmak()
