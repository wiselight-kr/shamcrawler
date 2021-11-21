from coin.models import Coin
from celery import shared_task
import json
import time
import requests
from bs4 import BeautifulSoup

@shared_task
def updateMarkCap():
    URL_PREFIX = 'https://coinmarketcap.com/currencies/'
    for coin in Coin.objects.all():
        print(coin.name)
        try:
            coin_page = requests.get(URL_PREFIX + coin.name)
            soup = BeautifulSoup(coin_page.content, 'html.parser')
            data = soup.find('script', id="__NEXT_DATA__", type="application/json")
            coin_data = json.loads(data.contents[0])

            coin.marketCap = coin_data['props']['initialProps']['pageProps']['info']['statistics']['marketCap']
            coin.save()
        except:
            print(coin.name, 'is none')
            coin.marketCap = 0
            coin.save()

        time.sleep(5)

@shared_task
def updateCoin():
    start = 1
    limit = 1000
    API_URL = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start={}&limit={}&sortBy=market_cap&sortType=desc&convert=USD&cryptoType=all&tagType=all&audited=false&aux=null'

    COINS = set()

    first_page = requests.get(API_URL.format(start, limit))
    first_page_json = json.loads(first_page.text)
    total_count = first_page_json['data']['totalCount']

    for i in range(1, int(int(total_count) / limit) + 2):
        page = requests.get(API_URL.format(start, limit))
        page_json = json.loads(page.text)

        COINS.update(set(map(lambda x: x['slug'], page_json['data']['cryptoCurrencyList'])))

        start += limit
        time.sleep(1)

    for coin in COINS:
        Coin.objects.create(name=coin)
    print(len(COINS))

@shared_task
def allUpdate():
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
