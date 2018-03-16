import sqlite3

def createdb(dbname):
    open(dbname, 'a')
    dbobj = sqlhelper(dbname)
    dbobj.cursor.execute('CREATE TABLE hosts (uid text PRIMARY KEY, name text, ip4 text, ip6 text);')
    dbobj.cursor.execute('CREATE TABLE networks (uid text PRIMARY KEY, name text, net4 text, mask4 text, net6 text, mask6 text);')
    dbobj.cursor.execute('CREATE TABLE groups (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE access_roles (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE servers (uid text PRIMARY KEY, name text);')
    dbobj.cursor.execute('CREATE TABLE services (uid text PRIMARY KEY, name text, port text, protocol text);')
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
            if 'ipv4-address' in cpobject and 'ipv6-address' in cpobject:
                self.insert_host(cpobject['uid'], cpobject['name'], cpobject['ipv4-address'], cpobject['ipv6-address'])
            elif 'ipv4-address' in cpobject:
                self.insert_host(cpobject['uid'], cpobject['name'], cpobject['ipv4-address'], None)
            elif 'ipv6-address' in cpobject:
                self.insert_host(cpobject['uid'], cpobject['name'], None, cpobject['ipv6-address'])
        elif cpobject['type'] == 'network':
            if 'subnet4' in cpobject and 'subnet6' in cpobject:
                self.insert_network(cpobject['uid'], cpobject['name'], cpobject['subnet4'], cpobject['mask-length4'], cpobject['subnet6'], cpobject['mask-length6'])
            elif 'subnet4' in cpobject:
                self.insert_network(cpobject['uid'], cpobject['name'], cpobject['subnet4'], cpobject['mask-length4'], None, None)
            elif 'subnet6' in cpobject:
                self.insert_network(cpobject['uid'], cpobject['name'], None, None, cpobject['subnet6'], cpobject['mask-length6'])
        elif cpobject['type'] == 'group':
            self.insert_group(cpobject['uid'], cpobject['name'])
        elif cpobject['type'] == 'service-tcp':
            self.insert_service(cpobject['uid'], cpobject['name'], cpobject['port'], 'TCP')
        elif cpobject['type'] == 'service-udp':
            self.insert_service(cpobject['uid'], cpobject['name'], cpobject['port'], 'UDP')
        elif cpobject['type'] == 'access-role':
            self.insert_access_role(cpobject['uid'], cpobject['name'])
        else:
            self.insert_server(cpobject['uid'], cpobject['name'])

    def insert_host(self, uid, name, ip4, ip6):
        self.cursor.execute('INSERT INTO hosts (uid, name, ip4, ip6) VALUES ("{}", "{}", "{}", "{}");'.format(uid, name, ip4, ip6))

    def insert_network(self, uid, name, net4, mask4, net6, mask6):
        self.cursor.execute('INSERT INTO networks (uid, name, net4, mask4, net6, mask6) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(uid, name, net4, mask4, net6, mask6))

    def insert_group(self, uid, name):
        self.cursor.execute('INSERT INTO groups (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def insert_access_role(self, uid, name):
        self.cursor.execute('INSERT INTO access_roles (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def insert_server(self, uid, name):
        self.cursor.execute('INSERT INTO servers (uid, name) VALUES ("{}", "{}");'.format(uid, name))

    def insert_service(self, uid, name, port, protocol):
        self.cursor.execute('INSERT INTO services (uid, name, port, protocol) VALUES ("{}", "{}", "{}", "{}");'.format(uid, name, port, protocol))

    def get_hosts(self):
        response = {'objects': [], 'total': 0}
        self.cursor.execute('SELECT name FROM hosts;')
        hosts = self.cursor.fetchall()
        for host in hosts:
            response['total'] += 1
            response['objects'].append(host[0])
        return response

    def get_networks(self):
        response = {'objects': [], 'total': 0}
        self.cursor.execute('SELECT name FROM networks;')
        networks = self.cursor.fetchall()
        for net in networks:
            response['total'] += 1
            response['objects'].append(net[0])
        return response

    def get_groups(self):
        response = {'objects': [], 'total': 0}
        self.cursor.execute('SELECT name FROM groups;')
        groups = self.cursor.fetchall()
        for group in groups:
            response['total'] += 1
            response['objects'].append(group[0])
        return response

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

    def check_local(self, cpuid):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table for table in self.cursor]
        for table in tables:
            self.cursor.execute
