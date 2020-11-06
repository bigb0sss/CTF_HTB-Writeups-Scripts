# hexIPv6.py

import sys

hexIPv6 = sys.argv[1].split(".")

ip = ""

for i in hexIPv6:
    ip += hex(int(i))[2:].rjust(2, "0")

print ".".join(ip[i:i+4] for i in range(0, len(ip), 4))
