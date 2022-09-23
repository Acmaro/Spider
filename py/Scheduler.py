import Myurl
import Spider
import IP
conclude = []
# Try to crawl, and if the IP address is abnormal, delete the original IP and use the next IP in the IP pool to
# continue the crawl.
print('Current IP address:'+str(IP.Valid[0]))
for i in Myurl.url:
    try:
        Spider.spider(i)
    except Spider.IP_Failed:
        del IP.Valid[0]
        print('Changing IP:'+str(IP.Valid[0]))
        conclude.append(Spider.spider(i))
    else:
        conclude.append(Spider.spider(i))
        print('Crawling movie:'+str(Myurl.url.index(i)+1))

with open('output.txt', 'w') as f:
    for i in conclude:
        for q in i:
            for k in q:
                f.write(k+'\n')

print('Done')
