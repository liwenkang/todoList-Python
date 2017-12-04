# 引入 log 函数
from utils import log

# 引入 Todo
from todo import Todo

# 引入 User
from models import User

# 引入 current_user 函数
from routes import current_user

# 引入 template 函数
from routes import template

# 引入 response_with_headers 函数
from routes import response_with_headers

# 引入 redirect 函数
from routes import redirect


# 验证是否登陆
def login_required(route_function):
    def f(request):
        # 加载任意内容前先验证是否登陆
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            # 说明用户没登陆,重定向到 login 页面
            redirect('/login')
        return route_function(request)

    return f


# 加载主页(将 header + index.html 页面编码后返回)
def index(request):
    # 加载主页前先验证是否登陆
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        # 说明用户没登陆,重定向到 login 页面
        return redirect('/login')

    headers = {
        'Content-Type': 'text/html'
    }
    todo_list = Todo.find_all(user_id=u.id)
    # 把所有的代办事件都加上编辑和删除功能
    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
        todos.append(s)
    todo_html = ''.join(todos)

    # 用 todo_html 替换掉在页面中预留的 todos
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 加载编辑页面(将 header + todo_edit.html 页面编码后返回)
def edit(request):
    headers = {
        'Content-Type': 'text/html'
    }

    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)

    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))

    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 添加 todo
def add(request):
    # 添加事件前验证是否登陆
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')

    headers = {
        'Content-Type': 'text/html'
    }

    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
        # 我们看到页面刷新的过程:
        '''
    点击add按钮添加一个新 todo 的时候,程序的流程如下(包含原始 HTTP 报文)
    1. 浏览器提交一个表单给服务器(发送 POST 请求)
        POST /todo/add HTTP/1.1
        Content-Type: application/x-www-form-urlencoded

        title=heuv

    2. 服务器把解析后的数据存放到指定的文件里(也就是增加了一个新的数据),并返回302响应
        HTTP/1.1 302 
        Location:/todo


        以下相当于你第一次访问这个页面

    3. 浏览器根据 302 中的地址,发送了一条新的 GET 请求
        GET /todo HTTP/1.1
        HOST:...

    4. 服务器给浏览器一个页面响应
        HTTP/1.1 200 
        Content-Type: text/html
        Content-Length: ...

        <html>
            ...
        </html>            

    5. 新页面经过浏览器解析,展现出来(因为数据变了,所以页面变了)
    '''
    return redirect('/todo')


# 加载更新页面(将 header + add.html 页面编码后返回)
def update(request):
    if request.method == 'POST':
        form = request.form()
        todo_id = int(str(form.get('id', -1)))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')


# 删除 todo
def delete_todo(request):
    # 删除事件前验证是否登陆
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')

    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)

    if t.user_id != u.id:
        return redirect('login')

    if t is not None:
        t.remove()

    return redirect('/todo')


# 路由字典
# 实现待办事项页面的添加,编辑.删除事件
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': login_required(edit),
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': login_required(update),
    '/todo/delete': delete_todo,
}
