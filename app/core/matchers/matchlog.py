# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 15:17
@desc:
"""

from app.tools.logger import Logger

logger = Logger().getLogger(__name__)

def log(sucess, type):
    end = "sucess" if sucess else "failed"
    logger.info("{type} match {end}".format(type=type, end=end))
