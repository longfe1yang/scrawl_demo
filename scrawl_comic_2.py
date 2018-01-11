from selenium import webdriver
from bs4 import BeautifulSoup

import requests
import os

'''
日文版漫画
步骤：
用requests爬取所有卷的url,
然后用phantom打开URL，
BeautifulSoup获取图片的photo_url，
再用requests来存储图片
'''
comic_url = 'http://m.jmydm.com/comic/28766/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookie': 'UM_distinctid=1601f9c4e576e1-08f24b81fb9da8-173f6d55-1fa400-1601f9c4e58fde; ViewCtTxt=28766*168207*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C06%u5377*1%5E28766*168349*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C05%u5377*1%5E28766*145937*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C04%u5377*1%5E28766*168348*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C03%u5377*1%5E28766*134013*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C02%u5377*1%5E28766*131425*%u60AA%u9B54%u3068%u30E9%u30D6%u30BD%u30F3%u30B0%5B%u65E5%u6587%u7248%5D*%u7B2C01%u5377*3',
    'Referer': 'http://m.jmydm.com/comic/28766/131425/?p=3&s=1',
}


# 获取12卷的url
def get_vol_url():
    r = requests.get(comic_url)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.select('#subBookListVol > div > a')
    link_lst = []
    for link in links:
        link_lst.insert(0, link.get('href'))
    return link_lst

# 下载图片
def download_photo(url, page, vol):
    r = requests.get(url, headers=headers)
    if not os.path.exists(vol):
        os.mkdir(vol)
    if r.status_code == 200:
        with open('./{}/{}'.format(vol, page), 'wb') as f:
            f.write(r.content)
            print('完成{}卷/{}页'.format(vol, page))

# 通过卷URL来爬每个卷的图片
def scrawl_vol(driver, vol_url, vol):
    driver.get(vol_url)
    num_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 获取总页数
    num_page = int(num_page_soup.select('#spPageCount')[0].get_text())
    page_url = vol_url + '?p={}&s=1'
    for page in range(1, num_page + 1):
        driver.get(page_url.format(page))
        print('单页url', page_url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        img_url = soup.select('img#imgCurr')[0].get('src')
        if img_url:
            download_photo(img_url, str(page), str(vol))


def phan(driver):
    all_vol_url = get_vol_url()
    vol = 1
    for url in all_vol_url:
        scrawl_vol(driver, url, vol)
        vol += 1


def main():
    driver = webdriver.PhantomJS()
    phan(driver)
