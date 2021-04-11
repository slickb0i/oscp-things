@echo off

Rem TODO
Rem - find domain users

echo /========================================/  > output.txt
echo /---------- User information ------------/ >> output.txt
echo /========================================/ >> output.txt
echo. >> output.txt

echo /====================/ Current user /====================/ >> output.txt
whoami >> output.txt
echo. >> output.txt

echo /====================/ Current user information /====================/ >> output.txt
net user %USERNAME% >> output.txt
echo. >> output.txt

echo /====================/ Users on system /====================/ >> output.txt
net user >> output.txt
echo. >> output.txt

echo /========================================/ >> output.txt
echo /---------- System information ----------/ >> output.txt
echo /========================================/ >> output.txt
echo. >> output.txt

echo /====================/ System info  /====================/ >> output.txt
systeminfo >> output.txt
echo. >> output.txt

echo /====================/ Hostname /====================/ >> output.txt
hostname >> output.txt
echo. >> output.txt

echo /====================/ Running tasks /====================/ >> output.txt
tasklist /SVC >> output.txt
echo. >> output.txt

echo /====================/ Running as root: /====================/ >> output.txt
tasklist /SVC /FI "USERNAME eq NT AUTHORITY\SYSTEM" >> output.txt
echo. >> output.txt

echo /====================/ Schedualed tasks /====================/ >> output.txt
schtasks /query /fo list | findstr /C:"TaskName:" >> output.txt
echo. >> output.txt

echo /========================================/ >> output.txt
echo /-------- Networking information --------/ >> output.txt
echo /========================================/ >> output.txt
echo. >> output.txt

echo /====================/ Network interfaces /====================/ >> output.txt
ipconfig /all >> output.txt
echo. >> output.txt

echo /====================/ Listening tasks /====================/ >> output.txt
netstat -ano >> output.txt
echo. >> output.txt

echo /====================/ Networking routes /====================/ >> output.txt
route print >> output.txt
echo. >> output.txt

echo /====================/ Hosts file /====================/ >> output.txt
type C:\Windows\system32\drivers\etc\hosts | findstr /V "^#" >> output.txt
echo. >> output.txt

echo /====================/ Arp cache /====================/ >> output.txt
arp -A >> output.txt
echo. >> output.txt

echo /====================/ Firewall state /====================/ >> output.txt
netsh firewall show state >> output.txt
echo. >> output.txt

echo /====================/ Firewall config /====================/ >> output.txt
netsh firewall show config >> output.txt
echo. >> output.txt

echo /========================================/ >> output.txt
echo /----------- Useful binaries ------------/ >> output.txt
echo /========================================/ >> output.txt
echo. >> output.txt

Set use_wmic = 0
wmic os get BuildNumber
if %ERRORLEVEL%==0 Set use_mic=1 && echo [+] wmic >> output.txt && where wmic >> output.txt

where curl && echo [+] curl >> output.txt && where curl >> output.txt
where python && echo [+] python >> output.txt && where python >> output.txt
where ruby && echo [+] ruby >> output.txt && where ruby >> output.txt
where plink && echo [+] plink >> output.txt && where plink >> output.txt
where putty && echo [+] putty >> output.txt && where putty >> output.txt

Rem echo /========================================/ >> output.txt
Rem echo /------------ Easy escalate -------------/ >> output.txt
Rem echo /========================================/ >> output.txt
Rem echo. >> output.txt
Rem 
Rem echo /====================/ Checking AlwaysInstallElevated Key  /====================/ >> output.txt
Rem reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevate >> output.txt
Rem 
Rem echo /====================/ Unquoted Paths /====================/ >> output.txt
Rem if %use_wmic%==1 wmic get displayname,pathname,startmode | findstr /i /v system32 | findstr /i /v """ >> output.txt
Rem echo. >> output.txt
