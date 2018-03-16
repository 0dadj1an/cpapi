import sqlite3

def createdb(dbname):
    open(dbname, 'a')
    dbobj = sqlhelper(dbname)
    dbobj.cursor.execute('CREATE TABLE hosts (uid text PRIMARY KEY, name text, ipaddress text);')
    dbobj.cursor.execute('CREATE TABLE networks (uid text PRIMARY KEY, name text, network text, mask text);')
    dbobj.cursor.execute('CREATE TABLE groups (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE access_roles (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE servers (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE services (uid text PRIMARY KEY, name text, protocol text);')
    dbobj.dbconn.commit()


class sqlhelper(object):
    def __init__(self, database):
        self.database = database
        self.dbconn = sqlite3.connect(database, check_same_thread=False)
        self.dbconn.row_factory = sqlite3.Row
        self.cursor = self.dbconn.cursor()
        self.tables = ['hosts', 'networks', 'groups', 'access_roles', 'servers', 'services']

    def insert_object(self, cpobject):
        if cpobject['type'] == 'host':
            self.insert_host(cpobject['uid'], cpobject['name'], cpobject['ipv4-address'])
        elif cpobject['type'] == 'network':
            self.insert_network(cpobject['uid'], cpobject['name'], cpobject['subnet4'], cpobject['mask-length4'])
        elif cpobject['type'] == 'group':
            self.insert_network(cpobject['uid'], cpobject['name'])
        elif cpobject['type'] == 'service-tcp' or cpobject['type'] == 'service-udp':
            self.insert_service(cpobject['uid'], cpobject['name'], cpobject['protocol'])
        elif cpobject['type'] == 'access-role':
            self.insert_access_role(cpobject['uid'], cpobject['name'])
        else:
            self.insert_server(cpobject['uid'], cpobject['name'])

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

    def insert_service(self, uid, name, protocol):
        self.cursor.execute('INSERT INTO services (uid, name, protocol) VALUES ("{}", "{}", "{}");'.format(uid, name, protocol))

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

    def get_services(self):
        self.cursor.execute('SELECT * FROM services;')

    def total_objects(self):
        local_total = 0
        for table in self.tables:
            self.cursor.execute('SELECT (select count() from {}) as count;'.format(table))
            objcount = self.cursor.fetchall()
            local_total += objcount[0][0]
        return local_total
