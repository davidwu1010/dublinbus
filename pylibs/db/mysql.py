# -*- coding: utf-8 -*-

import time
import pymysql.cursors


class Mysql(object):

    def __init__(self, host, port, user, pwd, db):
        self._conn = None
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd
        self._db = db
        self.connect()

    def __del__(self):
        self.close()

    def ping(self):
        try:
            self._conn.ping()
            return True
        except Exception as error:
            print(error)
            return False

    def connect(self):
        try:
            self._conn = pymysql.connect(host=self._host,
                                         user=self._user,
                                         passwd=self._pwd,
                                         db=self._db,
                                         port=self._port,
                                         charset='utf8mb4')
            self._conn.autocommit(False)
            return True
        except Exception as e:
            print(e)
            return False

    def reconnect(self):
        try:
            while True:
                if not self.ping():
                    self.connect()
                else:
                    break
                time.sleep(1)
        except Exception as error:
            print(error)

    def commit(self):
        try:
            self._conn.commit()
            return True
        except Exception as error:
            self.rollback()
            print(error)
            return False

    def rollback(self):
        try:
            self._conn.rollback()
            return True
        except Exception as error:
            print(error)
            return False

    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
            return True
        except Exception as error:
            print(error)
            return False

    def execute(self, sql, para=None):
        try:
            self.reconnect()
            cur = self._conn.cursor()
            cur.execute(sql, para)
            self._conn.commit()
            cur.close()
            return True
        except Exception as error:
            print('[{}] insert failed:{}'.format(sql, str(error)))
            return False
    
    def executemany(self, sql, para):
        try:
            self.reconnect()
            cur = self._conn.cursor()
            rowcount = cur.executemany(sql, para)
            self._conn.commit()
            cur.close()
            return rowcount
        except Exception as error:
            print(error)
            return 0

    def query(self, sql, para=None, cursor=None):
        try:
            self.reconnect()
            if cursor:
                cur = self._conn.cursor(cursor=pymysql.cursors.Cursor)
            else:
                cur = self._conn.cursor(cursor=pymysql.cursors.DictCursor)
            cur.execute(sql, para)
            r = cur.fetchall()
            self._conn.commit()
            cur.close()
            return r
        except Exception as error:
            print('[{}] query failed:{}'.format(sql, str(error)))
            return False
    
    def query_one(self, sql, para=None, cursor=None):
        r = self.query(sql, para, cursor)
        if r:
            return r[0]
        else:
            return {}


def test():
    pass


def main():
    return test()


if __name__ == '__main__':
    pass
