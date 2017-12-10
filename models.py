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
    # Python 的文件操作
    # w+ 可读可写，如果文件存在，则覆盖整个文件，不存在则创建
    # 参考
    # http://www.cnblogs.com/yangshl/p/6285942.html
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)


# 载入数据
def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # json.loads 是将 str 转化成 dict 格式
        return json.loads(s)


# 定义 Model
class Model(object):
    """
    Model 是所有 model 的基类,

    @classmethod 表示接下来的是一个类方法

    # python 类的实例方法，静态方法，类方法辨析和实例讲解 可以参考
        http://blog.csdn.net/a447685024/article/details/52424481
        http://www.cnblogs.com/hopeworld/archive/2011/08/16/2140145.html

    # 瓜的解释
    # @classmethod
    # 生成对象的东西都必然是类方法,第一个参数是类,不需要实例也可以调用
    #
    # Todo.all()
    # Todo 是类名,
    # all() 是一个类方法, 不需要任何实例就可以调用, 用来生成实例
    # Todo 当作 class 函数传入了
    # 相当于你调用了 Todo.all(Todo)
    #
    # 在 def save(self) 中
    #     models = self.all()
    #            = self.__class__.all()
    #     实例也可以调用类方法
    #
    # 实例方法: 只能是实例才能调用
    #
    # 静态方法:   没有第一个参数,和类是没有联系的(谁定义了这个类,谁就可以用这个静态方法)
    #             为了好看,可以写在类里面,此时必须通过类来调用

    # # get_no_of_instances() 这个方法既可以在类(ik1)中运行,也可以在实例中(Kls)运行
    # def get_no_of_instances(cls_obj):
    #     # cls_obj 是 <class '__main__.Kls'>
    #     return cls_obj.no_inst
    #
    #
    # class Kls(object):
    #     no_inst = 0
    #
    #     def __init__(self):
    #         # self 是 <__main__.Kls object at 0x000001F533D7DBA8>
    #         # Kls 是 <class '__main__.Kls'>
    #         Kls.no_inst = Kls.no_inst + 1
    #
    #
    # ik1 = Kls()
    # ik2 = Kls()
    # print(get_no_of_instances(ik1))       2
    # print(get_no_of_instances(ik2))       2
    # print(get_no_of_instances(Kls))       2

    # 我们要写一个只在类中运行而不在实例中运行的方法. 如果我们想让方法不在实例中运行，可以这么做:
    # def iget_no_of_instance(ins_obj):
    #     return ins_obj.__class__.no_inst
    #
    #
    # class Kls(object):
    #     no_inst = 0
    #
    #     def __init__(self):
    #         Kls.no_inst = Kls.no_inst + 1
    #
    #
    # ik1 = Kls()
    # ik2 = Kls()
    # # print(iget_no_of_instance(ik1))       2
    # # print(iget_no_of_instance(ik2))       2
    # # 下面这句会报错
    # # print(iget_no_of_instance(Kls))
    # # 也就是说,这样写的话, iget_no_of_instance() 只可以在类中运行(ik1),不能在实例中运行(Kls)
    # # 单纯把 def iget_no_of_instance(ins_obj) 写在 Kls 里面也不能解决问题

    # @classmethod 是为了使得 iget_no_of_instance() 既能在类中运行(ik1),也能在实例中运行(Kls)
    # class Kls(object):
    #     no_inst = 0
    #
    #     def __init__(self):
    #         Kls.no_inst = Kls.no_inst + 1
    #
    #     @classmethod
    #     def iget_no_of_instance(ins_obj):
    #         return ins_obj.no_inst
    #
    #
    # ik1 = Kls()
    # ik2 = Kls()
    # print(ik1.iget_no_of_instance())      2
    # print(ik2.iget_no_of_instance())      2
    # print(Kls.iget_no_of_instance())      2

    # class Kls(object):
    #     def __init__(self, data):
    #         self.data = data
    #
    #     def printd(self):
    #         print('self.data', self.data)
    #
    #     @classmethod  # classmethod的修饰符
    #     def class_method(cls, arg1, arg2):
    #         pass
    #
    #     @staticmethod  # staticmethod的修饰符
    #     def static_method(arg1, arg2):
    #         pass

    # Kls.printd()
    # TypeError: printd() missing 1 required positional argument: 'self'
    # 类方法的第一个参数cls，而实例方法的第一个参数是self，表示该类的一个实例。
    # 对于classmethod的参数，需要隐式地传递类名，而staticmethod参数中则不需要传递类名，其实这就是二者最大的区别。
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

    # todo 什么鬼?
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
        log('classname', classname)
        # todo 列表推倒有点没搞懂
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        log('properties', properties)
        s = '\n'.join(properties)
        log('s', s)
        log('最终结果:', '<\nclassname:{}\n properties:{}>\n'.format(classname, s))
        return '<\nclassname:{}\n properties:{}>\n'.format(classname, s)

    # 保存数据( User)
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
            """
            enumerate用法如下:
            for i, m in enumerate(models):
                log('i', i,'index')
                log('m', m,'key')
                log('models.get(m)', models.get(m),'value')
            """
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

    # 登陆检验函数
    def validate_login(self):
        # 先查询是否有当前用户
        u = User.find_by(username=self.username)
        if u is None:
            # 提醒用户用户名或者密码错误
            log('validate_login 提醒用户用户名或者密码错误')
            return False
        else:
            if u.password == self.password:
                log('validate_login  ok')
                return True
            else:
                log('validate_login  提醒用户用户名或者密码错误')
                return False
                # 提醒用户用户名或者密码错误

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


# 测试
def test1():
    # 测试 User 数据
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    log(u)
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
