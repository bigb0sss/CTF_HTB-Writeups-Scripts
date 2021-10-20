#!/usr/bin/python3

# WIP!!!!!

import requests

def login(url, url_login):

    data = {
        'username' : 'test',
        'password' : 'pass',
    }

    r = requests.post(url + url_login, data=data)
    print(r.text)

def weather(url, url_weather):

    data = {
        'endpoint' : 'openweathermap.org',
        'city' : 'Toronto',
        'country' : 'CA',
    }

    r = requests.post(url + url_weather, data)
    print(r.text)


if __name__ == '__main__':
    url = 'http://157.245.32.65:31557/'

    url_login = "login"
    url_register = "register"
    url_weather = "api/weather"
    
    #login(url, url_login)
    weather(url, url_weather)