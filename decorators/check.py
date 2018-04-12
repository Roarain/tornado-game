# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/9/18 12:25 AM
@contact: welovewxy@126.com
@file: login.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import functools
from utils.wredis import RedisPool
from utils.generations import GenerateId
import logging

logging.basicConfig(filename='login.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


def check_temp_id_session_id_from_cookie_id(cookie_id, temp_id):
    check_temp_id = GenerateId().generate_temp_id(cookie_id)
    check_session_id = GenerateId().generate_session_id(cookie_id)
    if temp_id == check_temp_id and RedisPool().exists(check_session_id):
        return True
    else:
        return False


def check_cookie_id(function):
    @functools.wraps(function)
    def _wrapper(self, *args, **kwargs):
        cookie_id = self.get_secure_cookie('cookie_id')
        if not cookie_id:
            self.redirect('/')
            return
        cookie_id = cookie_id.decode()
        session_id = GenerateId().generate_session_id(cookie_id)
        if not RedisPool().exists(session_id):
            logging.info('check_cookie_id wrapper: cookie_id found but session_id lost, redirect to / to init...')
            self.redirect('/')
            return
        return function(self, *args, **kwargs)

    return _wrapper


def check_login(function):
    @functools.wraps(function)
    def _wrapper(self, *args, **kwargs):
        cookie_id = self.get_secure_cookie('cookie_id')
        if not cookie_id:
            self.redirect('/')
            return
        session_id = GenerateId().generate_session_id(cookie_id.decode())

        if not RedisPool().hget(session_id, 'user_id'):
            logging.info('check_login wrapper: redirect to /login to login...')
            self.redirect('/login')

        return function(self, *args, **kwargs)
    return _wrapper


'''
def check_temp_id_session_id_from_cookie_id(function):
    @functools.wraps(function)
    def _wrapper(self, cookie_id, temp_id):
        check_temp_id = GenerateId().generate_temp_id(cookie_id)
        check_session_id = GenerateId().generate_session_id(cookie_id)
        if temp_id == check_temp_id and RedisPool().exists(check_session_id):
            return function(self, cookie_id, temp_id)
        else:
            self.redirect('/login')
            logging.info('check_temp_id_session_id_from_cookie_id wrapper faild: redirect to /login to login...')
            return
    return _wrapper
'''

'''
def check_user_session_id(function):
    @functools.wraps(function)
    def _wrapper(self, *args, **kwargs):
        user_session_id = self.get_argument('user_session_id', '')

        if not user_session_id:
            result_dict = dict(
                status='Failure',
                reason='None user_session_id',
            )
            self.write(result_dict)
            return

        if not RedisPool().exists(user_session_id):
            result_dict = dict(
                status='Failure',
                reason='Illegal user_session_id!',
            )
            self.write(result_dict)
            return

        return function(self, *args, **kwargs)
    return _wrapper
'''

'''
def check_login(function):
    @functools.wraps(function)
    def _wrapper(self, *args, **kwargs):
        cookie_id = self.get_secure_cookie('cookie_id')
        if not cookie_id:
            self.redirect('/')
            return
        session_id = GenerateId().generate_session_id(cookie_id.decode())

        if not RedisPool().hget(session_id, 'user_id'):
            logging.info('check_login wrapper: redirect to /login to login...')
            self.redirect('/login')

        self.Session['session_id'] = session_id

        return function(self, *args, **kwargs)
    return _wrapper
'''