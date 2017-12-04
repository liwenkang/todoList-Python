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
│	   Message.txt			// 存放用户留言
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
1. 先把小工具准备好(自定义一个 log 函数,方便后续调试) 实现 utils.py √
2. 实现 server.py √
3. 实现 models.py √
4. 实现 routes.py √
5. 实现 routes_todo.py √
6. 实现 todo.py √ 
7. 实现 templates 里的 html 文件 √
8. 小调试

#### 存在的问题:
1. 用户注册后应该直接跳转到当前用户的 todo 页面
2. 用户登录后应该直接跳转到当前用户的 todo 页面
3. Message 功能改炸了


 