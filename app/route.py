# encoding: utf-8
"""
@author: liuyun
@time: 2019/5/10/010 17:15
@desc:
"""

import os
from flask import make_response
import requests
from flask import Response

from app.tools.Properties import parse
from contextlib import closing

def get_config():

    cur_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cur_path, '..', 'route.ini')


class Proxy():

    def __init__(self, uri, from_ip_port):
        route_file = get_config()
        f = parse(route_file)

        self.from_ip_port = from_ip_port
        self.uri = uri
        self.to_ip_port = f.get_by_api(self.uri, self.from_ip_port)
        self.default = f.get_default(self.from_ip_port)


    def redirect(self, url, request):
        method = request.method
        data = request.data or request.form or None
        headers = dict()

        for name, value in request.headers:
            if not value or name == 'Cache-Control':
                continue
            headers[name] = value

        with closing(
                requests.request(method, url, headers=headers, data=data, stream=True)
        ) as r:
            resp_headers = []
            for name, value in r.headers.items():
                if name.lower() in ('content-length', 'connection',
                                    'content-encoding'):
                    continue
                resp_headers.append((name, value))
            result = Response(r, status=r.status_code, headers=resp_headers)
            print(result.data)
            return result




