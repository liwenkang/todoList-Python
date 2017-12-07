# 引入 log 函数
from utils import log

# 使用 socket 连接
import socket

# 引入一个解码方式,用于 url 的解析
import urllib.parse

# 引入 route_dict 路由字典,并把它改名为 todo_route ,实现待办事项页面的添加,编辑.删除事件
from routes_todo import route_dict as todo_route

# 引入静态资源的处理函数, 读取图片并生成响应返回
from routes import route_static
# 引入 route_dict 路由字典,实现用户注册,登陆啥的
from routes import route_dict


# 定义一个 class 保存请求的数据
class Request(object):
    # 初始化属性
    def __init__(self):
        """
        todo GET 和 POST 方法分析
        参考
        http://www.cnblogs.com/igeneral/p/3641574.html
        http://blog.csdn.net/lenovouser/article/details/52909842
        http://blog.csdn.net/u014612859/article/details/24381329
        GET一般用于获取 / 查询资源信息，而POST一般用于更新资源信息
        请求方法为 GET 从指定的服务器中获取数据,查询字符串（键值对）被附加在URL地址后面一起发送到服务器
        header 区别如下所示
            method: (POST)
            query: ({})
            body: (message=gua&author=gua)


            method: (GET)
            query: ({'message': 'guagua'})
            body: ()
        """
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def __repr__(self):
        """
        __str__ 和 __repr__ 方法

        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式

        class A(object):
            def __str__(self):
                return "this is A class"

            def __repr__(self):
                return "this is repr func"

        a = A()
        print(a) 调用的是 a 的 __str__ 方法,给用户看的
        如果在python解释器里直接敲a后回车，调用的是a.__repr__()方法,给机器看的
        """
        classname = self.__class__.__name__
        # todo 列表推倒有点没搞懂
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

        todo 关于编码问题,详细讨论可见阮大哥博客和官方文档
            http://www.ruanyifeng.com/blog/2010/02/url_encoding.html
            https://docs.python.org/3.2/library/urllib.parse.html

        urllib.parse.unquote 用法如下
        example:
            input:  'El%20Ni%C3%B1o'
            output: 'El Niño'
        """
        body = urllib.parse.unquote(self.body)
        kvs = body.split('&')
        body = {}
        for kv in kvs:
            k, v = kv.split('=')
            body[k] = v
        return body


# 新建一个 Request 对象
request = Request()


# 当页面响应发生错误时,根据状态码,返回不同的错误提示页面
def error(request, code=404):
    """
    这里要写多个状态码对应的页面
    有关状态码部分参考 http://tool.oschina.net/commons?type=5
    """
    # 一般不要使用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# 获取原始 url 中的 path 和 query todo 这里的输入到底是啥?
def parsed_path(path):
    """
    case1
        path
            www.baidu.com

        path
            www.baidu.com
        query
            {}

    case2
        path
            www.baidu.com/s?name=liwenkang&age=20

        path
            www.baidu.com/s
        query
            {
                'name':'liwenkang',
                'age':20
            }
    """

    """
    url 组成部分
    参考: 
        http://blog.csdn.net/ergouge/article/details/8185219
        http://blog.csdn.net/u014421556/article/details/51671353
    
    假设有一个 url 为 http://www.aspxfans.com:8080/news/index.asp?boardID=5&ID=24618&page=1#name
    
    从上面的URL可以看出，一个完整的URL包括以下几部分：
    
    1.协议部分(URL scheme specifier)：该URL的协议部分为 http: 这代表网页使用的是HTTP协议。在Internet中可以使用多种协议，如HTTP，FTP等等本例中使用的是HTTP协议。在"HTTP"后面的“//”为分隔符
    
    2.域名部分(Host name)：该URL的域名部分为 www.aspxfans.com 一个URL中，也可以使用IP地址作为域名使用
    
    3.端口部分(Port number)：跟在域名后面的是端口 8080 域名和端口之间使用“:”作为分隔符。端口不是一个URL必须的部分，如果省略端口部分，将采用默认端口(http默认端口为80, https默认端口为443 参考 http://blog.csdn.net/u014421556/article/details/51671353 )
    
    域名加端口就是Network location part
    
    4.虚拟目录部分：从域名后的第一个“/”开始到最后一个“/”为止，是虚拟目录部分。虚拟目录也不是一个URL必须的部分。本例中的虚拟目录是 /news/
    
    5.文件名部分：从域名后的最后一个“/”开始到“？”为止，是文件名部分，如果没有“?”,则是从域名后的最后一个“/”开始到“#”为止，是文件部分，如果没有“？”和“#”，那么从域名后的最后一个“/”开始到结束，都是文件名部分。本例中的文件名是 index.asp 。文件名部分也不是一个URL必须的部分，如果省略该部分，则使用默认的文件名(比如常见的 index.html )
 
    虚拟目录 + 文件名称 就是Hierarchical path
       
    6.锚部分(Fragment identifier)：从“#”开始到最后，都是锚部分。本例中的锚部分是“name”。锚部分也不是一个URL必须的部分
    
    7.参数部分(Query component)：从“？”开始到“#”为止之间的部分为参数部分，又称搜索部分、查询部分。本例中的参数部分为
        boardID=5&ID=24618&page=1。参数可以允许有多个参数，参数与参数之间用“&”作为分隔符。

    """

    """
    url分解
    
    import urllib.parse
    
    result = urllib.parse.urlparse('http://www.aspxfans.com:8080/news/index.asp?boardID=5&ID=24618&page=1#name')
    print(result.path)
    
    
     ParseResult(
        scheme='http',
        netloc='www.aspxfans.com:8080', 
        path='/news/index.asp', 
        params='', 
        query='boardID=5&ID=24618&page=1', 
        fragment='name'
    )
    
    # urllib.parse.urlparse将传入的url解析成了六大部分，是一个元组，含协议名称、域名、路径等
    
    Attribute	Index	Value	                            Value if not present
    scheme	    0	    URL scheme specifier	            scheme parameter
    netloc	    1	    Network location part	            empty string
    path	    2	    Hierarchical path	                empty string
    params	    3	    Parameters for last path element	empty string
    query	    4	    Query component	                    empty string
    fragment	5	    Fragment identifier	                empty string
        
    """

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
def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    # 根据 path 调用相应的处理函数
    # 没有处理的 path 会返回 404
    r = {
        '/static': route_static
    }
    # 更新用户注册,登陆的路由字典
    r.update(route_dict)
    # 更新待办事项的路由字典
    r.update(todo_route)
    # 根据 path 返回响应, 要是出错了, 就执行 error 函数
    response = r.get(path, error)
    return response(request)


# 服务器开启函数
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
            # 读取文件, 注意这里需要改为无限循环,从而获取全部的数据
            r = connection.recv(10000)
            # 解码为字符串
            r = r.decode('utf-8')
            # chrome 浏览器偶尔会发送空请求导致 split 后得到的 path 为空,所以预先判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置 request 的method
            request.method = r.split()[0]
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            request.body = r.split('\r\n\r\n', 1)[1]
            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
