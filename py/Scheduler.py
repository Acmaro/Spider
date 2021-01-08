import Myurl
import Spider
import IP
conclude = []
# 尝试进行爬取，如果IP地址异常，则删除原IP并使用IP库中的下一个IP继续进行爬取
print('正在使用的IP为:'+str(IP.Valid[0]))
for i in Myurl.url:
    try:
        Spider.spider(i)
    except Spider.IP_Failed:
        del IP.Valid[0]
        print('Changing IP:'+str(IP.Valid[0]))
        conclude.append(Spider.spider(i))
    else:
        conclude.append(Spider.spider(i))
        print('正在爬取：第'+str(Myurl.url.index(i)+1)+'部电影')

with open('output.txt', 'w') as f:
    for i in conclude:
        for q in i:
            for k in q:
                f.write(k+'\n')

print('爬取完成')
