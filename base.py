# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/3/18 2:41 PM
@contact: welovewxy@126.com
@file: base.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import libs
import tornado
import tornado.web
import functools
import uuid
import random
import ujson
import logging
import collections
from utils.generations import GenerateId

logging.basicConfig(filename='base.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

global card_to_number_dict_a, card_to_number_dict_b
card_to_number_dict_a = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
card_to_number_dict_b = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.Session = libs.session.Session(self.application.Session_manager, self)
        self.online_user_list = collections.deque()
        self.step = ''

    @staticmethod
    def calc_card_total_number(hand_cards):
        hand_cards_number_a = [card_to_number_dict_a[hand_card] for hand_card in hand_cards]
        hand_cards_total_count_a = functools.reduce(lambda x, y: x + y, hand_cards_number_a)
        if hand_cards_total_count_a > 21:
            hand_cards_number_b = [card_to_number_dict_b[hand_card] for hand_card in hand_cards]
            hand_cards_total_count_b = functools.reduce(lambda x, y: x + y, hand_cards_number_b)
            hand_cards_total_count = hand_cards_total_count_b
        elif 0 < hand_cards_total_count_a < 22:
            hand_cards_total_count = hand_cards_total_count_a
        # is_blackjack = BaseHandler.check_balckjack(hand_cards_total_count)
        # hand_cards_info = dict(hand_cards_total_count=hand_cards_total_count, is_blackjack=is_blackjack)
        return hand_cards_total_count

    @staticmethod
    def check_balckjack(hand_cards_total_count):
        if hand_cards_total_count == 21:
            return True
        else:
            return False

    @staticmethod
    def init_cards():
        try:
            dealer_name = BaseHandler.online_user_list.popleft()
        except Exception as e:
            dealer_name = str(uuid.uuid4())

        dealer_session_id = GenerateId().generate_session_id2(dealer_name)
        dealer_cards = []
        player_cards = []
        card_table_name = 'card_table_name_' + str(uuid.uuid4())
        card_table_name = str(uuid.uuid4())
        # card_table_name = 'card_table_name'
        cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        random.shuffle(cards)
        logging.info('BaseHandler: Generate Card Table Name: {0}, cards info: {1}'.format(card_table_name, cards))
        dealer_cards.append(cards.pop())
        dealer_cards.append(cards.pop())
        player_cards.append(cards.pop())
        player_cards.append(cards.pop())
        logging.info('BaseHandler: Init dealer_cards: {0}, player_cards: {1}. Left cards: {2}'.format(dealer_cards, player_cards, cards))

        dealer_cards_total_count = BaseHandler.calc_card_total_number(dealer_cards)
        player_cards_total_count = BaseHandler.calc_card_total_number(player_cards)

        dealer_is_blackjack = BaseHandler.check_balckjack(dealer_cards_total_count)
        player_is_blackjack = BaseHandler.check_balckjack(player_cards_total_count)

        player_info = dict(
            player_cards=player_cards,
            player_cards_total_count=player_cards_total_count,
            player_is_blackjack=player_is_blackjack,
        )
        dealer_info = dict(
            dealer_name=dealer_name,
            dealer_cards=dealer_cards,
            dealer_cards_total_count=dealer_cards_total_count,
            dealer_is_blackjack=dealer_is_blackjack,
        )

        init_cards_info = dict(
            card_table_name=card_table_name,
            player_info=player_info,
            dealer_info=dealer_info,
        )

        return init_cards_info