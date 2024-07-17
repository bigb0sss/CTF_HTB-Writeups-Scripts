# HTB Commands

## Enumeration
### port scan

```console
# Nmap
nmap -Pn --open -sC -sV -p- <IP>
```

### subdomain enum
```console
# wfuzz
wfuzz -w <Wordlist> -H "Host: FUZZ.devvortex.htb" --hc 403,400 -t 80 10.10.11.24
```
