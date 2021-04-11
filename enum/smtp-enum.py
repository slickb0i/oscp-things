# A simple python script to enumerate usernames using an smtp server

import socket
import sys

class Socket(socket.socket):
    def recv_until(self, delim):
        buf = ""
        while True:
            c = self.recv(1)
            buf += c.decode()
            if delim in buf:
                break
        return buf

if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} [host]:[port] [file]")
    exit(1)

host = sys.argv[1].split(':')[0]
port = int(sys.argv[1].split(':')[1])
usr_file = sys.argv[2]

# Read all usernames in
usernames = []
with open(usr_file, 'r') as usr_fh:
    usernames = [ usr.strip() for usr in usr_fh.readlines() ]

s = Socket(socket.AF_INET, socket.SOCK_STREAM)
print("\n[+] Running smtp username enum against server {0} [+]".format(host))

try:
    s.connect((host, port))
    banner = s.recv_until('\r')
    print(banner)

    for usr in usernames:
        vrfy = 'VRFY {}\r\n'.format(usr)
        s.send(vrfy.encode())
        resp = s.recv_until('\r')
        print(resp)
        if "VRFY is not supported" in resp:
            print("[-] VRFY command not supported by this smtp server. Skipping...")
            break
    s.close()
except ConnectionRefusedError:
    print("[+] Server refused connection to smtp service")
finally:
    print("[+] ----------------------------------------------------- [+]")
