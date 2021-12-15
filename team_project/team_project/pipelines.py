import json
import csv

import requests

class TeamProjectPipeline:

    def __init__(self):
        self.fp = open("data/result.json", "w", encoding="utf-8")

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.fp.write(item_json + '\n', )
        return item

    def close_spider(self, spider):
        self.fp.close()


class RmrbPipeline:
    def open_spider(self, spider):
        self.f = open('data/rmrb.csv', 'w', encoding='utf-8', newline='')

    def process_item(self, item, spider):
        writer = csv.DictWriter(self.f, ['author', 'title'])
        writer.writeheader()
        writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.f.close()


class SouhuPipeline:
    def open_spider(self, spider):
        self.f = open('data/souhu.csv', 'w', encoding='utf-8', newline='')

    def process_item(self, item, spider):
        writer = csv.DictWriter(self.f, ['title', 'content', 'reading'])
        writer.writeheader()
        writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.f.close()


class SinaPipeline:
    def open_spider(self, spider):
        self.f = open('data/sina.csv', 'w', encoding='utf-8', newline='')

    def process_item(self, item, spider):
        writer = csv.DictWriter(self.f, ['head', 'content'])
        writer.writeheader()
        writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.f.close()


class NewsPipeline:
    def open_spider(self, spider):
        self.f = open('data/news.csv', 'w', encoding='utf-8', newline='')

    def process_item(self, item, spider):
        writer = csv.DictWriter(self.f, ['title', 'content'])
        writer.writeheader()
        writer.writerow(dict(item))
        return item

    def close_spider(self, spider):
        self.f.close()


class TestPipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # data = json.dumps(dict(item), ensure_ascii=False)
        d = str(item)
        print('我们的item=======>')
        print(d)
        print('<=======')
        data = {'searchValue': '1', 'createBy': 'chen', 'data': d, 'remark': '无'}
        res = requests.post(url="http://47.98.127.15:8089/pyData/add", json=data, headers={'Content-Type': 'application/json'})
        print('返回结果================>')
        print(res.text)
        print("<==================")
        return item

    def close_spider(self, spider):
        pass


if __name__ == '__main__':
    open('data/rmrb.csv', 'w', encoding='utf-8', newline='')
