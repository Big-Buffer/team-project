import json
import csv


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


if __name__ == '__main__':
    open('data/rmrb.csv', 'w', encoding='utf-8', newline='')
