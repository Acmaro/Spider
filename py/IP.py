import time
from bs4 import BeautifulSoup
import bs4
import requests
import configparser
from fake_useragent import UserAgent
import os
# 读取config文件
curpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curpath, "config.ini")
conf = configparser.ConfigParser()
conf.read(path)
sections = conf.sections()
items = conf.items('IP')
# 获取所有将要进行爬取的网址
start = int(items[0][1])
end = int(items[1][1])
url = 'https://www.kuaidaili.com/free/inha/1/'
totalpage = []
for i in range(start, end + 1):
    totalpage.append(url.replace('1', str(i)))

ip = []


# 使用随机的请求头对指定的url进行爬取
def get_ip(url):
    headers = {'User-Agent': UserAgent().chrome}
    r = requests.get(url, headers=headers)
    t = r.text
    bs = BeautifulSoup(t, "html.parser")
    l = bs.find("table", class_="table table-bordered table-striped")
    # 获取网页中关于IP地址的所有信息
    info = []
    for child in l.descendants:
        if type(child) == bs4.element.NavigableString:
            if child.string != " ":
                info.append(child.string)
    a = []
    for i in info:
        if i != '\n':
            a.append(i)
    # 从所有信息中获提取IP地址
    for i in range(0, len(a[7:]), 7):
        ip.append(a[7:][i])


# 将所有页面的IP地址合并到一个列表里，每两次爬取之间间隔1秒
for i in totalpage:
    get_ip(i)
    time.sleep(1)
#指定用于测试的网页和请求头
test_url = 'https://movie.douban.com/top250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.198 Safari/537.36 '
}
Valid = []

# 测试IP地址是否有效
print('正在获取IP...')
for i in ip:
    proxies = {"http": "http://" + str(i)}
    r = requests.get(test_url, headers=headers, proxies=proxies)
    if r.status_code == 200:
        Valid.append(i)
if Valid != []:
    print('IP获取成功')
