#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ : stray_camel
# __description__ : 重构 djangorestframework-jwt
# __REFERENCES__ : [https://github.com/jpadilla/django-rest-framework-jwt/, https://www.cnblogs.com/ruhai/p/11311852.html]
# __date__: 2020/09/28 14

"""
JWT和token
相同：都是访问资源的令牌， 都可以记录用户信息，都是只有验证成功后
区别：​服务端验证客户端发来的token信息要进行数据的查询操作；JWT验证客户端发来的token信息就不用， 在服务端使用密钥校验就可以，不用数据库的查询。
Token 访问资源的令牌

验证流程：

1. 把用户的用户名和密码发到后端
2. 后端进行校验，校验成功会生成token, 把token发送给客户端
3. 客户端自己保存token, 再次请求就要在Http协议的请求头中带着token去访问服务端，和在服务端保存的token信息进行比对校验。
1
2
3
特点：

​ 客户端每次都要携带token, 客户端的内容比较多


JWT

概念: JSON WEB TOKEN 的简写。可以使用在RESTFUL接口定义， 也可以使用在普通的web

组成：
header、payload、签证

验证流程：

1. 在头部信息中声明加密算法和常量， 然后把header使用json转化为字符串
2. 在载荷中声明用户信息，同时还有一些其他的内容；再次使用json 把载荷部分进行转化，转化为字符串
3. 使用在header中声明的加密算法和每个项目随机生成的secret来进行加密， 把第一步分字符串和第二部分的字符串进行加密， 生成新的字符串。词字符串是独一无二的。
4. 解密的时候，只要客户端带着JWT来发起请求，服务端就直接使用secret进行解密。
1
2
3
4
特点：

1. 三部分组成，每一部分都进行字符串的转化
2. 解密的时候没有使用数据库，仅仅使用的是secret进行解密。
3. JWT的secret千万不能泄密！！！
"""
"""
1) jwt = base64(头部).base64(载荷).hash256(base64(头部).base(载荷).密钥)
2) base64是可逆的算法、hash256是不可逆的算法
3) 密钥是固定的字符串，保存在服务器
"""