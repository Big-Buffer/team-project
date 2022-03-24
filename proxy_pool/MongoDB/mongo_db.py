import pymongo
from pymongo.errors import DuplicateKeyError


class MongoDB:

    def __init__(self):
        # 连接mongodb服务器,先启动mongodb服务器和客户端
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        # 连接ProxiesPool数据库，可以先在mongodb中创建ProxiesPool数据库，集合插入数据时会自动创建
        self.db = self.client['myDB']
        # 连接ProxiesPool数据库下的proxies集合
        self.proxies = self.db['proxypool']
        # 给proxy字段创建一个新的索引，加快查询的速度
        self.proxies.create_index('proxy', unique=True)

    # 插入数据
    def insert(self, proxy):
        try:
            self.proxies.insert_one(proxy)
            print("插入成功:{}".format(proxy))
        except DuplicateKeyError:
            pass

    # 删除数据
    def delete(self, conditions):
        self.proxies.find_one_and_delete(conditions)
        print("删除成功:{}".format(conditions))

    # 更新数据
    def update(self, conditions, values):
        self.proxies.update_one(conditions, {"$set": values})
        print("更新成功:{},{}".format(conditions, values))

    # 取出所有的数据，count是check_crawl_ip获取到的ip代理数量
    def get(self, count, conditions=None):
        conditions = conditions if conditions else {}
        count = int(count)
        items = self.proxies.find(conditions)  # conditions=None,即默认查找所有的proxies集合下所有的文档
        items = list(items)
        return items

    # 取出所有http类型的数据，count是check_crawl_ip获取到的ip代理数量
    def get_http(self):
        items = self.proxies.find({'type': 'http'})
        items = list(items)
        return items

    # 取出所有https类型的数据，count是check_crawl_ip获取到的ip代理数量
    def get_https(self):
        items = self.proxies.find({'type': 'http'})
        items = list(items)
        return items

    # 统计数据库中代理个数
    def get_count(self):
        count = 0
        for i in self.proxies.find({}):
            count += 1
        return count  # {}条件为空，即统计全部数据

    def get_all(self):
        proxy_list = []
        for i in self.proxies.find():
            proxy_list.append(i)
        return proxy_list


if __name__ == '__main__':
    mongodb = MongoDB()
    print(mongodb.get_count())
