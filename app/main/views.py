# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 14:16
@desc:
"""
from flask import request, g, redirect, url_for

from app import route
from app.core.mocker.mocker import choose_mocker, set_resp_body_from_request
from app.main import main



@main.before_request
def proxy():
    g.proxy = route.Proxy(request.path, request.host)
    g.url = "http://" + g.proxy.default + request.path

    if g.proxy.to_ip_port:
        url = "http://" + g.proxy.to_ip_port + request.path
        return g.proxy.redirect(url, request)


@main.route("/<regex('.*'):uri>", methods=["GET", "POST"])
def mock_result(uri):
    mocker = choose_mocker(request)
    if mocker and mocker.mockresponse.contain_callback:
        set_resp_body_from_request(request, mocker)

    return mocker.mockresponse.make_response() if mocker else g.proxy.redirect(g.url, request )


@main.route("/")
def hello():
    return "hello"










