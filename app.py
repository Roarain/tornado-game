# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/3/18 2:41 PM
@contact: welovewxy@126.com
@file: app.py
@license: Apache Licence
@site:
@software: PyCharm
"""

import tornado
import tornado.web
import tornado.gen
import tornado.options
from tornado.options import define, options
import tornado.concurrent
import os
# from libs import session
import libs.session
# import base
from utils.generations import GenerateId
from utils.wredis import RedisPool
from config import conf
from decorators.check import check_cookie_id, check_login, check_temp_id_session_id_from_cookie_id
import functools
import uuid
import random
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

# global card_to_number_dict_a, card_to_number_dict_b

card_to_number_dict = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


define('port', default=9999, help='run on the given port', type=int)

tornado.options.parse_command_line()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/startgame", StartGameHandler),
            (r"/getcard", GetCardHandler),
        ]
        settings = dict(
            cookie_secret=conf.cookie_secret,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
        )
        self.Session_manager = libs.session.SessionManager()
        super(Application, self).__init__(handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.Session = libs.session.Session(self.application.Session_manager, self)
        self.online_user_list = []
        self.step = ''

    '''
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
        return hand_cards_total_count
        '''

    @staticmethod
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

        dealer_id = GenerateId().generate_user_id(dealer_name)
        dealer_cards = []
        player_cards = []
        desk_id = GenerateId().generate_desk_id()
        cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        random.shuffle(cards)
        logging.info('BaseHandler: Generate desk_id: {0}, cards info: {1}'.format(desk_id, cards))
        dealer_cards.append(cards.pop())
        dealer_cards.append(cards.pop())
        player_cards.append(cards.pop())
        player_cards.append(cards.pop())
        logging.info(
            'BaseHandler: Init dealer_cards: {0}, player_cards: {1}. Left cards: {2}'.format(dealer_cards, player_cards,
                                                                                             cards))

        dealer_cards_total_count = BaseHandler.calc_card_total_number(dealer_cards)
        player_cards_total_count = BaseHandler.calc_card_total_number(player_cards)

        dealer_is_blackjack = BaseHandler.check_balckjack(dealer_cards_total_count)
        player_is_blackjack = BaseHandler.check_balckjack(player_cards_total_count)

        '''
        player_info = dict(
            player_cards=player_cards,
            player_cards_total_count=player_cards_total_count,
            player_is_blackjack=player_is_blackjack,
        )
        dealer_info = dict(
            dealer_id=dealer_id,
            dealer_cards=dealer_cards,
            dealer_cards_total_count=dealer_cards_total_count,
            dealer_is_blackjack=dealer_is_blackjack,
        )


        init_cards_info = dict(
            desk_id=desk_id,
            player_info=player_info,
            dealer_info=dealer_info,
        )
        '''

        init_cards_info = dict(
            desk_id=desk_id,
            player_cards=player_cards,
            player_cards_total_count=player_cards_total_count,
            player_is_blackjack=player_is_blackjack,
            dealer_id=dealer_id,
            dealer_cards=dealer_cards,
            dealer_cards_total_count=dealer_cards_total_count,
            dealer_is_blackjack=dealer_is_blackjack,
            left_cards=cards,
        )

        return init_cards_info


class MainHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        return (yield self.main())

    @tornado.gen.coroutine
    def post(self):
        return (yield self.main())

    def main(self):
        if not self.get_secure_cookie('cookie_id'):
            self.Session.save()
        self.Session.save()
        logging.info('CurrentSession: {0}'.format(self.Session))

        logging.info('Init MainHandler success, Redirect to /login ...')
        self.render('index.html')


class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render('login.html')

    @tornado.gen.coroutine
    def post(self):
        return (yield self.login())

    @check_cookie_id
    def login(self):
        user_name = self.get_argument('user_name', '')
        user_password = self.get_argument('user_password', '')

        if user_name and user_password and user_name == user_password:
            if not RedisPool().exists(user_name):
                RedisPool().insert_user_name(user_name, user_password)

            user_id = GenerateId().generate_user_id(user_name)
            self.set_secure_cookie('user_id', user_id)

            cookie_id = self.get_secure_cookie('cookie_id').decode()
            temp_id = self.get_secure_cookie('temp_id').decode()

            if check_temp_id_session_id_from_cookie_id(cookie_id, temp_id):
                self.Session['user_name'] = user_name
                self.Session['user_password'] = user_password
                self.Session['user_id'] = user_id

            print('LoginHandler: ', self.Session)
            RedisPool().hmset(self.Session['session_id'], self.Session)

            self.redirect('/startgame')
        else:
            logging.info('user_name or user_password is invalid, redirect to /login...')
            self.render('login.html')


class StartGameHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        return (yield self.startgame())

    # @tornado.gen.coroutine
    # def post(self):
    #     return (yield self.startgame())

    @check_login
    def startgame(self):
        cookie_id = self.get_secure_cookie('cookie_id').decode()
        temp_id = self.get_secure_cookie('temp_id').decode()
        user_id = self.get_secure_cookie('user_id').decode()

        if check_temp_id_session_id_from_cookie_id(cookie_id, temp_id):
            cards_info = BaseHandler.init_cards()
            cards_info['player_id'] = user_id
            self.step = 'STARTGAME'
            self.Session['step'] = self.step

            session_id = GenerateId().generate_session_id(cookie_id)
            print('StartGameHandler: ', session_id)
            print('StartGameHandler: ', type(session_id))
            RedisPool().hmset(session_id, dict(step=self.step))

            for key, value in cards_info.items():
                self.Session[key] = value
                RedisPool().hmset(session_id, {key: value})
            current_session = self.Session

            print('StartGameHandler: ', current_session)
            print('StartGameHandler: ', type(current_session))
            print('StartGameHandler: ', RedisPool().hgetall(session_id))


        self.render('startgame.html', current_session=current_session, **current_session)


class GetCardHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        return (yield self.getcard())

    @tornado.gen.coroutine
    def get(self):
        return (yield self.getcard())

    @check_login
    def getcard(self):
        print('GetCardHandler: ', self.Session)
        print('GetCardHandler: ', type(self.Session))

        cookie_id = self.get_secure_cookie('cookie_id').decode()
        temp_id = self.get_secure_cookie('temp_id').decode()

        if check_temp_id_session_id_from_cookie_id(cookie_id, temp_id):
            session_id = self.Session['session_id']

            player_cards = eval(self.Session['player_cards'])
            left_cards = eval(self.Session['left_cards'])

            print(type(player_cards))
            print('player_cards: ', player_cards)
            player_cards.append(left_cards.pop())

            player_cards_total_count = BaseHandler.calc_card_total_number(player_cards)
            player_is_blackjack = BaseHandler.check_balckjack(player_cards_total_count)

            self.step = 'GETCARD'

            changes_dict = dict(
                player_cards=player_cards,
                player_cards_total_count=player_cards_total_count,
                player_is_blackjack=player_is_blackjack,
                left_cards=left_cards,
                step=self.step,
            )

            for key, value in changes_dict.items():
                self.Session[key] = value
                RedisPool().hmset(session_id, {key: value})

            current_session = self.Session

            self.render('startgame.html',current_session=current_session, **current_session)









def main():
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()