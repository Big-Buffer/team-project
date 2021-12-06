import pymongo
from pymongo.errors import DuplicateKeyError


class MongoDB(object):

    def __init__(self):
        self.client = pymongo.MongoClient(host="localhost", port=27017)
        # TODO 更改相应的db
        self.db = self.client['myDB']
        self.domain = self.db['domain']
        self.domain.create_index('domain', unique=True)

    def insert(self, domain):
        try:
            self.domain.insert_one(domain)
            print("插入成功:{}".format(domain))
        except DuplicateKeyError:
            pass

    def delete(self, conditions):
        self.domain.remove(conditions)
        print("删除成功:{}".format(conditions))

    def update(self, conditions, values):
        self.domain.update(conditions, {"$set": values})
        print("更新成功:{},{}".format(conditions, values))

    def get_count(self):
        return self.domain.count({})  # {}条件为空，即统计全部数据

    def get_all_by_condition(self, condition):
        domain_list = []
        for i in self.domain.find({'type': condition}):
            domain_list.append(i['domain'])
        return domain_list

    def get_all(self):
        domain_list = []
        for i in self.domain.find():
            domain_list.append(i)
        return domain_list


if __name__ == '__main__':
    mongodb = MongoDB()
    mongodb.insert({'domain': 'passport.bilibili.com', 'type': 'word_order'})  # 1,3,7

    domains = mongodb.get_all_by_condition('image')
    print(domains)
    print('captcha1.scrape.center' in domains)
    print(mongodb.get_all())
