# 此处定义一个 log 函数, 用于替代系统自带的 print 函数, 实现更完善的功能
import time

# 使用 jinja2 模版,更优雅的解决字符串的替代问题
from jinja2 import Environment, FileSystemLoader
import os.path


# 知识点 *args 和**kwargs
# 当函数的参数不确定时，可以使用*args 和**kwargs
# *args 没有key值，**kwargs有key值
# *args表示多个剩余参数()，它是一个tuple
# **kwargs表示关键字参数，它是一个dict
# 同时使用*args和**kwargs时，必须*args 在**kwargs前
# 所以在打 log 的时候,一定要注意最后才打"字典"

def log(*args, **kwargs):
    # time.time() 返回 unix time, 是1970年到现在时间相隔的时间 ms 为单位
    # 把 unix time 转换为普通人类可以看懂的格式
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    # 前面写要转换成的格式, 后面写参数
    dt = time.strftime(format, value)
    # a 表示追加模式不断往后写
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def test_log(*args, **kwargs):
    # time.time() 返回 unix time, 是1970年到现在时间相隔的时间 ms 为单位
    # 把 unix time 转换为普通人类可以看懂的格式
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    # 前面写要转换成的格式, 后面写参数
    dt = time.strftime(format, value)
    # a 表示追加模式不断往后写
    print(dt, *args, **kwargs)


def current_time():
    format = '%m/%d %H:%M'
    value = time.localtime(int(time.time()))
    # 前面写要转换成的格式, 后面写参数
    dt = time.strftime(format, value)
    return dt


# __file__ 就是本文件的名字
# 得到用于加载模板的目录,此处是一个绝对路径
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def templateM(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


