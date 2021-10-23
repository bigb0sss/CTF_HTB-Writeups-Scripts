# CTF / Hacking Practice

## [GameofHacks](https://www.gameofhacks.com/)


## hackthebox
### boxes
| Machines | Difficulty | Write-up | Vulnerabilities |
| :--- | :---: | :--- | :-- |
| Luke | Medium | [Read](https://medium.com/@bigb0ss/htb-luke-write-up-77aa52320250) | |
| SwagShop | Easy | [Read](https://medium.com/@bigb0ss/htb-swagshop-write-up-50a560aa7a56?sk=8bc4c4a5bbf0707c158d1305f3e0143d) | |
| JSON | Medium | [Read](https://medium.com/@bigb0ss/htb-json-write-up-6f91f89bcbf1) | |
| Zetta | Hard | [Read](https://medium.com/@bigb0ss/htb-zetta-write-up-be2fff5e2305) | |
| Scavenger | Hard | [Read](https://medium.com/@bigb0ss/htb-scavenger-write-up-fee11d971774) | Whois SQLi, Rootkit, Exim SMTP 4.8.9 Exploit |
| Postman | Easy | [Read](https://medium.com/@bigb0ss/htb-postman-write-up-34bc4fe5daa) | Redis Service Abuse, Webmin CVE 2019-12840 |
| Registry | Hard | [Read](https://medium.com/@bigb0ss/htb-registry-write-up-b4255bd78712) | Docker Registry API, Restic backups |
| Mango | Medium | [Read](https://medium.com/@bigb0ss/htb-mango-write-up-52fdd7e67cc6) | NoSQL Injection, SUID Abuse (GTFobins) |
| Obscurity | Medium | [Read](https://medium.com/@bigb0ss/htb-obscurity-write-up-bc65f61cd255) | Python Web Server |
| Forest | Easy | [Read](https://medium.com/@bigb0ss/htb-forest-write-up-fdd45e8e73bf) | AS-REP Roasting, Exchange AD Exploitation |
| Blunder | Easy | [Read](https://bigb0sss.github.io/posts/htb-blunder-writeup/) | Bludit CMS Exploit, Sudo Bypass |
| Cache | Medium | [Read](https://bigb0sss.github.io/posts/htb-cache-writeup/) | OpenEMR, SQLi, Memcached, Doker |
| Mischief | Insane | [Read](https://bigb0sss.github.io/posts/htb-mischief-writeup/) | SNMP, IPv6, ICMP Info Leak, Systemd-run |
| Tabby | Easy | [Read](https://bigb0sss.github.io/posts/htb-tabby-writeup/) | LFI, Tomcat, zip2john, LXD, Container |
| Valentine | Easy | [Read](https://bigb0sss.github.io/posts/htb-valentine-writeup/) | OpenSSL, Heartbleed, Tmux |
| Bounty | Easy | [Read](https://bigb0sss.github.io/posts/htb-bounty-writeup/) | Web.config RCE, Juicy Potato |
| Frolic | Easy | [Read](https://bigb0sss.github.io/posts/htb-frolic-writeup/) | Frackzip, playSMS RCE, ret2libc |

### challenges
| Web Challenge | Difficulty | |
| :--- | :---: | :--- |
| Emdee Five for Life | Easy | [Write-up](https://medium.com/@bigb0ss/htb-web-challenge-emdee-five-for-life-56cb0ddfd63f) | 
<br />

## Protostar Walkthrough ([Exploit Exercise](http://exploit-exercises.lains.space/protostar/))
|Module |Link   |Note  |
| :---  | :---  | :--- |
|Stack0 |[Stack BOF Intro](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack0-214e8cbccb04)   |Basic buffer overflow abusing gets() function | 
|Stack1 |[Stack BOF Basic1](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack1-2f28302559fc)  |Basic buffer overflow abusing strcpy() function |
|Stack2 |[Stack BOF Basic2](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack2-d6cb2e467853)  |Basic buffer overflow abusing strcpy() function |
|Stack3 |[Stack BOF Basic3](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack3-7db54291f867)  |Basic buffer overflow abusing gets() function |
|Stack4 |[Stack BOF Basic4](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack-4-bde92b7b6b38) |Basic buffer overflow abusing gets() function |
|Stack5 |[Stack BOF Shellcode](https://medium.com/bugbountywriteup/expdev-exploit-exercise-protostar-stack-5-c8d085c914e6) | Stack-based buffer overflow to get a root shell |
|Stack6 |[Stack BOF ret2libc](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack-6-ef75472ec7c6)  |Stack-based bufferoverflow + ret2libc |
|Stack7 |[Stack BOF ret2.text](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-stack-7-fea3ac85ffe7) |Stack-based bufferoverflow + ret2.text |
|Format0  |[Format String Exploit Intro](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-format-0-332983bfd388) |Intro to Format String vulnerability |
|Format1  |[Format String Basic1](https://medium.com/bugbountywriteup/expdev-exploit-exercise-protostar-format-1-c5182332a69a) |Basic Format String Exploit |
|Format2  |[Format String Basic2](https://medium.com/bugbountywriteup/expdev-exploit-exercise-protostar-format-2-73ef08011a8c) |Basic Format String Exploit (4-byte Write) |
|Format3  |[Format String Basic3](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-format-3-33e8d8f1e83) |Basic Format String Exploit (4/2/1-byte Write) |
|Format4  |[Format String Exploit: GOT](https://medium.com/@bigb0ss/expdev-exploit-exercise-protostar-format-4-e2907b4716d1) |Format String Exploit overwriting the entry of GOT |
<br>

## Vulnserver (Binary Exploitation)
|Series |Link |Command |Vulnerability | Note |
| :---  | :---  | :--- | :--- | :--- |
|Part 1 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-1-ba35b9e36478) | N/A | N/A | Lab Setup |
|Part 2 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-2-46de4dd7bdde) | TRUN | EIP Overwrite | 
|Part 3 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-3-24859bd31c0a) | GMON | SEH Overwrite + Short JMP + Egghunter |
|Part 4 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-4-a5529731f0f1) | KSTET | EIP Overwrite + Short JMP + Egghunter |
|Part 5 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-5-10942c8c4395) | HTER | EIP Overwrite + Restricted Characters + Manual Offset Finding |
|Part 6 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-6-8c98fcdc9131) | GTER | EIP Overwrite + Socket Reuse Exploit |
|Part 7 |[Read](https://medium.com/@bigb0ss/expdev-vulnserver-part-7-bfe9fb5fd1e6) | LTER | SEH Overwrite + Restricted Characters + Encoded Payloads |

## Resources
* https://github.com/roya0045/Pentest-practice (List of practice sites)
* https://securityscorecard.com/blog/common-web-application-vulnerabilities-explained (41 Web vuln explained)