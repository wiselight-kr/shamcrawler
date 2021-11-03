import requests
from bs4 import BeautifulSoup
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
    if not content:
        content = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[2]/div/div[4]/div/div[1]/ul')
    if not content:
        content = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div/div[1]/div[3]/div/div[4]/div/div[1]/ul')
    btns = content[0].find_elements_by_tag_name('li')
    return btns

def getSymbol(driver):
    return driver.find_element_by_class_name('nameSymbol').text

def getFDMC(driver):
    try:
        return driver.find_element_by_class_name('statsValue').text[1:].replace(',','')
    except:
        return None
