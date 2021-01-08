import configparser
import os
import requests
from bs4 import BeautifulSoup
import re
# 读取config文件
curpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curpath, "config.ini")
conf = configparser.ConfigParser()
conf.read(path)
sections = conf.sections()
items = conf.items('config')

start = int(items[0][1])
end = int(items[1][1])

urlbase = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.198 Safari/537.36 '
}
totalpages = []
# 获取所有将要读取的网址
for i in range(start, end + 1):
    a = 'https://movie.douban.com/top250?start='
    b = '&filter='
    web = a + str(25 * (i - 1)) + b
    totalpages.append(web)

url = []


# 获取指定页面所包含的所有目标网址
def geturl(page):
    r = requests.get(page, headers=headers)
    t = r.text
    bs = BeautifulSoup(t, "html.parser")
    l = []
    l = bs.find_all("a")
    all_url = []
    # 读取符合格式的网址
    for i in l:
        all_url.append(i.get('href'))
    for i in all_url:
        a = re.search('^https://movie.douban.com/subject/.*', i)
        if a is not None and a.string not in url:
            url.append(a.string)

# 整合所有页面的目标网址
for i in totalpages:
    geturl(i)
