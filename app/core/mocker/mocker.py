# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/8/008 17:36
@desc:
"""
import hashlib
import time

import jsonpickle
from flask_socketio import emit

from app.core.mocker import all_mocker


class MockRequest:

    def __init__(self):
        self.path = ""
        self.method = ""
        self.body = ""

    def with_path(self, path):
        self.path = path
        return self

    def with_method(self, method):
        self.method = method
        return self

    def with_body(self, body):
        self.body = body
        return self

class MockResponse:

    def __init__(self):
        self.actual_req = None
        self.contain_callback = False

    def with_body(self, value):
        self.body = value
        return self

    def with_callback(self, func):
        self.contain_callback = True
        self.callback = func
        return self



class Mocker():

    def __init__(self, mockrequest:MockRequest, mockresponse:MockResponse):

        self.mockrequest = mockrequest
        self.mockresponse = mockresponse
        self.receive_request = None

    def set_id(self):
        m = hashlib.md5()
        s = '_'.join([str(self.mockrequest.method), str(self.mockrequest.path), str(self.mockrequest.body)])
        m.update(s.encode("utf8"))
        self.id = m.hexdigest()

    def register(self):
        self.set_id()
        all_mocker[self.id] = self


def choose_mocker(request):
    from app.core.matchers.matcher import Matcher

    for id in all_mocker:
        matcher = Matcher(request, all_mocker[id])
        if matcher.match():
            return all_mocker[id]

    return None


def del_mocker(id):
    del all_mocker[id]


def get_resp_from_request(request, mocker):
        data = {
                'path': request.path,
                'json': request.json,
                'data': request.data.decode(encoding='utf-8'),
                'header': request.content_type,
                'id': mocker.id
                }
        emit("app_request", jsonpickle.encode(data), room=mocker.id, namespace="/mock")

        while True:
            print("%s 等待結果返回" % (mocker.id))
            if hasattr(mocker.mockresponse, "body"):
                return mocker.mockresponse.body
            time.sleep(1)