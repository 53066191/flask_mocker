# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:10
@desc:
"""
import jsonpickle
from flask import request, jsonify
from . import api
from app.core.mocker import all_mocker



@api.route("/mock/create", methods=["POST"])
def create_mock():
    mocker = jsonpickle.decode(request.data)
    mocker.register()
    result = {"code": 0, "id": mocker.id}
    return jsonify(result)



@api.route("/mock/delete", methods=["GET"])
def del_mock():
    id = request.args.get("id")
    if id in all_mocker:
        del all_mocker[id]
    result = {"code": 0, "msg": "sucess"}
    return jsonify(result)

