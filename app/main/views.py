# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/9/009 14:16
@desc:
"""

from flask import request

from app.core.mocker import all_mocker
from app.core.mocker.mocker import choose_mocker, get_resp_from_request
from app.main import main


@main.route("/<url>", methods=["GET", "POST"])
def mock_result(url):
    mocker = choose_mocker(request, all_mocker)
    if mocker and mocker.mockresponse.contain_callback:
        get_resp_from_request(request, mocker)

    return mocker.mockresponse.body if mocker else "xxxxx"

@main.route("/", methods=["GET", "POST"])
def index():
    return "hello"










