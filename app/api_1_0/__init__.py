# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:06
@desc:
"""


from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import mocker