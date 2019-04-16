# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 11:26
@desc:
"""
import time

from app.client.mock_client import Mock_Client
from app.client.mock_tools import params, param
from app.core.mocker.mocker import MockRequest, Mocker, MockResponse
from app.logger import Logger

logger = Logger().getLogger(__name__)



def create_mocker():

    client = Mock_Client("192.168.1.182", 5000)
    mocker_request = MockRequest().with_path("/abc").with_body(params(param("O01-9", "aaa"))).with_method("post")
    mocker_response = MockResponse().with_body("aaaa")
    mocker = Mocker(mocker_request, mocker_response)
    id = client.mock(mocker)
    logger.info("create mock id: " + id)


def get_resp_by_req(req):
    return req['path']

def create_client_callback():
    client = Mock_Client("192.168.1.182", 5000)
    mocker_request = MockRequest().with_path("/abc").with_body(params(param("O01-9", "aaa"))).with_method("post")
    mocker_response = MockResponse().with_callback(get_resp_by_req)
    mocker = Mocker(mocker_request, mocker_response)
    client.mock_callback(mocker)
    # import time
    # time.sleep(10)
    # client.disconect()

def create_mock2():
    client = Mock_Client("192.168.1.182", 5000)
    mocker_request = MockRequest().with_path("/123")
    mocker_response = MockResponse().with_body("aaaa")
    mocker = Mocker(mocker_request, mocker_response)
    client.mock(mocker)

def del_mocker():
    client = Mock_Client("192.168.1.182", 5000)
    client.delete("6fdac8d3807be50a8740d145cc907711")


def clean():
    client = Mock_Client("192.168.1.182", 5000)
    client.restore()

if __name__ == '__main__':
    create_mock2()
    create_client_callback()
    time.sleep(10)
    print("清理mock")
    clean()