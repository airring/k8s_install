# coding=utf-8

import pymysql
import queue
from k8s import settings
import logging
logger = logging.getLogger('sourceDns.webdns.views')


REQUIRED_PARAMS = ["host", "user", "passwd", "db"]
DB_CONNET = {'host': '192.168.3.105',
             'port': 3306,
             'user': 'root',
             'passwd': 'rrjc2018',
             'db': 'kubernetes'}


class ConnectionPool():

    def __init__(self, maxsize=10, **kwargs):
        self.kwargs = DB_CONNET

        self._queue = queue.Queue(maxsize=maxsize)

        for i in range(maxsize):
            self._queue.put(self._create())

    def _create(self):
        for param in REQUIRED_PARAMS:
            if self.kwargs.get(param, None) is None:
                raise Exception(
                    "Instantiation failed, '{0}' param is not found.".format(
                        param
                    )
                )

        return pymysql.connect(**DB_CONNET, cursorclass=pymysql.cursors.DictCursor)

    def _put(self, conn):
        self._queue.put(conn)

    def _get(self):
        conn = self._queue.get()
        if conn is None:
            return self._create()

        return conn

    def execute(self, sql, args=None, exec_many=False, return_one=False):
        """
        执行 sql 操作
        :param sql: sql 语句
        :param args: 对应参数
        :param exec_many: 是否开启 `cur.executemany(sql, args)`
        :param return_one: 是否开启 `cur.fetchone()`
        """
        conn = self._get()
        try:
            with conn as cur:
                if exec_many:
                    cur.executemany(sql, args)
                else:
                    cur.execute(sql, args)
                return cur.fetchone() if return_one else cur.fetchall()

        except Exception as e:
            raise e

        finally:
            self._queue.put(conn)

    @property
    def size(self):
        return self._queue.qsize()

    def __del__(self):
        """
        确保每个链接实例最后都会被释放
        """
        while not self._queue.empty():
            conn = self._queue.get_nowait()
            if conn:
                conn.close()

# pool = ConnectionPool(
#     # maxsize=100, maxsize 非必须，用于指定最大连接数
#     host="192.168.3.105",
#     port=3306,
#     user="root",
#     passwd="rrjc2018",
#     db="kubernetes"
# )
