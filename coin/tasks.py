from coin.models import Coin
from celery import shared_task


# @shared_task
# def add(x, y):
#     print('add hello!', x, y, x+y)
#     return x+y
# @shared_task
# def test(x, y):
#     print(x, y)
#     return x+y

from coinFunc import *


@shared_task
def updateMarkCap():
    URL = 'https://coinmarketcap.com/currencies/'
    print(URL)
    driver = webdriver.Chrome('./chromedriver')

    for coin in Coin.objects.all():
        if not coin.marketCap: continue
        time.sleep(1)
        driver.get(URL+coin.name)
        data = getFDMC(driver)
        print(coin, data)
        if data:
            coin.marketCap = data
            coin.save()
