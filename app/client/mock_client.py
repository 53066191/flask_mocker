# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:58
@desc:
"""
import ctypes
import inspect
import threading
import jsonpickle
import requests

from app.client import all_connection
from app.core.mocker.mocker import Mocker
from socketIO_client import SocketIO, BaseNamespace


class Mock_Client():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.t = None

    def mock(self, mocker: Mocker):
        url = "http://%s:%s/mock/create" % (self.ip, self.port)
        headers = {"content-type": "application/json"}
        resp = requests.post(url, headers=headers, data=jsonpickle.encode(mocker))
        if resp.json()['code'] == 0:
            return resp.json()['id']
        else:
            print("创建失败")


    def mock_callback(self, mocker):
        self.t = threading.Thread(target=run, args=(self.ip, self.port, mocker))
        all_connection.append(self.t)
        self.t.start()

    def delete(self, id):
        parmas = {"id":id}
        url = "http://%s:%s/mock/delete" % (self.ip, self.port)

        resp = requests.get(url, params=parmas)
        if resp.json()['code'] == 0:
            print("删除完成")
        else:
            print("删除失败")

        if self.t:
            stop_thread(self.t)

    def restore(self):

        '''清理所有的socketio链接，以及mocker对象'''

        for conn in all_connection:
            stop_thread(conn)
        url = "http://%s:%s/mock/clean" % (self.ip, self.port)
        resp = requests.get(url)
        if resp.json()['code'] == 0:
            print("清理完成")
        else:
            print("清理失败")


    def disconect(self):
        stop_thread(self.t)


class Namespace(BaseNamespace):

    #接收服务端收到的请求
    def on_app_request(self,  r):
        r = jsonpickle.decode(r)
        print("收到app request %s" % r)
        body = self.call_back(r)
        self.emit("client_result", {'id':r['id'], 'body':body})

    def on_mocker_id(self, cid):
        print("服务端已连接，客户端id:", cid)

    def callback(self, func):
        self.call_back = func


def run(ip, port, mocker):
    try:
        socketIO = SocketIO(ip, port, wait_for_connection=False)
        mocknamespace = socketIO.define(Namespace, '/mock')
        mocknamespace.callback(mocker.mockresponse.callback)
        mocknamespace.emit('join', jsonpickle.encode(mocker))
        socketIO.wait()
    except ConnectionError:
        print('The server is down. Try again later.')


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


def stop_thread(t):
    _async_raise(t.ident, SystemExit)
