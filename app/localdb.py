import sqlite3


def createdb(dbname):
    open(dbname, 'a')
    dbobj = cplocaldb(dbname)
    dbobj.cursor.execute(
        'CREATE TABLE objects (uid text PRIMAR KEY, name text, type text);')


class cplocaldb(object):
    def __init__(self, database):
        self.database = database
        self.dbconn = sqlite3.connect(database, check_same_thread=False)
        self.dbconn.row_factory = sqlite3.Row
        self.cursor = self.dbconn.cursor()

    def insert_object(self, cpobject):
        self.cursor.execute(
            'INSERT INTO objects VALUES("{}", "{}", "{}")'.format(
                cpobject['uid'], cpobject['name'], cpobject['type']))

    def delete_object(self, uid):
        self.cursor.execute('DELETE FROM objects WHERE uid="{}";'.format(uid))

    def object_counter(self):
        self.cursor.execute('SELECT (select count() from objects) as count;')
        objcount = self.cursor.fetchall()
        return objcount[0][0]

    def uidcheck(self, uid):
        self.cursor.execute(
            'SELECT uid FROM objects WHERE uid="{}";'.format(uid))
        objfind = self.cursor.fetchall()
        for obj in objfind:
            if obj[0] == None:
                return False
            else:
                return True

    def local_uids(self):
        self.cursor.execute('SELECT uid, type FROM objects;')
        all_uid = self.cursor.fetchall()
        return [uid[0] for uid in all_uid]

    def allobjects(self):
        nettypes = ['host', 'network', 'group']
        servtypes = ['service-tcp', 'service-udp', 'service-group']
        all_objects = {
            'networkobjects': [],
            'serviceobjects': [],
            'targets': []
        }
        self.cursor.execute('SELECT * FROM objects')
        dbresp = self.cursor.fetchall()
        for row in dbresp:
            if row[2] in nettypes:
                all_objects['networkobjects'].append(row)
            elif row[2] in servtypes:
                all_objects['serviceobjects'].append(row)
            else:
                all_objects['networkobjects'].append(row)
                if 'host' in row[2].lower():
                    # Check Point Management Object
                    pass
                else:
                    all_objects['targets'].append(row)
        return all_objects
