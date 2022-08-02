import os
import _pickle
import redis as redis
from starlette.exceptions import HTTPException
from utils.logger import Logger
import pymysql.cursors


class Db:
    logger = Logger()
    ttl: int = 5

    # Dict Cursor as default
    def __init__(self, cursor_class=pymysql.cursors.DictCursor):
        self.__cache_hash = None
        self.__result = None
        try:
            self.__mysql = pymysql.connect(
                host=os.getenv('DBHOST'),
                user=os.getenv('DBUSER'),
                password=os.getenv('DBPASS'),
                database=os.getenv('DBNAME'),
                cursorclass=cursor_class
            )
        except Exception:
            raise HTTPException(500, 'DB Connect Error')
        if os.getenv('REDISHOST', None):
            try:
                self.__redis = redis.Redis(
                    host=os.getenv('REDISHOST'),
                    password=os.getenv('REDISPASS', None)
                )
            except Exception:
                raise HTTPException(500, 'Redis Connect Error')
        else:
            self.__redis = None

    def query(self, query: str, params: tuple = None):
        self.make_hash(query, params)
        self.logger.add.debug("DB query: {}".format(query))
        self.logger.add.debug("DB params: {}".format(params))

        if self.redis and self.redis.get(self.cache_hash):
            self.logger.add.debug("Return from Cache: {}".format(self.cache_hash))
            self.__result = _pickle.loads(self.redis.get(self.cache_hash))
        else:
            with self.mysql:
                with self.mysql.cursor() as cursor:
                    cursor.execute(query, params)
                    self.logger.add.debug("Create Cache: {}".format(self.cache_hash))
                    self.__result = cursor

        return self

    def fetch(self, fetch_type: str = 'fetchall'):
        if isinstance(self.__result, self.__mysql.cursorclass):
            fetch_type_method = getattr(self.__result, fetch_type)
            data = fetch_type_method()
            if self.redis:
                self.redis.set(self.cache_hash, _pickle.dumps(data))
                self.redis.expire(self.cache_hash, int(os.getenv('REDISTTL', self.ttl)))
            return data
        else:
            return self.__result

    def fetchone(self):
        return self.fetch('fetchone')

    def fetchall(self):
        return self.fetch('fetchall')

    def commit(self):
        self.mysql.commit()

    def make_hash(self, query, params):
        query_hash = hash(query)
        params_hash = hash(frozenset(params)) if params else '-0'
        self.cache_hash = str(query_hash) + str(params_hash)

    # Static method for standalone query's to DB
    @staticmethod
    def make_query(query: str, params: tuple = None):
        db = Db()
        _res = db.query(query, params).fetchall()
        return _res

    @property
    def redis(self):
        return self.__redis

    @property
    def mysql(self):
        return self.__mysql

    @property
    def cache_hash(self):
        return self.__cache_hash

    @cache_hash.setter
    def cache_hash(self, value):
        self.__cache_hash = value
