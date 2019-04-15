# flask_mocker
使用客户端控制服务端，生成mock，并根据客户端需要返回


###  客户端支持匹配方式：
    1.regex(): 带上此函数后，将转为正则表达式匹配
    2.parmas(param("O01-9", "aaa")), body中含有{"O01-9":"aaa"}


###  普通mock
   ```python
    client = Mock_Client("192.168.1.182", 5000)
    mocker_request = MockRequest().with_path(regex("abc")).with_body(params(param("O01-9", "aaa"))).with_method("post")
    mocker_response = MockResponse().with_body("aaaa")
    mocker = Mocker(mocker_request, mocker_response)
   ```
    
###  mock with callback
   ```python
    def get_resp_by_req(req):
      return req['path']

    def create_mocker_callback():
       client = Mock_Client("192.168.1.182", 5000, get_resp_by_req)
       mocker_request = MockRequest().with_path("/abc").with_body(params(param("O01-9", "aaa"))).with_method("post")
       mocker_response = MockResponse().with_callback()
       mocker = Mocker(mocker_request, mocker_response)
       client.mock_callback(mocker)
       import time
       time.sleep(10)
       client.disconect()
     ```
