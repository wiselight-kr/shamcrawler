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
    print('나들어왔어!!')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    print('driver set')
    from coin.models import Coin

    lastPage = getLastPage()
    PAGEURL = 'https://coinmarketcap.com/?page='
    COINS = set()
    for i in range(1, lastPage + 1):
        time.sleep(1)
        driver.get(PAGEURL + str(i))
        height = driver.execute_script("return document.body.scrollHeight")
        toHeight = 0
        steps = 30
        heightByStep = height / steps
        for i in range(steps):
            time.sleep(1)
            driver.execute_script("window.scrollTo(0, %d);" % toHeight)
            toHeight += heightByStep
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tbody = soup.select(
            '#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div:nth-child(1) > div.h7vnx2-1.bFzXgL > table > tbody')
        coins = tbody[0].select('tr > td > div > a')

        for coin in coins:
            tmp = coin['href'].split('/')[2]
            try:
                Coin.objects.get(name=tmp)
                print('in', tmp)
            except:
                print('not in', tmp)
                COINS.add(tmp)
            # COINS.add(coin['href'].split('/')[2])
        print(len(COINS))

    print(len(COINS))
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
