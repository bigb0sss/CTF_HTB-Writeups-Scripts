#!/usr/bin/python3

import requests

def toxic(url, format):


    r = requests.get(url + format + payload_3)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    url = 'http://46.101.14.236:32650/'
    format = ''
    
    toxic(url, format)