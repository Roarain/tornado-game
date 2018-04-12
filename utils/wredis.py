# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/3/18 2:53 PM
@contact: welovewxy@126.com
@file: wredis.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import redis
from config import conf
from utils.generations import GenerateId
import logging
import json
import ujson

logging.basicConfig(filename='wredis.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


class RedisPool(object):
    def __init__(self):
        if not hasattr(RedisPool, 'redis_pool'):
            RedisPool.redis_pool = self.create_redis_pool()
        if not hasattr(RedisPool, 'redis_timeout'):
            RedisPool.redis_timeout = conf.redis_options['redis_timeout']

    @staticmethod
    def create_redis_pool():
        pool = redis.ConnectionPool(host=conf.redis_options['redis_host'],
                                    port=conf.redis_options['redis_port'],
                                    db=conf.redis_options['redis_db'])
        RedisPool.redis_pool = redis.Redis(connection_pool=pool)
        return RedisPool.redis_pool

    def setex(self, key, value):
        """
        from dict to redis string with timeout
        :param key:
        :param value:
        :return: None
        """
        try:
            self.redis_pool.setex(key, value, self.redis_timeout)
            logging.info('Execute SETEX Success, key: {0}, value: {1}'.format(key, value))
        except Exception as e:
            logging.debug('Execute SETEX Faild, key: {0}, value: {1}'.format(key, value))

    def get(self, key):
        """
        according to key to get string type's value
        :param key:
        :return:value
        """
        try:
            result = self.redis_pool.get(key).decode()
            result = eval(result)
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute GET Success, key: {0}'.format(key))
            return result
        except Exception as e:
            logging.debug('Execute GET Faild, key: {0}'.format(key))
            result = None
        return result

    def hmset(self, key, mapping):
        """
        hash type
        :param key:
        :param mapping:dict
        :return: None
        """
        try:
            self.redis_pool.hmset(key, mapping)
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute HMSET Success, key: {0}, mapping: {1}'.format(key, mapping))
        except Exception as e:
            logging.debug('Execute HMSET Faild, key: {0}, mapping: {1}'.format(key, mapping))

    def hgetall(self, key):
        """
        according to key to get hash type's value
        :param key:
        :return: mapping(dict)
        """
        try:
            bresult = self.redis_pool.hgetall(key)
            result = {key.decode(): value.decode() for (key, value) in bresult.items()}
            self.redis_pool.expire(key, self.redis_timeout)
            logging.info('Execute HGETALL Success, key: {0}'.format(key))
        except Exception as e:
            logging.debug('Execute HGETALL Faild, key: {0}'.format(key))
            result = None
        return result

    def exists(self, key):
        """

        :param key:
        :return:True/False
        4556
        """
        return self.redis_pool.exists(key)

    def hget(self, key, field):
        """
        hash hget key, field
        :param key:
        :param field:
        :return: key-->field-->value
        """
        try:
            result = self.redis_pool.hget(key, field).decode()
            result = eval(result)
        except Exception as e:
            logging.debug('Execute HGET Faild, key: {0}, field: {1}'.format(key, field))
            result = self.redis_pool.hget(key, field)
        return result

    def insert_user_name(self, user_name, user_password, user_gender=None, user_avatar=None):
        """
        check passed user info to redis
        :param user_name:
        :param user_password:
        :param user_gender:
        :param user_avatar:
        :return:
        """
        user_id = GenerateId().generate_user_id(user_name)
        user_dict = dict(
            user_name=user_name,
            user_password=user_password,
            user_id=user_id,
            user_gender=user_gender,
            user_avatar=user_avatar,
        )
        self.redis_pool.hmset(user_name, user_dict)
        self.redis_pool.expire(user_name, self.redis_timeout)

    def insert_session_id(self, user_name):
        user_id = self.hget(user_name, 'user_id')

    def insert_user_session_id(self, user_name):
        user_id = self.hget(user_name, 'user_id')
        user_session_id = GenerateId().generate_session_id2(user_name)
        user_session_id_dict = dict(
            user_session_id=user_session_id,
            user_id=user_id,
        )
        self.redis_pool.hmset(user_session_id, user_session_id_dict)
        self.redis_pool.expire(user_session_id, self.redis_timeout)

    def get_user_session_from_user_name(self, user_name):
        user_session_id = GenerateId().generate_session_id2(user_name)
        user_session = self.hgetall(user_session_id)
        user_session = eval(user_session)
        return user_session

    def bulk_injection_user_name(self):
        pass

    def bulk_injection_user_session_id(self):
        pass

    def expire(self, key):
        self.redis_pool.expire(key, self.redis_timeout)


# '''
if __name__ == '__main__':
    rp = RedisPool()
    '''
    ccc = dict(c1='cc1',
               c2='cc2')
    bbb = dict(b1='bb1',
               b2='bb2',
               b3='bb3',
               c=ccc)
    rp.hmset('bbb', bbb)
    result = rp.hgetall('bbba')
    result = rp.get('k').decode()
    print(type(result))
    print(result)

    rp.bulk_injection_user_name('cat', 'cat', 'male', 'www.cat.com')
    rp.bulk_injection_user_name('dog', 'dog', 'female', 'www.dog.com')
    rp.bulk_injection_user_name('pig', 'pig', 'male', 'www.pig.com')
    rp.bulk_injection_user_name('wolf', 'wolf', 'female', 'www.wolf.com')
    '''
    mapping = {'list1': ['aa', 'bb', 'cc']}
    rp.hmset('list1', mapping)
    jmapping = rp.hget('list1', 'list1')
    print(type(jmapping))
    print(jmapping)

# '''

