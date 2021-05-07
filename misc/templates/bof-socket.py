#!/bin/python3

import pwnlib.util.cyclic as pattern
from socket import *
import string
import telnetlib
import time

addr = ""
port =

# --------- TCP Client --------- #

class TCPClient():
    def __init__(self, host, port):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((host, port))

    def send(self, data):
        nsend = self.sock.send(data)
        return data

    def sendline(self, data):
        data += b'\n'
        self.sock.send(data)
        return data

    def recv(self, size=1024, delay=0):
        if delay:
            time.sleep(delay)
        buf = self.sock.recv(size).decode()
        return buf

    def recv_until(self, delim):
        buf = ""
        while True:
            c = self.sock.recv(1).decode()
            buf += c
            if delim in buf:
                break
        return buf

    def recvline(self):
        buf = self.recv_until("\n")
        return buf

    def close(self):
        self.sock.close()

# --------- Fuzzing Server --------- #

def fuzz_server(client, start, end, skip):
    for i in range(start,end,skip):
        fuzz = pattern.cyclic(i, alphabet=string.ascii_letters)
        print("[+] Fuzzing with {0} characters".format(len(fuzz)))
        client.sendline(fuzz.encode('ascii'))
        time.sleep(1)

def check_pattern(s):
    print("[+] Checking pattern")
    index = pattern.cyclic_find(s, alphabet=string.ascii_letters)
    print("[+] Pattern at {}".format(index))
    exit(0)

# --------- Main --------- #

def main():
    print("[+] Connecting to client")
    client = TCPClient(addr,port)
    print("[+] Connection established")

main()


# Bad Characters
#   tst = set([ i for i in range (0, 0x100) ])
#   bad = set([0x00])
#   payload = bytes(tst - bad)
