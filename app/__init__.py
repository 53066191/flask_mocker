# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:06
@desc:
"""


from flask import Flask
from flask_socketio import SocketIO
from werkzeug.routing import BaseConverter

socketio = SocketIO()


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex=items[0]


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter

    app.config['SECRET_KEY'] = 'secret!'

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint)

    socketio.init_app(app)

    return app