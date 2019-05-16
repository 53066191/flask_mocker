# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/15/015 15:19
@desc:
"""

import jsonpickle
from flask_socketio import emit, join_room
from app import socketio
from app.core.mocker import get_all_mocker


#客戶端连接成功后，加入到room中
@socketio.on("join", namespace='/mock')
def create_mock_callback(message):
    mocker = jsonpickle.decode(message)
    mocker.register()
    join_room(mocker.id)  # 連接加入到id為名的room中
    emit('mocker_id', mocker.id)


#接收客户端生成的返回
@socketio.on("client_result", namespace='/mock')
def receive_client_result(msg):
    all_mocker = get_all_mocker()
    all_mocker[msg['id']].mockresponse.body = msg['body']
