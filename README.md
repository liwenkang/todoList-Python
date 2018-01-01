### 你好,这是一个 todo 小应用(基于Python)

#### 使用方法:
1. 运行 server.py 后
2. 打开浏览器,输入 localhost:3000


```
测试账户

用户名 liwenkang 密码 liwenkang (拥有管理员权限)
用户名 guagua 密码 guagua (普通用户)
```

#### 基础功能：
1. 显示所有todo
2. 增加todo(时间标签)
3. 更新todo(时间标签)
4. 删除todo
5. 用户登陆
6. 用户注册
7. 用户留言
8. 管理员界面,对于所有用户的 id ,用户名,密码查看
9. 管理员根据 id 修改不同用户的密码
10. 利用 jinja2 模版框架,生成 html(相当于优化了 replace ,而且可以直接传入 dict 做替换)
11. 将用户的密码加密(摘要算法)后存放

#### 包含的文件如下:
<pre>
├─data	
│      Todo.txt             // 存放事件信息
│      User.txt             // 存放用户信息
│      Message.txt          // 存放用户留言
│
├─static
│      doge.gif             // 在主页上放三张图,以表示尴尬
│      doge1.jpg
│      doge2.gif
│
├─templates
│      admin.html           // 显示管理员页面
│      message.html         // 显示 Message 页面
│      index.html           // 显示主页
│      login.html           // 显示用户登陆界面
│      register.html        // 显示用户注册界面
│      todo_edit.html       // 显示编辑 todo 的界面
│      todo_index.html      // 显示所有 todo 的页面
│
├─log.txt                   // 记录调试日志
├─models.py                 // 主页 Model
├─routes.py                 // 主页路由函数
├─routes_todo.py            // todo 路由函数
├─server.py                 // 建立一个 server.py
├─todo.py                   // 包含了 Todo Model, 用于处理数据
├─utils.py                  // 自定义的工具函数
└─summarize.md              // 知识点总结
</pre>

#### 主要涉及的知识点见 summarize.md

#### 实现过程:
1. 实现 utils.py √
2. 实现 server.py √
3. 实现 models.py √
4. 实现 routes.py √
5. 实现 routes_todo.py √
6. 实现 todo.py √ 
7. 实现 templates 里的 html 文件 √
8. 小调试 √

#### 存在的问题:
1. 用户登录后,登录框应该隐藏掉
2. 用户登录后,注册框应该隐藏掉
3. server.py 的 306 行,读取文件,需要改为无限循环,从而获取全部的数据
4. 调试中,发现 Chrome 突然抽风,输入用户名和密码后点击登录会直接报错(相当于发送了空的 POST 请求),改为 Firefox 后没有发现异常,后来再使用 Chrome 时,一切正常, 需要关注一下(当前后台服务器为单线程的，需要改为支持多线程的)
5. 如果一个用户新注册了账号,应该在注册成功的页面上让用户可以选择进入 TODO 或者 Message 页面
6. 不同用户共享了一个计数的 id 值,应该不同用户拥有不同的计数 id
7. Model 里面有个类方法 new ,没搞懂,感觉 User.new(form) 和 User(form) 是一样的
