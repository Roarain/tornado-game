# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/3/18 2:43 PM
@contact: welovewxy@126.com
@file: session.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import uuid
import hmac
from utils.wredis import RedisPool
from utils.generations import GenerateId
import json
import logging

logging.basicConfig(filename='session.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

class SessionData(dict):
    def __init__(self, cookie_id, temp_id):
        self.cookie_id = cookie_id
        self.temp_id = temp_id
        self.session_id =  GenerateId().generate_session_id(self.cookie_id)

        self['cookie_id'] = cookie_id
        self['temp_id'] = temp_id
        self['session_id'] = self.session_id


class Session(SessionData):
    def __init__(self, session_manager, request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler
        try:
            session = self.session_manager.get(request_handler)
        except Exception as e:
            session = self.session_manager.get()

        for key, value in session.items():
            self[key] = value

        self.cookie_id = session.cookie_id
        self.temp_id = session.temp_id

    def save(self):
        try:
            cookie_id = self.request_handler.get_secure_cookie("cookie_id").decode()
            temp_id = self.request_handler.get_secure_cookie("temp_id").decode()
            session_id = GenerateId().generate_session_id(cookie_id)
            if RedisPool().exists(session_id):
                RedisPool().expire(session_id)
            else:
                self.session_manager.set(self.request_handler, self)
        except:
            self.session_manager.set(self.request_handler, self)


class SessionManager(object):
    def _fetch(self, cookie_id):
        session_id = GenerateId().generate_session_id(cookie_id)
        if RedisPool().exists(session_id):
            session_data = RedisPool().hgetall(session_id)
            if session_data and isinstance(session_data, dict):
                return session_data
            else:
                return {}
        else:
            return {}

    def get(self, request_handler=None):
        if request_handler:
            try:
                cookie_id = request_handler.get_secure_cookie("cookie_id").decode()
                temp_id = request_handler.get_secure_cookie("temp_id").decode()
            except Exception as e:
                logging.info('cookie_id or temp_id not in request_handler: {0}'.format(request_handler))
        else:
            cookie_id = None
            temp_id = None

        if not cookie_id:
            session_exists = False
            cookie_id = GenerateId().generate_cookie_id()
            temp_id = GenerateId().generate_temp_id(cookie_id)
        elif cookie_id:
            session_exists = True

        check_temp_id = GenerateId().generate_temp_id(cookie_id)
        if check_temp_id == temp_id:
            session = SessionData(cookie_id, temp_id)
        else:
            raise InvalidSessionException()

        if session_exists:
            session_data = self._fetch(cookie_id)
            for key, value in session_data.items():
                session[key] = value

        return session

    def set(self, request_handler, session):
        request_handler.set_secure_cookie("cookie_id", session.cookie_id)
        request_handler.set_secure_cookie("temp_id", session.temp_id)

        session.session_id = session['session_id'] = GenerateId().generate_session_id(session.cookie_id)

        RedisPool().hmset(session.session_id, session)

class InvalidSessionException(Exception):
    pass