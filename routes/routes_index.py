# 引入生成随机数的 random
import random

# 引入 log 函数
from utils import log
from utils import templateM
from utils import current_time

from models import save
from models import load
from models import out_salted_password

from models import Message
from models import User

# session 可以在服务器端实现用户账户过期功能
# 可以定时让 cookie 失效
session = {}


# 生成一个随机字符串来作为 Cookie 的加密
def random_str():
    """
    result
        'lzLj45Q7augckQsj'
    """
    character = 'abcdefghijklmnopqlstuvwxyzABCDEFGHIJKLMNOPQLSTUVWXYZ0123456789'
    result = ''
    for i in range(16):
        random_index = random.randint(0, len(character) - 1)
        result += character[random_index]
    return result


# 根据 cookie 里是否有 user 信息,返回当前用户的名称
def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '游客')
    return username


# 根据 cookie 里是否有 id 信息,返回当前用户的 id
def current_id(request):
    session_id = request.cookies.get('user', '')
    uname = session.get(session_id, '游客')
    u = User.find_by(username=uname)
    if u is not None:
        return u.id
    else:
        return None


# 根据 cookie 里是否有 role 信息,返回当前用户的 role
def current_role(request):
    session_id = request.cookies.get('user', '')
    uname = session.get(session_id, '游客')
    u = User.find_by(username=uname)
    if u is not None:
        return u.role
    else:
        return None


# 根据 headers(字典) 生成响应头
def response_with_headers(headers, code=200):
    """
    headers
        {
            'age': 20,
            'name': 'liwenkang'
        }
    code
        200

    header
        HTTP/1.1 200 OK
        age: 20
        name: liwenkang
    """
    if code == 200:
        header = 'HTTP/1.1 {} OK\r\n'.format(code)
    elif code == 302:
        header = 'HTTP/1.1 {} redirect\r\n'.format(code)

    kvs = headers.items()
    items = []
    for k, v in kvs:
        item = '{}: {}\r\n'.format(k, v)
        items.append(item)
    header += ''.join(items)
    return header


# 根据 302 状态码实现重定向(当用户未登录就想留言时)
def redirect(url):
    """
    url
        /

    r.encode('utf-8')
        HTTP/1.1 302 xxx
        Location: /

    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    301是一个浏览器的永久重定向,浏览器会记住它
    302是一个浏览器的临时重定向
    """
    headers = {
        'Content-Type': 'text/html',
        'Location': url
    }
    # 重新生成 HTTP 响应
    # 注意此次响应没有 HTTP body 部分
    header = response_with_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode('utf-8')


# 处理静态资源(如图片),生成响应
def route_static(request):
    # 如果没找到,就默认使用doge.gif
    filename = request.query.get('file', 'doge.gif')
    # 路径
    path = 'static/' + filename
    # 'r'表示只读, 'b'代表二进制模式访问
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        # f.read() 表示就是 path 位置存储的文件(二进制)
        img = header + f.read()
        return img


# 加载主页(将 header + index.html 页面编码后返回)
def route_index(request):
    username = current_user(request)
    header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n'
    body = templateM('index.html', username=username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 加载登录页面(将 header + login.html 页面编码后返回)
def route_login(request):
    # 点击登陆后,验证用户信息,改变页面上的信息(登陆是否成功)
    headers = {
        'Content-Type': 'text/html'
    }
    username = current_user(request)
    # 验证为 post 请求
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)

        # u = User(form)

        if u.validate_login():
            # 为了防止用户伪造 cookie 信息,所以设置一个随机字符串来加密用户名
            # 首先生成一个 16 位的随机字符串
            session_id = random_str()
            # 也就是我把随机生成的字符串作为用户名
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            # 真实的 username 存在 session[session_id] 里
            session[session_id] = u.username
            result = '登陆成功 <p><a href="/todo">进入 todo 页面</a></p><p><a href="/messages">进入 Message 页面</a></p>'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = templateM('login.html', result=result, username=username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 加载一个管理页面(这个页面显示了所有的用户 包括 id username password)
def route_admin(request):
    # 只允许 role 为 1 的用户组访问
    if current_role(request) == 1:
        data = load('data/User.txt')
        # list 转换为 str
        headers = {
            'Content-Type': 'text/html'
        }
        body = templateM('admin.html', users=data)
        header = response_with_headers(headers)
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')
    else:
        return redirect('/login')


# 加载注册页面(将 header + register.html 页面编码后返回)
def route_register(request):
    header = 'HTTP/1.1 210 OK\r\nContent-Type: text/html\r\n'
    # 验证 POST 请求
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        flag = u.validate_register()
        if flag == '该用户名已存在':
            result = '注册失败: 该用户名已存在'
            body = templateM('register.html', result=result)
        elif flag == True:
            u.save()
            result = '注册成功: 您的账号为 {}'.format(u.username)
            # result = '注册成功<br> <pre>{} {}</pre>'.format(User.all())
            body = templateM('register.html',
                             result=result + '<p><a href="/login">进入登录页面</a></p>')
        else:
            result = '注册失败: 用户名和密码均必须以字母开头,且只能包含英文字符,数字和下划线,长度在6--18之间'
            body = templateM('register.html', result=result)
    else:
        # 打开网页时自动的 GET 请求
        body = templateM('register.html', result='')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 对于已登录的用户加载留言页面(将 header + message.html 页面编码后返回)
def route_message(request):
    username = current_user(request)
    # 如果此时用户未登录,重定向到 '/'
    if username == '游客':
        return redirect('/login')

    # 判断 POST 请求
    if request.method == 'POST':
        # 先加载原有数据
        form = request.form()
        t = Message.new(form)
        # 加个时间
        t.time = current_time()
        item = t.saveMessage()
        save(item, 'data/Message.txt')
        # 将 list 转换成 str
        body = templateM('message.html', messages=item)
    elif request.method == 'GET':
        # 也就是说,当我第一次访问 http://localhost:3000/messages 时,会先发送 GET 请求
        # 定向到了新的 url
        # http://localhost:3000/messages?message=gua
        if any(request.query) == False:
            # 说明是进入网页的时候提交的 GET 请求
            # 提取出现有的 Message.
            path = 'data/Message.txt'
            data = load(path)
            body = templateM('message.html', messages=data)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 系统管理员根据 id 修改用户的密码
def route_update(request):
    form = request.form()
    if request.method == 'POST':
        oldId = form.get('id')
        new_password = form.get('password')
        u = User.find_by(id=int(oldId))
        # 需要加密
        u.password = out_salted_password(new_password)
        u.save()
        return redirect('/admin/users')


# 路由字典,实现主页显示,用户注册,登陆,留言
index_routes = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/admin/users': route_admin,
    '/admin/user/update': route_update
}
