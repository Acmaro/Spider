from bs4 import BeautifulSoup
import requests
import IP
from fake_useragent import UserAgent


# 当IP库没有可用IP时返回此异常
class OutOfIPs(Exception):
    pass


# 当正在使用的IP出错时返回此异常
class IP_Failed(Exception):
    pass


# 使用随机头文件，从IP库中抽取一个IP对网页进行爬取，并返回一个含有结果的列表
def spider(url):
    headers = {'User-Agent': UserAgent().chrome}

    def load(index):  # 使用指定IP加载
        proxies = {'http': IP.Valid[index]}
        return requests.get(url, headers=headers, proxies=proxies)

    # 检测IP库是否为空
    if len(IP.Valid) == 0:
        raise OutOfIPs
    index = 0
    r = load(index)
    stat = r.status_code
    # 对连接状态进行检测
    if stat != 200:
        raise IP_Failed

    # 解析网址
    t = r.text
    bs = BeautifulSoup(t, "html.parser")
    l = bs.find("script", type="application/ld+json")

    new = eval("".join(l.string.replace('\n', '')))
    # 对IP地址有效性进行检测
    if type(new) != dict:
        raise IP_Failed
    ob1 = [new['name']]  # 电影名
    ob2 = [new['image']]  # 海报
    ob3 = [new['director'][0]['name']]  # 导演
    ob4 = []
    for i in new['actor']:
        ob4.append(i['name'])  # 演员
    ob5 = [new['description']]  # 简介
    ob6 = [new['aggregateRating']["ratingValue"]]  # 评分
    result = [ob1, ob2, ob3, ob4, ob5, ob6]
    return result
