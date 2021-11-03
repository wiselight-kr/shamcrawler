from coinFunc import *
import requests
from bs4 import BeautifulSoup


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donghadongha.settings")
import django
django.setup()
from coin.models import Coin

URL = 'https://coinmarketcap.com/currencies/'

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
