# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/10/18 2:18 PM
@contact: welovewxy@126.com
@file: redistest.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging

logging.basicConfig(filename='redistest.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


import redis
class RedisDBConfig:
  HOST = '127.0.0.1'
  PORT = 6379
  DBID = 0
def operator_status(func):
  '''''get operatoration status
  '''
  def gen_status(*args, **kwargs):
    error, result = None, None
    try:
      result = func(*args, **kwargs)
    except Exception as e:
      error = str(e)
    return {'result': result, 'error': error}
  return gen_status
class RedisCache(object):
  def __init__(self):
    if not hasattr(RedisCache, 'pool'):
      RedisCache.create_pool()
    self._connection = redis.Redis(connection_pool = RedisCache.pool)
  @staticmethod
  def create_pool():
    RedisCache.pool = redis.ConnectionPool(
        host = RedisDBConfig.HOST,
        port = RedisDBConfig.PORT,
        db  = RedisDBConfig.DBID)
  @operator_status
  def set_data(self, key, value):
    '''''set data with (key, value)
    '''
    return self._connection.set(key, value)
  @operator_status
  def get_data(self, key):
    '''''get data by key
    '''
    return self._connection.get(key)
  @operator_status
  def del_data(self, key):
    '''''delete cache by key
    '''
    return self._connection.delete(key)
if __name__ == '__main__':
    rc = RedisCache()
    print(RedisCache().set_data('Testkey', "Simple Test"))
    print(RedisCache().get_data('Testkey'))
    print(RedisCache().del_data('Testkey'))
    print(RedisCache().get_data('Testkey'))