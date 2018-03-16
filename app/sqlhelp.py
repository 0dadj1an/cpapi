import sqlite3


def createdb(dbname):
    tables = ['hosts', 'networks', 'groups', 'access_roles', 'servers']
    open(dbname, 'a')
    dbobj = sqlhelper(dbname)
    dbobj.cursor.execute('CREATE TABLE hosts (uid text PRIMARY KEY, name text, ipaddress text);')
    dbobj.cursor.execute('CREATE TABLE networks (uid text PRIMARY KEY, name text, network text, mask text);')
    dbobj.cursor.execute('CREATE TABLE groups (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE access_roles (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE servers (uid text PRIMARY KEY, name text);')
    dbobj.dbconn.commit()


class sqlhelper(object):
    def __init__(self, database):
        self.database = database
        self.dbconn = sqlite3.connect(database, check_same_thread=False)
        self.dbconn.row_factory = sqlite3.Row
        self.cursor = self.dbconn.cursor()


    def insert_host(self, uid, name, ipaddress):
        self.cursor.execute('INSERT INTO hosts (uid, name, ipaddress) VALUES ("{}", "{}", "{}");'.format(uid, name, ipaddress))

    def insert_network(self, uid, name, network, mask):
        self.cursor.execute('INSERT INTO networks (uid, name, network, mask) VALUES ("{}", "{}", "{}", "{}");'.format(uid, name, network, mask))

    def insert_group(self, uid, name):
        self.cursor.execute('INSERT INTO groups (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def insert_access_role(self, uid, name):
        self.cursor.execute('INSERT INTO access_roles (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def insert_server(self, uid, name):
        self.cursor.execute('INSERT INTO servers (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def get_hosts(self):
        self.cursor.execute('SELECT * FROM hosts;')

    def get_networks(self):
        self.cursor.execute('SELECT * FROM networks;')

    def get_groups(self):
        self.cursor.execute('SELECT * FROM groups;')

    def get_access_roles(self):
        self.cursor.execute('SELECT * FROM access_roles;')

    def get_servers(self):
        self.cursor.execute('SELECT * FROM servers;')
