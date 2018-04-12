# -*- coding: utf-8 -*-

"""
@purpose: 
@version: 1.0
@author: Roarain
@time: 4/11/18 5:03 PM
@contact: welovewxy@126.com
@file: calc.py
@license: Apache Licence
@site: 
@software: PyCharm
"""

import functools
import logging

logging.basicConfig(filename='calc.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.DEBUG)

card_to_number_dict = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}


hand_cards = ['2', '8']


def calc(hand_cards):
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

result = calc(hand_cards)
print(result)



