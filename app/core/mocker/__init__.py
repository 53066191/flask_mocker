# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 11:59
@desc:
"""

all_mocker = {}

def get_all_mocker():
    return all_mocker

def add_mocker(id, mocker):
    all_mocker[id] = mocker

def del_mocker(id):
    del all_mocker[id]

def clean_mocker():
    global all_mocker
    all_mocker = {}


