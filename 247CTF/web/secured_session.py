import requests
import os
import re

def connect(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        }

    proxies = {
        'http' : '127.0.0.1:8080',
        }
    
    s = requests.Session()
    r = s.get(url+"cookie", proxies=proxies, headers=headers)
    tmp = s.cookies.get_dict()
    cookie = tmp['session']
    return cookie

if __name__ == '__main__':
    url = "https://1694b82d96a81cb7.247ctf.com/flag?secret_key="

    cookie = connect(url)
    cmd = f"python3 flask_session_cookie_manager3.py decode -c '{cookie}'"
    os.system(cmd)

    # echo -n "MjQ3Q1RGe2RhODA3OTVmOGE1Y2FiMmUwMzdkNzM4NTgwN2I5YTkxfQ==" | base64 -d

