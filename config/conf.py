# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/6/18 1:40 PM
@contact: welovewxy@126.com
@file: conf.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import logging

logging.basicConfig(filename='conf.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)


server_port = 9999

user_secret = 'Y0JXsEFkrhQ35a8SJYtcQv6HLXYnmRpoxyAoV8G1n2SGoTa6xK37AsvaiUdN9awM8Q'
session_secret = 'wD8UOyYcDbcbbDWHb9wsqfmCXDkZmZBzCFQjJZmtTRomRYFp2XN&ibo127Hygig'
session_secret2 = 'QX369Yvq6A6gx8ywKxrbA70DdmHOKnlWV1CHIyu'
desk_secret = 'qRA178I50q4hz8XXdJthyrdewCQ864MhbB0lRm3nxcRIDC2vwbrm8DkZmZbcbbDWH'
hmac_secret = 'QLhAFScLPZIT3Q55QJKPgbAs6p85goBW3uk8NxfX2DfYh3PS9LJ07kmD1Qu6aEReVX'
cookie_secret = 'FfxcDYNpMMkpYvLgSiqiiV00PGYYXGYcnxOfPhKzBVUilj14xRNAW'
temp_secret = '2wjHv1VeDDc9LaYC0mn5ksCyRy5d8i9cH8W1zF3N5di3N5di'
table_secret = '6HLXYnmXdJthyrdewCQ864MhbB0lRmDYNpMMkpYvLg'

redis_options = {
    'redis_host': '192.168.174.143',
    'redis_port': 6379,
    'redis_password': '',
    'redis_db': 0,
    'redis_timeout': 3600,
}
