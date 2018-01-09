import requests
from bs4 import BeautifulSoup
import time

url = 'http://vote.gog.cn/Ticket/Data'

src = 'http://dvote.gog.cn/f1eabb98261d451fb2993d2c46e0e1f3.html'
scheme = 'http'
ip = '121.31.148.127'
port = '8123'
info = '{0}://{1}:{2}'.format(scheme,ip,port)
proxies = {'http':info}
response = requests.get(url=src, proxies=proxies)
response.encoding = response.apparent_encoding

soup = BeautifulSoup(response.text, 'lxml')

sxwdiv = soup.find(attrs={'class':'item_wrap item_wrap_305 page_1'})
print(sxwdiv)

bb = sxwdiv.select('dd > a')

ele = bb[-1]

tid = ele.get('data-tid')
print(tid)

tkey = ele.get('data-tkey')
print(tkey)

data = {'tid':tid, 'tkey':tkey}
for i in range(7):
    r = requests.post(url, data=data, proxies=proxies)
    print(r.text)
    time.sleep(2)

