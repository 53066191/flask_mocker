# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 11:48
@desc:
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, socket_io_views