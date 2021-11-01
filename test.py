import requests
from bs4 import BeautifulSoup


def getLastPage():
    URL = 'https://coinmarketcap.com/'
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    TARGET_SELECTOR = '#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > ' \
                      'div:nth-child(' \
                      '1) > ' \
                      'div.sc-16r8icm-0.sc-4r7b5t-0.gJbsQH > div.sc-4r7b5t-3.bvcQcm > div > ul > li:nth-child(9) > a '
    data = soup.select(TARGET_SELECTOR)
    last_page = data[0].get('aria-label').split()[1]
    return int(last_page)




import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains



def getData(driver, url):
    driver.get(url)
    data = {}
    MUSTURL = [('etherscan', 'https://etherscan.io/token/', 'https://etherscan.io/address/'), ('bscscan', 'https://bscscan.com/token/', 'https://bscscan.com/address/')]
    btns = getHoverDataBtn(driver)
    for i, btn in enumerate(btns):
        try:
            if i==0:
                if btn.text=='Website':
                    data['site'] = getHrefUsingHoverByWebElementChild(driver, btn)[0]
                else:
                    data['site'] = btn.text
                doBtnHover(driver, btn)
                time.sleep(0.2)

            elif btn.text=='Explorers':
                childs = getHrefUsingHoverByWebElementChild(driver, btn)
                for child in childs:
                    if not len(child): continue
                    for (mUrl, p, q) in MUSTURL:
                        if mUrl in child:
                            tmpStr = child.replace(p, '')
                            tmpStr = tmpStr.replace(q, '')
                            if not len(tmpStr): continue
                            data[mUrl] = tmpStr
        except: continue
    try:
        data['symbol'] = getSymbol(driver)
    except:
        data['symbol'] = None
    try:
        data['marketCap'] = int(getFDMC(driver))
    except:
        data['marketCap'] = None
    return data

def doBtnHover(driver, btn):
    ActionChains(driver).move_to_element(btn).perform()

def getHrefUsingHoverByWebElementChild(driver, target):
    doBtnHover(driver, target)
    return [tar.get_attribute('href') for tar in target.find_elements_by_tag_name('a')]

def getHoverDataBtn(driver):
    ## TODO set detail
    content = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div[1]/ul')
    if not content:
        content = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[3]/div/div[5]/div/div[1]/ul')
    btns = content[0].find_elements_by_tag_name('li')
    return btns
    # driver.find

def getSymbol(driver):
    return driver.find_element_by_class_name('nameSymbol').text

def getFDMC(driver):
    try:
        return driver.find_element_by_class_name('statsValue').text[1:].replace(',','')
    except:
        return None

driver = webdriver.Chrome('./chromedriver')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "donghadongha.settings")
import django
django.setup()
from coin.models import Coin

# lastPage = getLastPage()
# PAGEURL = 'https://coinmarketcap.com/?page='
# COINS = set()
# for i in range(1, lastPage + 1):
#     time.sleep(1)
#     driver.get(PAGEURL + str(i))
#     height = driver.execute_script("return document.body.scrollHeight")
#     toHeight = 0
#     steps = 30
#     heightByStep = height / steps
#     for i in range(steps):
#         time.sleep(1)
#         driver.execute_script("window.scrollTo(0, %d);" % toHeight)
#         toHeight += heightByStep
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     tbody = soup.select(
#         '#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > div:nth-child(1) > div.h7vnx2-1.bFzXgL > table > tbody')
#     coins = tbody[0].select('tr > td > div > a')
#
#     for coin in coins:
#         COINS.add(coin['href'].split('/')[2])
#     print(len(COINS))
#
# print(len(COINS))
# for coin in COINS:
#     Coin.objects.create(name=coin)
# print(len(COINS))


URL = 'https://coinmarketcap.com/currencies/'

for coin in Coin.objects.all():
    data = getData(driver, URL + coin.name)
    print(data)
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
