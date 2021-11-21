import requests
from bs4 import BeautifulSoup
import json
import time
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donghadongha.settings")
import django
django.setup()
from coin.models import Coin

URL = 'https://coinmarketcap.com/currencies/'

for coin in Coin.objects.all():
    if coin.symbol:
        continue
    print(coin)
    try:
        coin_page = requests.get(URL + coin.name)
        soup = BeautifulSoup(coin_page.content, 'html.parser')
        data = soup.find('script', id="__NEXT_DATA__", type="application/json")
        coin_data = json.loads(data.contents[0])

        coin.symbol = coin_data['props']['initialProps']['pageProps']['info']['symbol']
        coin.marketCap = coin_data['props']['initialProps']['pageProps']['info']['statistics']['marketCap']
        platforms = coin_data['props']['initialProps']['pageProps']['info']['platforms']
        eth = list(filter(lambda x: x['contractPlatform'] == 'Ethereum', platforms))
        if len(eth) == 1:
            coin.ethTokenAddress = eth[0]['contractAddress']
        bsc = list(filter(lambda x: x['contractPlatform'] == 'Binance Smart Chain (BEP20)', platforms))
        if len(bsc) == 1:
            coin.bscTokenAddress = bsc[0]['contractAddress']
        coin.website = coin_data['props']['initialProps']['pageProps']['info']['urls']['website'][0]
        coin.save()

        time.sleep(5)
    except:
        print('delete coin', coin)
        # coin.delete()
