# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 13:34
@desc:
"""
import re

from app.core.mocker.mocker import Mocker
from app.core.matchers.matchlog import log


def matched_from_type(actual, expect):

    if isinstance(expect, re.Pattern):
        regex = re.compile(expect)
        return regex.match(actual)
    else:
        return expect.lower() == actual.lower()


def is_dict_value_matched(actual_dict, expect_dict):

    for key in expect_dict:
        if key in actual_dict:
            if not matched_from_type(actual_dict[key], expect_dict[key]):
                return False

        # 实际请求中没有期望的key，则直接false
        else:
            return False

    return True


class Matcher:

    def __init__(self, request, mocker:Mocker):
        self.mocker = mocker
        self.request = request

    def match_method(self):
        if not self.mocker.mockrequest.method:
            log(True, "method")
            return True
        elif self.mocker.mockrequest.method.upper() == self.request.method:
            log(True, "method")
            return True
        else:
            log(False, "method")
            return False

    def match_path(self):
        sucess = matched_from_type(self.request.path, self.mocker.mockrequest.path)
        log(sucess, "path")
        return sucess

    def _match_body_str(self):
        return matched_from_type(self.request.data.decode(encoding='utf-8'), self.mocker.mockrequest.body)


    def _match_body_params(self):

        if not self.request.json:
            return False
        return is_dict_value_matched(self.request.json, self.mocker.mockrequest.body)

    def match_body(self):
        if isinstance(self.mocker.mockrequest.body, dict):
            sucess = self._match_body_params()
            log(sucess, "body")
            return sucess

        elif isinstance(self.mocker.mockrequest.body, str):
            sucess = self._match_body_str()
            log(sucess, "body")
            return sucess

        else:
            sucess=True
            log(sucess, "body")
            return True

    def match(self):
        return self.match_method() and self.match_path() and self.match_body()






