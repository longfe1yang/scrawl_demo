import requests
import os

# 爬取《恶魔》的

User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
Cookie = 'UM_distinctid=15fdce07c149a-03bb084c0a3f8d-173f6d55-1fa400-15fdce07c17d77; Hm_lvt_645dcc265dc58142b6dbfea748247f02=1511239221; Hm_lpvt_645dcc265dc58142b6dbfea748247f02=1511239307'


# VOL 1-6
url_root = 'http://images.dmzj.com/e/恶魔拉法颂/VOL{}/{}.jpg'

headers = {
    'User-Agent': User_Agent,
    'Cookie': Cookie,
    'Referer': 'http://manhua.dmzj.com/emolafasong/5805.shtml',
}

def download_photo(url):
    chapter_dir, page = url.split('/')[5:7]
    r = requests.get(url, headers=headers)
    if not os.path.exists(chapter_dir):
        os.mkdir(chapter_dir)
    if r.status_code == 200:
        with open('./{}/{}'.format(chapter_dir, page), 'wb') as f:
            f.write(r.content)
            print('完成', chapter_dir, page)

def gen_url():
    url_lst = []
    for chapter in range(1, 7):
        chapter = '0' + str(chapter)
        for page in range(1, 120):
            if page < 10:
                page = '00' + str(page)
            elif 100 > page >= 10:
                page = '0' + str(page)
            elif page >= 100:
                page = str(page)
            url_lst.append(url_root.format(chapter, page))
    return url_lst


def main():
    urls = gen_url()
    for url in urls:
        download_photo(url)


if __name__ == '__main__':
    main()
