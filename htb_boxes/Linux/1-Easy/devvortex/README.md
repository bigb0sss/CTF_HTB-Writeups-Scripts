# Devvortex (Easy - Linux)

## Recon
### Nmap (TCP)
```console
# nmap -Pn --open -T4 -sV -sC -p- 10.10.11.242
Starting Nmap 7.94 ( https://nmap.org ) at 2024-04-29 23:04 EDT
Nmap scan report for 10.10.11.242
Host is up (0.033s latency).
Not shown: 65533 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://devvortex.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.79 seconds
```
* 80/TCP - Web server 

### Subdomain enum
```console
$ wfuzz -w subdomains-top1million-20000.txt -H "Host: FUZZ.devvortex.htb" --hc 302 -t 80 10.10.11.242

********************************************************
* Wfuzz 3.1.0 - The Web Fuzzer                         *
********************************************************

Target: http://10.10.11.242/
Total requests: 19966

=====================================================================
ID           Response   Lines    Word       Chars       Payload                                                                                                                                                                             
=====================================================================

000000019:   200        501 L    1581 W     23221 Ch    "dev"                                                                                                                                                                               

Total time: 0
Processed Requests: 19966
Filtered Requests: 19965
Requests/sec.: 0
```

Need to update the virtual host config:
```console
┌──(root㉿kali)-[/opt]
└─# cat /etc/hosts
...

10.10.11.242    devvortex.htb dev.devvortex.htb
```


## Initial Access


### user.txt


## Privesc


### root.txt

¬