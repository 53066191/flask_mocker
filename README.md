# flask_mocker

    自动化需求， 在自动化代码中，直接控制mock服务器返回报文，
    mock服务器接收到请求后，转发至自动化代码中，从而达到自动化代码中生成需要的返回报文目的
    
    暂时只支持完全匹配以及正则匹配


###  客户端支持匹配方式：
    1.regex(): 带上此函数后，将转为正则表达式匹配
    2.parmas(param("O01-9", "aaa")), body中含有{"O01-9":"aaa"}


###  普通mock
```python
    client = Mock_Client("192.168.1.182", 5000)
    mocker_request = MockRequest().with_path(regex("abc")).with_body(params(param("O01-9", "aaa")))
    mocker_response = MockResponse().with_body("aaaa")
    mocker = Mocker(mocker_request, mocker_response)
    client.mock(mocker)

```

###  mock with callback

```python
    '''
      req结构：{
                'path': request.path,
                'json': request.json,
                'data': request.data.decode(encoding='utf-8'),
                'header': request.content_type,
                'id': mocker.id
                }
    '''
    def get_resp_by_req(req):
      return req['path']

    def create_mocker_callback():
       client = Mock_Client("192.168.1.182", 5000)
       mocker_request = MockRequest().with_path("/abc").with_body(params(param("O01", "aaa"))).with_method("post")
       mocker_response = MockResponse().with_callback(get_resp_by_req).with_header('name', 'liuyun')
       mocker = Mocker(mocker_request, mocker_response)
       client.mock_callback(mocker)
       import time
       time.sleep(10)
       client.disconect()
```

###  转发
      mock服务器匹配mock失败，则转发至真实服务器
```python
      #/abc不經過mock直接轉發至193
      .*:/abc:.*:.*=192.168.1.193:9090
      #無匹配mock，轉發至193
      .*:.*:.*:.*=192.168.1.193:9090
```
