from bs4 import BeautifulSoup
import requests
import IP
from fake_useragent import UserAgent


# This exception is returned when there is no IP available in the IP pool
class OutOfIPs(Exception):
    pass


# This exception is returned when there is an error in the IP being used
class IP_Failed(Exception):
    pass


# Crawl a web page using a random header that draws an IP from the IP library and returns a list with the results
def spider(url):
    headers = {'User-Agent': UserAgent().chrome}

    def load(index):  # Load using the specified IP
        proxies = {'http': IP.Valid[index]}
        return requests.get(url, headers=headers, proxies=proxies)

    # Test if IP pool is empty
    if len(IP.Valid) == 0:
        raise OutOfIPs
    index = 0
    r = load(index)
    stat = r.status_code
    # Test connection status
    if stat != 200:
        raise IP_Failed

    # parse URL
    t = r.text
    bs = BeautifulSoup(t, "html.parser")
    l = bs.find("script", type="application/ld+json")

    new = eval("".join(l.string.replace('\n', '')))
    # Checking the validity of IP addresses
    if type(new) != dict:
        raise IP_Failed
    ob1 = [new['name']]  # movie name
    ob2 = [new['image']]  # post
    ob3 = [new['director'][0]['name']]  # director
    ob4 = []
    for i in new['actor']:
        ob4.append(i['name'])  # actor
    ob5 = [new['description']]  # introduction
    ob6 = [new['aggregateRating']["ratingValue"]]  # rating
    result = [ob1, ob2, ob3, ob4, ob5, ob6]
    return result
