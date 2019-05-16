# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 15:07
@desc:
"""


import logging


class Logger:

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def getLogger(self, name=__name__):

        return logging.getLogger(name)

