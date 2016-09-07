# -*- coding: UTF-8 -*-
import MySQLdb


class Db(object):
    """docstring for Db"""
    connect = None
    cursor = None
    connectEoor = None

    def __init__(self, **arg):
        super(Db, self).__init__()
        if arg is None:
            raise 'link info not empty!'
        self.Host = arg['host']
        self.User = arg['user']
        self.Pwd = arg['password']
        self.dbbase = arg['dbbase']
        try:
            self.connect = MySQLdb.connect(
                self.Host, self.User, self.Pwd, self.dbbase)
            self.cursor = self.connect.cursor()
        except MySQLdb.Error, e:
            try:
                self.connectEoor = "Error %d:%s" % (e.args[0], e.args[1])
            except IndexError:
                self.connectEoor = "MySQL Error:%s" % str(e)

    def ifConnectEoor(self):
        if self.connectEoor:
            return self.connectEoor
        else:
            return False

    def queryAction(self, sql, param=None):
        self.cursor.execute(sql, param)
        return self.cursor.fetchall()
