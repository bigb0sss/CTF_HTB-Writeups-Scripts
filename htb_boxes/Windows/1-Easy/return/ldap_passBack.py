#!/usr/bin/python3

import requests
import sys

def connect(url, endpoint):

	data = {
		"ip": sys.argv[1]
	}

	r = requests.post(url + endpoint, data=data)

if __name__ == '__main__':
	url = "http://10.10.11.108"
	endpoint = "/settings.php"

	connect(url, endpoint)