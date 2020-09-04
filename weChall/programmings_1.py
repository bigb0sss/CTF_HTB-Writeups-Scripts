#!/usr/bin/python

import requests

r = requests.session()
url = 'https://www.wechall.net/challenge/training/programming1/index.php?'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',  
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Cookie': 'WC=12852207-55602-9BSIo4vn3s0kXB7J',
    'Upgrade-Insecure-Requests': '1'
    }

### GET Request
rget = r.get(url + 'action=request', headers=header)
html = rget.content.decode('utf-8')
print(html)

### POST Request
payload = url + 'answer=' + html
print(payload)
rpost = r.post(url + 'answer=' + html, headers=header)
print(rpost.content.decode('utf-8'))
