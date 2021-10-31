import requests
from bs4 import BeautifulSoup


def getLastPage():
    URL = 'https://coinmarketcap.com/ko/'
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    TARGET_SELECTOR = '#__next > div > div.main-content > div.sc-57oli2-0.comDeo.cmc-body-wrapper > div > ' \
                      'div:nth-child(' \
                      '1) > ' \
                      'div.sc-16r8icm-0.sc-4r7b5t-0.gJbsQH > div.sc-4r7b5t-3.bvcQcm > div > ul > li:nth-child(9) > a '
    data = soup.select(TARGET_SELECTOR)
    last_page = data[0].get('aria-label').split()[1]
    print(last_page)


def checkExplorerUrlByBtn(btn):
    MUSTURL = ['etherscan.io', 'bscscan.com']
    tmp = 0
    for tag in btn.find_elements_by_tag_name('a'):
        if not tag.text:
            continue
        for url in MUSTURL:
            text = tag.text.replace(' ', '')
            tmp |= text == url
    return tmp


from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get('https://coinmarketcap.com/ko/currencies/ethereum/')

content = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div/div[1]/ul')
btns = content[0].find_elements_by_tag_name('li')

# btn.click()
# driver.execute_script("console.log(document.getElementsByClass('link-button'))")
from selenium.webdriver.common.action_chains import ActionChains

btn = btns[1]
ActionChains(driver).move_to_element(btns[1]).perform()

# driver.find