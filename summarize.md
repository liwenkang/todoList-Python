# 网络相关

1. 路由的实现

2. 利用 302 状态码实现重定向
```
有关状态码部分参考 

浏览器在收到 302 响应的时候,会自动在 HTTP header 里面找 Location 字段,并获取一个 url 然后自动请求新的 url 301是一个浏览器的永久重定向,浏览器会记住它
302是一个浏览器的临时重定向
```
	常见状态码可以参考
	http://tool.oschina.net/commons?type=5

3. POST 和 GET 的区别
	GET一般用于获取 / 查询资源信息，而POST一般用于更新资源信息 请求方法为 GET 从指定的服务器中获取数据,查询字符串（键值对）被附加在URL地址后面一起发送到服务器 header 
```
区别如下所示
method: (POST)
query: ({}) 
body: (message=gua&author=gua)     

method: (GET)
query: ({
	'message': 'gua',
	'author': 'gua'
}) 
body: ()
```

	参考 
	http://www.cnblogs.com/igeneral/p/3641574.html 			
	
	http://blog.csdn.net/lenovouser/article/details/52909842
 								
	http://blog.csdn.net/u014612859/article/details/24381329 


4. url 组成部分?

```
假设有一个 url 为
 http://www.aspxfans.com:8080/news/index.asp?boardID=5&ID=24618&page=1#name   

从上面的URL可以看出，一个完整的URL包括以下几部分：

1.协议部分(URL scheme specifier)：该URL的协议部分为 http: 这代表网页使用的是HTTP协议。在Internet中可以使用多种协议，如HTTP，FTP等等本例中使用的是HTTP协议。在"HTTP"后面的“//”为分隔符   

2.域名部分(Host name)：该URL的域名部分为 www.aspxfans.com 一个URL中，也可以使用IP地址作为域名使用   	

3.端口部分(Port number)：跟在域名后面的是端口 8080 域名和端口之间使用“:”作为分隔符。端口不是一个URL必须的部分，如果省略端口部分，将采用默认端口(http默认端口为80, https默认端口为443 参考 http://blog.csdn.net/u014421556/article/details/51671353 )   

域名加端口就是Network location part   

4.虚拟目录部分：从域名后的第一个“/”开始到最后一个“/”为止，是虚拟目录部分。虚拟目录也不是一个URL必须的部分。本例中的虚拟目录是 /news/  

5.文件名部分：从域名后的最后一个“/”开始到“？”为止，是文件名部分，如果没有“?”,则是从域名后的最后一个“/”开始到“#”为止，是文件部分，如果没有“？”和“#”，那么从域名后的最后一个“/”开始到结束，都是文件名部分。本例中的文件名是 index.asp 。文件名部分也不是一个URL必须的部分，如果省略该部分，则使用默认的文件名(比如常见的 index.html )   

虚拟目录 + 文件名称 就是Hierarchical path

6.锚部分(Fragment identifier)：从“#”开始到最后，都是锚部分。本例中的锚部分是“name”。锚部分也不是一个URL必须的部分   

7.参数部分(Query component)：从“？”开始到“#”为止之间的部分为参数部分，又称搜索部分、查询部分。本例中的参数部分为 boardID=5&ID=24618&page=1。参数可以允许有多个参数，参数与参数之间用“&”作为分隔符。   
```
5. 请求数据和发送数据(具体到各阶段的原始报文信息)
```
点击add按钮添加一个新 todo 的时候,程序的流程如下(包含原始 HTTP 报文)

1.浏览器提交一个表单给服务器(发送 POST 请求)
POST /todo/add HTTP/1.1 
Content-Type: application/x-www-form-urlencoded   
title=喝水

2.服务器把解析后的数据存放到指定的文件里(也就是增加了一个新的数据),并返回302响应
HTTP/1.1 302
Location:/todo    

以下相当于你第一次访问这个页面   

3.浏览器根据 302 中的地址,发送了一条新的 GET 请求
GET /todo HTTP/1.1 HOST:...  

4. 服务器给浏览器一个页面响应
HTTP/1.1 200    
Content-Type: text/html
Content-Length: ...   

<html> ... </html> 
5.新页面经过浏览器解析,展现出来(因为数据变了,所以页面变了)
```
6. 数据加密
```
1. 
摘要算法是一种能产生特殊输出格式的算法
给定任意长度的数据生成定长的密文
摘要结果是不可逆的,不能被还原为原数据,理论上无法通过反向运算取得原数据内容
一个安全的摘要算法是无法找到碰撞的
碰撞是说, 两个不一样的数据, 产生了一样的结果 
通常只被用来做数据完整性验证:比如网站在下载页面公布文件的 sha1 摘要结果,你下载后自己生成结果来对比,就能知道文件是否被篡改,或者是用来加密用户密码

常用的摘要算法主要有 md5 和 sha1
md5 的输出结果为 32 字符
sha1 的输出结果为 40 字符

import hashlib 
# 用 ascii 编码转换成 bytes 对象 
# 将字符串 'gua' 加密
pwd = 'gua'.encode('ascii')

# 创建 md5 对象 
m = hashlib.md5(pwd) 
# 返回摘要字符串, 这里是 c9c1ebed56b2efee7844b4158905d845
print(m.hexdigest())

# 创建 sha1 对象 
s = hashlib.sha1(pwd) 
# 返回摘要字符串, 这里是 4843c628d74aa10769eb21b832f00a778db8b17e 
print(s.hexdigest())           

2
用 md5 或者 sha1 保护用户的密码 用户的密码存在数据库中, 有可能会被黑客盗取(拖库) 所以一般会对用户的密码使用摘要算法加密 存储在数据库中的是加密后的密文 (所以找回密码是不可能的, 只能重置, 因为摘要不可逆)

3
用 salt 防止黑客对密码进行碰撞
假如用户使用简单密码, 破解者可以用提前生成的简单密码摘要表(彩虹表),来破解原文,所以我们会存储一个额外的信息, 扰乱用户的简单密码,一般不需要给不同的用户带上不同的"盐",因为加了一种盐之后的破解成本就很高了.

使用如下函数可以生成一个带盐的密文 
def salted_password(self, password, salt='用于混淆的盐'):
	def md5hex(ascii_str):
		return hashlib.md5(ascii_str.encode('ascii')).hexdigest() 
		hash1 = md5hex(password) 
		hash2 = md5hex(hash1 + salt) 
		return hash2     

4
重置密码功能:一般情况下,当用户重置密码时,我们在确认用户身份后,会发送一个链接地址到用户的邮箱,这个 url 地址中就包含了识别该用户的唯一 id ,此处的 id 是需要加密的,否则任何人都可以伪装成他人修改密码
```
# Python 相关

1. __str__ 和 __repr__ 方法 ?
   __repr__ 是一个魔法方法
   简单来说, 它的作用是得到 类 的 字符串表达形式
```
class A(object):
	def __str__(self):
		return "this is A class"

	def __repr__(self):
		return "this is repr func"

a = A()
print(a) //"this is A class"  调用的是 a 的 __str__ 方法,给用户看的
// 如果在 python 解释器里直接敲a后回车，调用的是 a.__repr__() ,给机器看的
```


2. todo 列表推导 ?  
```
headers = {
	'age': 20,
	'name': 'liwenkang' 
}

kvs = headers.items()
items = []
for k, v in kvs:
	item = '{}: {}\r\n'.format(k, v)
	items.append(item)
header += ''.join(items)

等价于下面

header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])

header = "
	age: 20
	name: liwenkang
"

特殊的 enumerate ?

for i, m in enumerate(headers):
	log('i', i,'index')
	log('m', m,'key') 
	log('models.get(m)', models.get(m),'value')

# 另外的探索 ==>

from utils import test_log as log

data = [
	{
	    'age': 10,
	    'name': 'liwenkang' 
	},
	{
        'age': 20,
        'name': 'huasheng'
	}
]

# 可以看出此处的 k , v 分别对应的是对象中不同的 key 值(age 还有 name)
# 如果只有一个 k 时, k 对应的是列表中的每一项
	properties1 = '\n'.join(['{}: ({})'.format(k, v) for k, v in data])
	properties2 = '\n'.join(['{}'.format(k) for k in data])

	log('properties1: ',properties1)
	# <properties:age: (name) 
	age: (name)>

	log('properties2: ',properties2)
    # <properties:{'age': 10, 'name': 'liwenkang'}
	{'age': 20, 'name': 'huasheng'}>

	tuidao(data)
```
3. 关于编码的问题
	urllib.parse.unquote 会将字符中的 %xx 这种编码转换为对应的实体字符,比如 %20 对应一个空格
```
import urllib.parse

log(urllib.parse.unquote('El%20Ni%C3%B1o'))

输出为: El Niño	
```
	其它编码问题可以参考
	
	http://www.ruanyifeng.com/blog/2010/02/url_encoding.html 				
	
	https://docs.python.org/3.2/library/urllib.parse.html   



4. url分解   
	
```
import urllib.parse   

result = urllib.parse.urlparse('http://www.aspxfans.com:8080/news/index.asp?boardID=5&ID=24618&page=1#name') 

print(result.path)     

ParseResult( 
	scheme='http',
	netloc='www.aspxfans.com:8080',
	path='/news/index.asp', 
	params='', 
	query='boardID=5&ID=24618&page=1', 
	fragment='name' 
)
```
```
urllib.parse.urlparse将传入的url解析成了六大部分，是一个元组，含协议名称、域名、路径等   

	Index  		Index	Value  								Value if not present 
	scheme     	0      	URL scheme specifier               	scheme parameter 
	netloc     	1      	Network location part              	empty string 
	path       	2      	Hierarchical path                  	empty string 
	params     	3      	Parameters for last path element   	empty string 
	query      	4      	Query component                     empty string 
	fragment   	5      	Fragment identifier                	empty string
```
	参考内容: 
	http://blog.csdn.net/ergouge/article/details/8185219
	http://blog.csdn.net/u014421556/article/details/51671353

5. 什么是实例,什么是类?
```
# get_no_of_instances() 这个方法既可以在类(ik1)中运行,也可以在实例中(Kls)运行 

def get_no_of_instances(cls_obj):
	return cls_obj.no_inst 

class Kls(object):
	no_inst = 0 

	def __init__(self): 
		Kls.no_inst = Kls.no_inst + 1

ik1 = Kls()															
ik2 = Kls()
# Kls 就是一个实例
# ik1 就是一个类
```

6. 类的实例方法，静态方法，类方法 辨析?

```
1.实例方法:第一个参数是self,表示该类的一个实例,所以该方法只能是实例才能调用 

在 def save(self) 中 
models = self.all() 等价于 models = self.__class__.all() 
实例也可以调用类方法


2. 静态方法: 没有第一个参数,和类是没有联系的(谁定义了这个类,谁就可以用这个静态方法),为了好看,可以写在类里面,此时必须通过类来调用.(一般情况下用不到),参数中不需要传递类名


3. 类方法: 第一个参数是cls,是类

@classmethod 表示接下来的是一个类方法

生成对象的东西都必然是类方法,不需要实例也可以调用

Todo.all() Todo 是类名, all() 是一个类方法, 不需要任何实例就可以调用, 用来生成实例 , 参数中需要隐式地传递类名, 也就是说 Todo 当作 class 函数传入了,所以 Todo.all() 等价于 Todo.all(Todo)  
```

	参考
	http://blog.csdn.net/a447685024/article/details/52424481 		
	http://www.cnblogs.com/hopeworld/archive/2011/08/16/2140145.html   


7. *args 和**kwargs ?

```
当函数的参数不确定时，可以使用*args 和**kwargs 
*args 没有 key 值，**kwargs 有 key 值 

*args 表示多个剩余参数()，它是一个tuple 
**kwargs表示关键字参数，它是一个dict 

同时使用*args和**kwargs时，必须*args 在**kwargs前 
在打 log 的时候,一定要注意最后才打"字典"
```

8. 文件操作 
```
w+ 	可读可写，如果文件存在，则覆盖整个文件，不存在则创建   
a+ 	追加模式
r	只读模式
with open(path, 'w+', encoding='utf-8') as f:
  f.write(s)
```
	参考
	http://www.cnblogs.com/yangshl/p/6285942.html
