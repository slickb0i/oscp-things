#!/bin/sh

outfile="output.txt"

print(){
    printf '%b ' "$@\n\c"
}

print "/========================================/" | tee $outfile
print "/---------- User information ------------/" | tee -a $outfile
print "/========================================/\n" | tee -a $outfile

print "/=========================/ Hostname /========================/\n" | tee -a $outfile
print "$(hostname)\n" | tee -a $outfile

print "/=====================/ Users on System /=====================/\n" | tee -a $outfile
print "$(cat /etc/passwd)\n" | tee -a $outfile

print "/======================/ Current User /=======================/\n" | tee -a $outfile
print "$(whoami)\n" | tee -a $outfile

print "/==================/ Current Users groups /===================/\n" | tee -a $outfile
print "$(groups)\n" | tee -a $outfile

print "/===================/ Current environment /===================/\n" | tee -a $outfile
print "$(env)\n" | tee -a $outfile

print "/========================================/" | tee -a $outfile
print "/--------- System information -----------/" | tee -a $outfile
print "/========================================/\n" | tee -a $outfile

print "/====================/ Operating System /=====================/\n" | tee -a $outfile
print "$(cat /etc/*release || cat /etc/issue)\n" | tee -a $outfile

print "/=======================/ Kernel info /=======================/\n" | tee -a $outfile
print "$(uname -a)\n" | tee -a $outfile

print "/======================/ Running tasks /======================/\n" | tee -a $outfile
print "$(ps -ax -o euser,pid,%cpu,%mem,cmd)\n" | tee -a $outfile

print "/======================/ Cron files /=========================/\n" | tee -a $outfile
print "$(ls -al /etc/cron*)\n" | tee -a $outfile

print "/========================================/" | tee -a $outfile
print "/------- Networking information ---------/" | tee -a $outfile
print "/========================================/\n" | tee -a $outfile

print "/===================/ Network Interfaces /====================/\n" | tee -a $outfile
print "$(ip addr list || ifconfig )\n" | tee -a $outfile

print "/=================/ Active TCP Connections /==================/\n" | tee -a $outfile
print "$(ss -antp || netstat -antp)\n" | tee -a $outfile

print "/=================/ Active UDP Connections /==================/\n" | tee -a $outfile
print "$(ss -antp || netstat -antp)\n" | tee -a $outfile

print "/===================/ Routing Information /===================/\n" | tee -a $outfile
print "$(ip route || route)\n" | tee -a $outfile

print "/========================/ ARP cache /========================/\n" | tee -a $outfile
print "$(ip neigh show || arp -e)\n" | tee -a $outfile

print "/=====================/ etc-hosts file /=====================/\n" | tee -a $outfile
print "$(cat /etc/hosts)\n" | tee -a $outfile

print "/=====================/ IPTables Config /====================/\n" | tee -a $outfile
print "$(iptables -L 2>/dev/null)\n" | tee -a $outfile

print "/========================================/" | tee -a $outfile
print "/----------- Useful Binaries ------------/" | tee -a $outfile
print "/========================================/\n" | tee -a $outfile

if which curl > /dev/null ; then print "[+] curl\n$(which curl)\n" | tee -a $outfile; fi
if which wget > /dev/null ; then print "[+] wget\n$(which wget)\n" | tee -a $outfile; fi
if which nc > /dev/null ; then print "[+] nc\n$(which nc)\n" | tee -a $outfile; fi
if which ncat > /dev/null ; then print "[+] ncat\n$(which ncat)" | tee -a $outfile; fi
if which python > /dev/null ; then print "[+] Python\nVersion: $(python --version 2>&1)\n$(which python)\n" | tee -a $outfile; fi
if which python3 > /dev/null ; then print "[+] Python3\nVersion: $(python3 --version 2>&1)\n$(which python3)\n" | tee -a $outfile; fi
if which ssh > /dev/null ; then print "[+] SSH\nVersion: $(ssh -V 2>&1)\n$(which ssh)\n" | tee -a $outfile; fi

print "/========================================/" | tee -a $outfile
print "/------------ Easy Priv Esc -------------/" | tee -a $outfile
print "/========================================/\n" | tee -a $outfile

find /etc/passwd -writable -exec print '[+] /etc/passwd is writable' \; | tee -a $outfile
find /etc/shadow -readable -exec print '[+] /etc/shadow is readable' \; | tee -a $outfile
find /root/ -maxdepth 3 -name .ssh -type d -exec print "[+] SSH directory found:" {} \; 2>/dev/null | tee -a $outfile
find /home/ -maxdepth 3 -name .ssh -type d -exec print "[+] SSH directory found:" {} \; 2>/dev/null | tee -a $outfile

# # Lets first check that we can run commands
# print "[+] Checking path quickly to ensure we can continue" | tee -a $outfile
# if [ -z "$PATH" ]; then
#     PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/system/bin:/system/sbin:/system/xbin"
#     print "[+] PATH was empty! Setting some popular locations, hopefully these still work!" | tee -a $outfile
# fi
