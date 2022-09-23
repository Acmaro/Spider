import time
from bs4 import BeautifulSoup
import bs4
import requests
import configparser
from fake_useragent import UserAgent
import os
# read configuration file
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


# Crawl the specified url using a random request header
def get_ip(url):
    headers = {'User-Agent': UserAgent().chrome}
    r = requests.get(url, headers=headers)
    t = r.text
    bs = BeautifulSoup(t, "html.parser")
    l = bs.find("table", class_="table table-bordered table-striped")
    # Get all information about IP addresses in web pages
    info = []
    for child in l.descendants:
        if type(child) == bs4.element.NavigableString:
            if child.string != " ":
                info.append(child.string)
    a = []
    for i in info:
        if i != '\n':
            a.append(i)
    # Extract IP address from all information
    for i in range(0, len(a[7:]), 7):
        ip.append(a[7:][i])


# Combine the IP addresses of all pages into one list, wait for 1 second between every two crawls
for i in totalpage:
    get_ip(i)
    time.sleep(1)
# Specify the page and request header to be used for testing
test_url = 'https://movie.douban.com/top250'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.198 Safari/537.36 '
}
Valid = []

# Test if the IP address is valid
print('Acquiring IP...')
for i in ip:
    proxies = {"http": "http://" + str(i)}
    r = requests.get(test_url, headers=headers, proxies=proxies)
    if r.status_code == 200:
        Valid.append(i)
if Valid != []:
    print('IP acquisition success')
