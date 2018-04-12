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

card_to_number_dict = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


def check_temp_id_session_id_from_cookie_id(cookie_id, temp_id):
    """
    根据get_secure_cookie获取到的cookie_id和temp_id来生成session_id，校验cookie_id和temp_id是否与重新生成的一致，校验session_id是否存在redis中（有效性）。
    :param cookie_id:str
    :param temp_id: str
    :return: True/False
    """
    check_temp_id = GenerateId().generate_temp_id(cookie_id)
    check_session_id = GenerateId().generate_session_id(cookie_id)
    if temp_id == check_temp_id and RedisPool().exists(check_session_id):
        return True
    else:
        return False


def check_cookie_id(function):
    """
    确认在登录前有cookie_id，也就是一定要初始化self.Session，只有这样，才能对cookie_id和temp_id执行set_secure_cookie，将session_id存入redis
    :param function:
    :return:
    """
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
    """
    LoginHandler将user_name,user_password，根据user_name生成的user_id等信息以user_name为键，存入redis，同时也将user_id存入session_id中，也使用set_secure_cookie设置了user_id。同时也校验了登陆与首页刷新时间过长，session_id过期删除
    :param function:
    :return:
    """
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
            return

        return function(self, *args, **kwargs)
    return _wrapper


def calc_card_total_number(hand_cards):
    countA = hand_cards.count('A')
    cards = [hand_card for hand_card in hand_cards if not hand_card == 'A']
    chc = sum([card_to_number_dict[card] for card in cards])
    if countA:
        A_count = 11 * 1 + (countA - 1) * 1
        if chc + A_count > 21:
            A_count = countA * 1
    else:
        A_count = 0
    result = chc + A_count
    return result


def get_hand_cards_total_cout_status(hand_cards):
    """

    :param hand_cards:
    :return:tuple hand_cards_total_count, hand_cards_status
    """
    countA = hand_cards.count('A')
    cards = [hand_card for hand_card in hand_cards if not hand_card == 'A']
    chc = sum([card_to_number_dict[card] for card in cards])
    if countA:
        A_count = 11 * 1 + (countA - 1) * 1
        if chc + A_count > 21:
            A_count = countA * 1
    else:
        A_count = 0
    hand_cards_total_count = chc + A_count

    if hand_cards_total_count > 21:
        hand_cards_status = 'BOOM'
    elif hand_cards_total_count == 21:
        hand_cards_status = 'BLACKJACK'
    elif 0 < hand_cards_total_count < 21:
        hand_cards_status = 'NORMAL'
    else:
        hand_cards_status = 'Unknown'

    return hand_cards_total_count, hand_cards_status


def calc_match_result(session):
    step = session['step']
    player_cards_status = session['player_cards_status']
    if step == 'STARTGAME':
        if player_cards_status == 'BLACKJACK':
            result = tuple(('WIN', 'BLACKJACK'))

    if player_cards_status == 'BOOM':
        result = tuple(('LOSE', 'BOOM'))

    dealer_cards_status = session['dealer_cards_status']
    if player_cards_status == 'BLACKJACK':
        if dealer_cards_status == 'BLACKJACK':
            result = tuple(('PUSH', 'ALL_BLACKJACK'))
        else:
            result = tuple(('WIN', 'BLACKJACK'))

    if dealer_cards_status == 'BLACKJACK':
        result = tuple(('LOSE', 'DEALER_BLACKJACK'))

    player_cards_total_count = int(session['player_cards_total_count'])
    dealer_cards_total_count = int(session['dealer_cards_total_count'])

    if player_cards_status == dealer_cards_status == 'NORMAL':
        if player_cards_total_count > dealer_cards_total_count:
            result = tuple(('WIN', 'BIGGER'))
        elif player_cards_total_count == dealer_cards_total_count:
            result = tuple(('PUSH', 'EQUAL'))
        elif player_cards_total_count < dealer_cards_total_count:
            result = tuple(('LOSE', 'SMALLER'))
    return result
