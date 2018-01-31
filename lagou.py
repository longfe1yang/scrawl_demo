from bs4 import BeautifulSoup
import requests
import json
import re

User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
headers = {
    'User-Agent': User_Agent,
}


def request_info(url):
    f = requests.get(url, headers=headers)
    soup = BeautifulSoup(f.text, 'lxml')
    companies = soup.select(
        '#s_position_list > ul > li > div.list_item_top > div.company > div.company_name > a')
    # print('公司', companies, '数量', len(companies))
    salaries = soup.select(
        '#s_position_list > ul > li > div.list_item_top > div.position > div.p_bot > div > span')
    # print('工资', salaries, '数量', len(salaries))
    experiences = soup.select(
        '#s_position_list > ul > li > div.list_item_top > div.position > div.p_bot')
    # print('经验', experiences, '数量', len(experiences))
    data_list = []
    for company, salary, experience in zip(companies, salaries, experiences):
        data = {
            'company': company.get_text(),
            'salary': salary.get_text(),
            'experience': str(experience.contents[1]).split('经验')[1].split('年')[0],
        }
        data_list.append(data)
    return data_list


def get_pages_num(soup):
    pages = soup.select('#s_position_list > div.item_con_pager > div > a:nth-of-type(5)')[0].get_text()
    pages = pages if pages.isdigit() else len(soup.select('#s_position_list > div.item_con_pager > div > a')) - 2
    # print('debug', pages)
    return pages


def save(data):
    with open('java.txt', 'a', encoding='utf-8') as f:
        f.write(str(data))
        f.write('\r\n')


def format_salary(s):
    s1, s2 = s.split('-')
    return s1[:len(s1) - 1], s2[:len(s2) - 1]


def caculate(lst):
      # todo, 整理冗余的，可以携程函数
    one_to_three_n = one_to_three_l = one_to_three_h = 0
    three_to_five_n = three_to_five_l = three_to_five_h = 0
    for i in lst:
        if i['experience'] == '1-3':
            # print('1-3经验', i['experience'])
            one_to_three_n += 1
            one_to_three_l += int(format_salary(i['salary'])[0])
            one_to_three_h += int(format_salary(i['salary'])[1])
        elif i['experience'] == '3-5':
            # print('3-5经验', i['experience'])
            three_to_five_n += 1
            three_to_five_l += int(format_salary(i['salary'])[0])
            three_to_five_h += int(format_salary(i['salary'])[1])
    print('1-3', one_to_three_n, '3-5', three_to_five_n)
    # todo, 区别除数为零的情况
    print('1-3年平均:',
          round(one_to_three_l / one_to_three_n, 2), '到',
          round(one_to_three_h / one_to_three_n, 2))
    print('3-5年平均:',
          round(three_to_five_l / three_to_five_n, 2), '到',
          round(three_to_five_h / three_to_five_n, 2))


def request_main(root_url):
      # todo, url变量更改为更容易操作的，不用每次修改这个URL
    url = 'https://www.lagou.com/zhaopin/Node.js/{}/?filterOption=2'
    f = requests.get(root_url, headers=headers)
    soup = BeautifulSoup(f.text, 'lxml')
    page_num = int(get_pages_num(soup))
    total = []
    for i in range(1, page_num + 1):
        total.extend(request_info(url.format(str(i))))
    # save(total)
    caculate(total)


def main():
    # todo
    request_main('https://www.lagou.com/zhaopin/Node.js/1/?filterOption=2')


if __name__ == '__main__':
    main()
