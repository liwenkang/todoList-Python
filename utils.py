# 此处定义一个 log 函数, 用于替代系统自带的 print 函数, 实现更完善的功能
import time


# 当函数的参数不确定时，可以使用*args 和**kwargs
# *args 没有key值，**kwargs有key值
# *args表示多个剩余参数()，它是一个tuple
# **kwargs表示关键字参数，它是一个dict
# 同时使用*args和**kwargs时，必须*args 在**kwargs前
# 所以在打 log 的时候,一定要注意最后才打"字典"

def log(*args, **kwargs):
    # time.time() 返回 unix time, 是1970年到现在时间相隔的时间
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    # 前面写要转换成的格式, 后面写参数
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)


def current_time():
    format = '%m/%d %H:%M'
    value = time.localtime(int(time.time()))
    # 前面写要转换成的格式, 后面写参数
    dt = time.strftime(format, value)
    return dt

