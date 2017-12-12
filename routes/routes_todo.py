# 引入 log 函数
from utils import log
from utils import current_time
# 引入 template 模版函数
from utils import templateM

# 引入 Todo
from models import Todo

# 引入 User
from models import User

# 引入 current_user 函数
from routes.routes_index import current_user

# 引入 response_with_headers 函数
from routes.routes_index import response_with_headers

# 引入 redirect 函数
from routes.routes_index import redirect


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

    body = templateM('todo_index.html', todos=todo_list)

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

    body = templateM('todo_edit.html', todo_id=str(t.id), todo_title=str(t.title))

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
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.created_time = current_time()
        t.save()
    '''
    我们看到页面刷新的过程:
    README.md 中的 网络部分 5. 请求数据和发送数据(具体到各阶段的原始报文信息)
    '''
    return redirect('/todo')


# 加载更新页面(将 header + add.html 页面编码后返回)
def update(request):
    if request.method == 'POST':
        form = request.form()
        todo_id = int(str(form.get('id', -1)))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.updated_time = current_time()
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
todo_routes = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': login_required(edit),
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': login_required(update),
    '/todo/delete': delete_todo,
}
