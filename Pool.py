#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'wufulin'

import MySQLdb
import string


class PoolConnection:

    def __init__(self, maxconnections, connstr, dbtype):
        from Queue import Queue
        self._pool = Queue(maxconnections)
        self.connstr = connstr
        self.dbtype = dbtype
        self.maxconnections = maxconnections

        try:
            for i in range(maxconnections):
                self.addConnection(self.createConnection(connstr, dbtype))
        except Exception, e:
            raise e

    def addConnection(self, conn):
        try:
            self._pool.put(conn)
        except Exception, e:
            raise "addConnection error:"+str(e)

    def returnConnection(self, conn):
        try:
            self._pool.put(conn)
        except Exception, e:
            raise "returnConnection error:"+str(e)

    def getConnection(self):
        try:
            return self._pool.get()
        except Exception, e:
            raise 'getConnection error:'+str(e)

    def closeConnection(self):
        try:
            self._pool.get().close()
            self.addConnection(self.createConnection(self.connstr, self.dbtype))
        except Exception, e:
            raise 'closeConnection error:'+str(e)

    def createConnection(self, connstr, dbtype):
        if dbtype == 'mysql':
            try:
                db_conn = connstr.split('#')
                conndb = MySQLdb.connect(user=db_conn[0],
                                         passwd=db_conn[1],
                                         host=db_conn[2],
                                         port=string.atoi(db_conn[3]),
                                         db=db_conn[4])
                conndb.ping()
                return conndb
            except Exception, e:
                raise 'Error %s !' % str(e)


class A(object):

    @classmethod
    def createA(cls, name):
        instance = cls.__new__(cls)
        instance.__dict__['name'] = name
        return instance

    def __repr__(self):
        return self.name

if __name__ == '__main__':
    connstring = "root#root#localhost#3306#mysql"
    mysqlpool = PoolConnection(1, connstring, "mysql")
    conn = mysqlpool.getConnection()

    cursor = conn.cursor()
    cursor.execute(r"select * from user")
    result = cursor.fetchone()
    print(result)
    conn.close()
