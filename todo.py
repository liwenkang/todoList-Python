from utils import log
from utils import log_time
from models import Model


# 继承来自 Model 的类
class Todo(Model):
    def __init__(self, form):
        # 代办事件编号
        self.id = form.get('id', None)
        # 代办事件名称
        self.title = form.get('title', '')
        # user_id 表明了代办事项的拥有者
        self.user_id = form.get('user_id', '')
