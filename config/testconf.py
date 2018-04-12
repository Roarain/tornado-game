# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/10/18 10:02 PM
@contact: welovewxy@126.com
@file: testconf.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging

logging.basicConfig(filename='testconf.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


options = {
    'host': '127.0.0.1',
    'port': 8888,
    'password': 'abcd1234',
}

