import sqlite3


def createdb(dbname):
    tables = ['hosts', 'networks', 'groups', 'access_roles', 'servers']
    open(dbname, 'a')
    dbobj = cplocaldb(dbname)
    for table in tables:
        dbobj.cursor.execute(
        'CREATE TABLE {} (uid text PRIMARY KEY, name text);'.format(table))


class sqlhelper(object):
    def __init__(self, database):
        self.database = database
        self.dbconn = sqlite3.connect(database, check_same_thread=False)
        self.dbconn.row_factory = sqlite3.Row
        self.cursor = self.dbconn.cursor()
