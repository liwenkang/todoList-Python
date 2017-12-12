from utils import log

# 使用 socket 连接
import socket

# 引入一个解码方式,用于 url 的解析
import urllib.parse

# 实现待办事项页面的添加,编辑.删除事件
from routes.routes_todo import todo_routes

# 引入静态资源的处理函数, 读取图片并生成响应返回
from routes.routes_index import route_static

# 路由字典,实现主页显示,用户注册,登陆,留言
from routes.routes_index import index_routes


# 定义一个 class 保存请求的数据
class Request(object):
    # 初始化属性
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<\nclassname:{}\n properties:{}>\n'.format(classname, s)

    # 把从 self.headers 得到的 Cookie 格式化为字典,加入到 self.cookies 里面
    def add_cookies(self):
        """
        self.headers:
            {
                'Cookie': 'height=169; user=gua'
            }

        self.cookies
            {
                'height': '169',
                'user': 'gua'
            }
        """
        cookies = self.headers.get('Cookie', '')
        # kvs 表示 key value store 键值对的存储
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    # 把从外部得到的 header 格式化为字典,加入到 self.headers 里面,并且把 self.cookies 清空,再重新添加
    def add_headers(self, header):
        """
        header:
            [
                'Accept-Language: zh-CN,zh;q=0.8',
                'Cookie: height=169; user=gua'
            ]

        self.headers
            {
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Cookie': 'height=169; user=gua'
            }
        self.cookies
            {
                'height': '169',
                'user': 'gua'
            }
        """
        # 清空 headers
        self.headers = {}
        # 最终的结果希望是键值对
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        # 清空 self.cookies
        self.cookies = {}
        # 添加 self.cookies
        self.add_cookies()

    # 将 self.body 格式化(用等效的字符替换掉 %xx 这种格式),再将它转换为字典返回
    def form(self):
        """
        self.body:
            'name%20=liwenkang&age%20=21'

        self.body:
            {
                'name ': 'liwenkang',
                'age ': '21'
            }
        """
        body = urllib.parse.unquote(self.body)
        kvs = body.split('&')
        body = {}
        for kv in kvs:
            k, v = kv.split('=')
            body[k] = v
        return body


# 当页面响应发生错误时,根据状态码,返回不同的错误提示页面
def error(request, code=404):
    """
    这里要写多个状态码对应的页面
    一般不要使用数字来作为字典的 key
    但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# 获取原始 url 中的 path 和 query
def parsed_path(path):
    """
    case1
        path
            /login

        path
            /login
        query
            {}

    case2(一般情况)
        path
            /static?name=liwenkang&age=20

        path
            /static
        query
            {
                'name':'liwenkang',
                'age':20
            }
    """
    log('path: ', path)
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        kvs = query_string.split('&')
        query = {}
        for kv in kvs:
            k, v = kv.split('=')
            query[k] = v
        return path, query


# 根据不同的 path 调用不同的处理函数
def response_for_path(path, request):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    # 根据 path 调用相应的处理函数
    # 没有处理的 path 会返回 404
    r = {
        '/static': route_static
    }
    # 注册外部路由
    # 实现主页显示, 用户注册, 登陆, 留言
    r.update(index_routes)
    r.update(todo_routes)
    # 根据 path 返回响应, 要是出错了, 就执行 error 函数
    response = r.get(path, error)
    return response(request)


# 服务器开启函数
# todo 还可以优化
def run(host='', port=3000):
    # 初始化 socket
    # 使用 with 保证程序中断的时候正确关闭 socket
    # 释放占用的端口
    with socket.socket() as s:
        s.bind((host, port))
        # 写一个无限循环处理请求
        while True:
            # 监听
            s.listen(3)
            # 接收
            connection, address = s.accept()
            # todo 读取文件, 注意这里需要改为无限循环,从而获取全部的数据
            r = connection.recv(10000)
            # 解码为字符串
            r = r.decode('utf-8')
            # chrome 浏览器偶尔会发送空请求导致 split 后得到的 path 为空,所以预先判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]

            # 新建一个 Request 对象
            request = Request()
            # 设置 request 的method
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path, request)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
