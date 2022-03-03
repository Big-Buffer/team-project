import time
import json
import logging


class Log():
    CUR_LOG = {
        'time': {
            'start_time': 0,  # 开始时间
            'end_time': 0,  # 结束时间
            'consume_time': 0,  # 共耗时
        },
        # 'spider1': {
        #     'request_sucess': 0,  # 请求成功(分页数)
        #     'request_error': 0,  # 请求错误
        #     'data_crawl': 0,  # 爬取到的数量
        #     'data_new': 0,  # 获取到的新数据
        #     'data_error': 0,  # 数据出错
        #     'data_illegal': 0,  # 数据格式错误
        #     'data_repeat': 0,  # 重复的数据
        #     'db_error': 0,  # 数据库系统错误
        #     'db_operate': 0,  # 数据库操作返回错误
        # },
    }
    logger = logging.getLogger('stat')

    def __init__(self, name=None):
        if name:
            self.CUR_LOG[name] = {}
            self.CUR_LOG[name]['request_success'] = 0
            self.CUR_LOG[name]['request_error'] = 0
            self.CUR_LOG[name]['data_crawl'] = 0
            self.CUR_LOG[name]['data_new'] = 0
            self.CUR_LOG[name]['data_error'] = 0
            self.CUR_LOG[name]['data_illegal'] = 0
            self.CUR_LOG[name]['data_repeat'] = 0
            self.CUR_LOG[name]['db_error'] = 0
            self.CUR_LOG[name]['db_operate'] = 0

    def start_time(self):
        self.CUR_LOG['time']['start_time'] = time.time()
        self.logger.warning('{: <6s}'.format('all') \
                            + '{: <17s} '.format('[start_time]') \
                            + time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime()))

    def end_time(self):
        self.CUR_LOG['time']['end_time'] = time.time()
        self.CUR_LOG['time']['consume_time'] \
            = self.CUR_LOG['time']['end_time'] \
              - self.CUR_LOG['time']['start_time']

        self.CUR_LOG['time']['start_time'] \
            = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(self.CUR_LOG['time']['start_time']))
        self.CUR_LOG['time']['end_time'] \
            = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(self.CUR_LOG['time']['end_time']))

        hours = '{:0>2s}'.format(str(int(self.CUR_LOG['time']['consume_time'] // 3600)))
        minutes = '{:0>2s}'.format(str(int((self.CUR_LOG['time']['consume_time'] // 60) % 60)))
        seconds = '{:0>2s}'.format(str(int(self.CUR_LOG['time']['consume_time'] % 60)))
        self.CUR_LOG['time']['consume_time'] = hours + ':' + minutes + ':' + seconds
        self.logger.warning('{: <6s}'.format('all') \
                            + '{: <17s} '.format('[end_time]') \
                            + time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime()))
        self.logger.warning('{: <6s}'.format('all') \
                            + '{: <17s} '.format('[consume_time]') \
                            + self.CUR_LOG['time']['consume_time'])

    def add_request_success(self, name, msg='', num=1):
        self.CUR_LOG[name]['request_success'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[request_success]') \
                            + str(msg).replace('\n', ' '))

    def add_request_error(self, name, msg='', num=1):
        self.CUR_LOG[name]['request_error'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[request_error]') \
                            + str(msg).replace('\n', ' '))

    def add_data_crawl(self, name, msg='', num=1):
        self.CUR_LOG[name]['data_crawl'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[data_crawl]') \
                            + str(num))

    def add_data_new(self, name, msg='', num=1):
        self.CUR_LOG[name]['data_new'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[data_new]') \
                            + str(msg).replace('\n', ' '))

    def add_data_error(self, name, msg='', num=1):
        self.CUR_LOG[name]['data_error'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[data_error]') \
                            + str(msg).replace('\n', ' '))

    def add_data_illegal(self, name, msg='', num=1):
        self.CUR_LOG[name]['data_illegal'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[data_illegal]') \
                            + str(msg).replace('\n', ' '))

    def add_data_repeat(self, name, msg='', num=1):
        self.CUR_LOG[name]['data_repeat'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[data_repeat]') \
                            + str(msg).replace('\n', ' '))

    def add_db_error(self, name, msg='', num=1):
        self.CUR_LOG[name]['db_error'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[db_error]') \
                            + str(msg).replace('\n', ' '))

    def add_db_operate(self, name, msg='', num=1):
        self.CUR_LOG[name]['db_operate'] += num
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[db_operate]') \
                            + str(msg).replace('\n', ' '))

    def json_display(self, name=None):
        if name:
            self.logger.warning('{: <6s}'.format(name) \
                                + '{: <17s} '.format('[json_display]') \
                                + str(self.CUR_LOG[name]))
        else:
            self.logger.warning('{: <6s}'.format('all') \
                                + '{: <17s} \n'.format('[json_display]') \
                                + str(json.dumps(self.CUR_LOG, indent=4)))

    def crawled_display(self, name, msg=''):
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[crawled_number]') \
                            + str(msg))

    def open_display(self, name, msg=''):
        self.logger.warning('{: <6s}'.format(name) \
                            + '{: <17s} '.format('[opened]'))
