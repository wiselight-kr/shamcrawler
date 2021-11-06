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
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./driver/chromedriver', chrome_options=chrome_options)

    for coin in Coin.objects.all():
        if not coin.marketCap: continue
        time.sleep(1)
        driver.get(URL+coin.name)
        try:
            data = int(getFDMC(driver))
            if data:
                coin.marketCap = data
                coin.save()
        except:
            print(coin.name, 'is none')

@shared_task
def updateCoin():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('./driver/chromedriver', chrome_options=chrome_options)
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donghadongha.settings")
    import django
    django.setup()
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