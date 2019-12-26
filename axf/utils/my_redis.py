
from django_redis import get_redis_connection


class MyRedis():

    def __init__(self):
        self.conn = get_redis_connection()

    def hset(self, key1, fields, value):
        # 使用hash散列
        self.conn.hset(key1, fields, value)

    def hget(self, key1, fields):
        return self.conn.hget(key1, fields)

# 单例模式
# 因为模块在第一次导入时，会生成 .pyc 文件，当第二次导入时，就会直接加载 .pyc 文件，而不会再次执行模块代码。
# 因此，只需把相关的函数和数据定义在一个模块中，就可以获得一个单例对象了
myredis = MyRedis()
