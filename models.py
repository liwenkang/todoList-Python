# 引入 log 函数
from utils import log

# 引入 json ,用于将数据转换为 JSON 格式再读取和存储
import json

# 引入正则表达式模块
import re


# 保存数据
def save(data, path):
    """
    data 为 dict 或 list
    path 表示文件路径
    """
    # json.dumps 是将 dict 转化成 str 格式
    # ensure_ascii = False 是为了让它正确显示中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


# 载入数据
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # json.loads 是将 str 转化成 dict 格式
        return json.loads(s)


# 加密数据
def out_salted_password(password, salt='5&4*$%":<>|dfewd5'):
    import hashlib
    def sha256(ascii_str):
        # 用 ascii 编码转换成 bytes 对象
        obj = ascii_str.encode('ascii')
        return hashlib.sha256(obj).hexdigest()
    hash1 = sha256(password)
    hash2 = sha256(hash1 + salt)
    return hash2


# Model 是一个 ORM（object relation mapper）对象关系映射
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """

    # db_path 方法返回调用该方法的类的 txt 文件路径
    @classmethod
    def db_path(cls):
        # cls 是类名,谁调用的类名就是谁的,所以可以通过cls.__name__得到 class 的名字
        # 例如
        # user = User()
        # user.db_path()
        # 返回
        # User.txt
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    # all 方法使用 load 函数得到所有的 models
    @classmethod
    def all(cls):
        path = cls.db_path()
        # models 是 dict
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls.new(m) 可以初始化一个 cls 的实例
        ms = [cls.new(m) for m in models]
        return ms

    # todo 这里用不用 new  好像没差别 ?
    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    # 在类中找到含有指定一个条件的 对象
    @classmethod
    def find_by(cls, **kwargs):
        # u = User.find_by(username='gua')
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            # m.__dict__[k] 等价于 getattr(m,k)
            if v == m.__dict__[k]:
                return m
        return None

    # 在类中找到含有指定多个条件的 对象
    @classmethod
    def find_all(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        data = []
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                data.append(m)
        return data

    @classmethod
    def find_by_id(cls, id):
        return cls.find_by(id=id)

    # 这里还可以写一个 delete 方法, 代替 remove

    # 重写了 __repr__ ,让 log 出来的信息更加可读
    @classmethod
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
        如果在 python 解释器里直接敲a后回车，调用的是 a.__repr__() ,给机器看的
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<\nclassname:{}\n properties:{}>\n'.format(classname, s)

    # 保存数据 (User)
    def save(self):
        models = self.all()
        first_index = 1
        if self.__dict__.get('id') is None:
            # 之前没有id这儿属性,说明在文件中没有存放这个数据,我就直接写入新的数据
            if len(models) > 0:
                # 不是第一个数据
                self.id = models[-1].id + 1
            else:
                self.id = first_index
            models.append(self)
        else:
            # 有id这个属性,说明是已经存在文件中的数据,那么我需要找到相应的数据并且替换
            # 默认找不到 index = -1
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    # 如果遍历得到的 id 等于 自己的 id
                    index = i
                    break
            if index > -1:
                # 说明 index 发生了变化,也就说明找到了,那么第 index 个的内容就被新的内容所替代,生成新的 models
                models[index] = self

                # 将新的 models 遍历后,根据名字,存入对应的路径文件中
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
        log('l, path', l, path)

    # 保存数据 (Message)
    def saveMessage(self):
        models = self.all()
        first_index = 1
        if self.__dict__.get('message_id') is None:
            # 之前没有id这儿属性,说明在文件中没有存放这个数据,我就直接写入新的数据
            if len(models) > 0:
                # 不是第一个数据
                self.message_id = models[-1].message_id + 1
            else:
                self.message_id = first_index
            models.append(self)
        else:
            # 有id这个属性,说明是已经存在文件中的数据,那么我需要找到相应的数据并且替换
            # 默认找不到 index = -1
            index = -1
            for i, m in enumerate(models):
                if m.message_id == self.message_id:
                    # 如果遍历得到的 id 等于 自己的 id
                    index = i
                    break
            if index > -1:
                # 说明 index 发生了变化,也就说明找到了,那么第 index 个的内容就被新的内容所替代,生成新的 models
                models[index] = self

                # 将新的 models 遍历后,根据名字,存入对应的路径文件中
        l = [m.__dict__ for m in models]
        return l

    # 删除数据
    def remove(self):
        models = self.all()
        first_index = 1
        if self.__dict__.get('id') is not None:
            # id 属性存在
            # 默认找不到 index = -1
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    # 如果遍历得到的 id 等于 自己的 id,说明找到了
                    index = i
                    break
            if index > -1:
                # index 发生了变化,说明 index 被找到了
                del models[index]
        # 将新的 models 遍历后,根据名字,存入对应的路径文件中
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


# 定义 User
class User(Model):
    # 用来保存用户的数据,有 3 个属性, id , username , password
    def __init__(self, form):
        # form 表示从外面给的 一个用户对象
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.role = form.get('role', 10)
        if self.role is not None:
            self.role = int(self.role)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    # 用户密码加密(使用了 hash 加密)
    def salted_password(self, password, salt='5&4*$%":<>|dfewd5'):
        import hashlib
        def sha256(ascii_str):
            # 用 ascii 编码转换成 bytes 对象
            obj = ascii_str.encode('ascii')
            return hashlib.sha256(obj).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    # 登陆检验函数
    def validate_login(self):
        # 先查询是否有当前用户
        u = User.find_by(username=self.username)
        if u is None:
            # 提醒用户用户名错误
            return False
        else:
            if u.password == self.salted_password(self.password):
                return True
            else:
                # 提醒用户密码错误
                return False

    # 注册检验函数
    def validate_register(self):
        # 以字母开头，长度在6~18之间，只能包含字符、数字和下划线
        u = User.find_by(username=self.username)
        if u is not None:
            return '该用户名已存在'
        pattern = re.compile(r'^[a-zA-Z]\w{5,17}$')
        nameMatch = pattern.search(self.username)
        passwordMatch = pattern.search(self.password)
        if nameMatch and passwordMatch:
            # 执行加密
            pwd = self.password
            self.password = self.salted_password(pwd)
            return True
        else:
            return False


# 定义 Message
class Message(Model):
    # 用来保存用户的留言
    def __init__(self, form):
        self.message = form.get('message')
        self.author = form.get('author')
        self.time = form.get('time')
        self.message_id = form.get('message_id')


# 定义 Todo
class Todo(Model):
    def __init__(self, form):
        # 代办事件编号
        self.id = form.get('id', None)
        # 代办事件名称
        self.title = form.get('title', '')
        # user_id 表明了代办事项的拥有者
        self.user_id = form.get('user_id', '')
        # 新增时间
        self.created_time = form.get('created_time', '出错了')
        # 刷新修改时间
        self.updated_time = form.get('updated_time', '未作修改')


# 测试
def test1():
    # 测试 User 数据
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    u.save()


def test2():
    # 测试 Message 数据
    # 测试 Message 数据
    form = dict(
        author='gua',
        message='gua',
    )
    m = Message(form)
    m.save()


if __name__ == '__main__':
    test1()
    # test2()
