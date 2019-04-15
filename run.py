# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:14
@desc:
"""

from app import create_app, socketio


if __name__ == '__main__':
    app = create_app()
    socketio.run(app, '0.0.0.0', debug=True)