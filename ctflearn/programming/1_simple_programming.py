#!/usr/bin/python3

def countNum():
    howMany_zero = 0
    howMany_one = 0

    for i in open("data.dat", "r"):
        zero = i.count('0')
        one = i.count('1')

        if zero % 3 == 0:
            howMany_zero += 1
        elif one % 2 == 0:
            howMany_one += 1
        else:
            pass
    
    print(f"[INFO] zero: {howMany_zero}")
    print(f"[INFO] one: {howMany_one}")
    print("[INFO] Answer: %s" % (howMany_zero + howMany_one))

if __name__ == '__main__':
    countNum()
