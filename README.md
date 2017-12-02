### 你好,这是一个 todo 小应用(基于Python)

#### 基础功能：
1. 显示所有todo
2. 增加todo 
3. 更新todo 
4. 删除todo 
5. 用户登陆

#### 包含的文件如下:
<pre>
├─data 
│      Todo.txt             // 存放事件信息
│      User.txt             // 存放用户信息
│
├─static
│      doge.gif             // 在主页上放三张图,以表示尴尬
│      doge1.jpg
│      doge2.gif
│
├─templates
│      html_basic.html      
│      index.html           // 显示主页
│      login.html           // 显示用户登陆界面
│      register.html        // 显示用户注册界面
│      todo_edit.html       // 显示编辑 todo 的界面
│      todo_index.html      // 显示所有 todo 的页面
├─models.py
├─routes.py
├─routes_todo.py            // 包含了应用的所有路由函数 
├─server.py         
├─todo.py                   // 包含了 Todo Model, 用于处理数据
└─utils.py
</pre>

#### 主要涉及的知识点:
1. 请求数据和发送数据(具体到各阶段的原始报文信息)
2. 路由的实现
3. 利用302状态码实现重定向
4. Python的基础

#### 实现过程:
0. 先把小工具准备好(自定义一个 log 函数,方便后续调试) √
1. 实现用户的注册和登陆,并返回信息
2. 实现 todo 的事件添加,更新,删除
3. 实现 todo 事件和用户的绑定