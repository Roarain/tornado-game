# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/6/18 2:26 PM
@contact: welovewxy@126.com
@file: test.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging
import redis
from utils.wredis import RedisPool

logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

'''
# redispool = RedisPool()

# RedisPool().setex('key1', 'value1')
# RedisPool().setex('key2', 'value2')
# RedisPool().setex('key3', 'value3')

class A(object):
    def setA(self):
        RedisPool().setex('key1', 'value1')

class B(A):
    def setB(self):
        RedisPool().setex('key1', 'value1')

class C(B):
    def setC(self):
        RedisPool().setex('key1', 'value1')

a = A()
a.setA()
b = B()
b.setB()
c = C()
c.setC()


'''

class A(object):
    def __init__(self):
        self.a = 'a'
        self.b = 'b'
        self.c = 'c'


result = [i for i in dir(A()) if not i.startswith('__')]
print(result)