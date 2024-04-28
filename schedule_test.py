import schedule, time, requests


def hello_world():
    print(f"Hello World {time.ctime()}")


def backend_16_1b():
    print(f"Здравствуйте, сегодня у вас урок в 19:00")


# schedule.every(5).seconds.do(hello_world)
# schedule.every(1).minutes.do(hello_world)
# schedule.every().monday.at('20:14').do(backend_16_1b)


def get_btc_price():
    response = requests.get(
        "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    )
    data = response.json()
    price = data["price"]
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Цена биткоина на {current_time}:{price}$")


schedule.every(1).seconds.do(get_btc_price)


while True:
    schedule.run_pending()
    time.sleep(1)
