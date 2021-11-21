from coin.models import Coin
from celery import shared_task
import json
import time

from coinFunc import *

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
    from coin.models import Coin

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
    print(URL)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    URL = 'https://coinmarketcap.com/currencies/'

    for coin in Coin.objects.all():
        if coin.symbol:
            continue
        print(coin)
        try:
            data = getData(driver, URL + coin.name)
            if data.get('symbol'):
                coin.symbol = data['symbol']
            if data.get('marketCap'):
                coin.marketCap = data['marketCap']
            if data.get('etherscan'):
                coin.ethTokenAddress = data['etherscan']
            if data.get('bscscan'):
                coin.bscTokenAddress = data['bscscan']
            if data.get('site'):
                coin.website = data['site']
            coin.save()
        except:
            print('delete coin', coin)
            #coin.delete()
