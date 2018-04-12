# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/3/18 3:11 PM
@contact: welovewxy@126.com
@file: generations.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging
import uuid
import hmac
import hashlib
from config import conf

logging.basicConfig(filename='generations.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


class GenerateId(object):

    def generate_desk_id(self):
        desk_id = hashlib.sha256(('desk_name_' + conf.desk_secret + str(uuid.uuid4())).encode()).hexdigest()
        return desk_id

    def generate_cookie_id(self):
        cookie_id = hashlib.sha256(('cookie_id_' + conf.cookie_secret + str(uuid.uuid4())).encode()).hexdigest()
        return cookie_id

    def generate_temp_id(self, cookie_id):
        temp_id = self.generate_id(cookie_id, conf.temp_secret)
        return temp_id

    def generate_session_id(self, cookie_id):
        session_id = self.generate_id(cookie_id, conf.session_secret)
        return session_id

    def generate_id(self, original_character, salt):
        result = hmac.new(bytes(original_character, 'utf-8'), bytes(salt, 'utf-8'), hashlib.sha256).hexdigest()
        return result

    def generate_user_id(self, user_name):
        user_id = self.generate_id(user_name, conf.user_secret)
        return user_id

    def generate_hmac_id(self, session_id):
        hmac_id = self.generate_id(session_id, conf.hmac_secret)
        return hmac_id

    def generate_card_table_id(self, card_table_name):
        card_table_id = self.generate_id(card_table_name, conf.table_secret)
        return card_table_id

