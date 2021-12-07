# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from urllib.parse import urlparse

import pytesseract
import requests
import json

from six import BytesIO
from PIL import Image
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from .setting_db import MongoDB
from .chaojiying import Chaojiying

pic_id = ''


class TeamProjectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TeamProjectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


#######
PROXY_POOL_URL = 'http://127.0.0.1:5000/one'


class RandomProxyMiddleware(object):
    # 动态设置ip代理

    def process_request(self, request, spider):
        h = request.url.split(':')[0]
        if h == 'https':
            proxy = requests.get(PROXY_POOL_URL + "/https").text
            print(proxy)
            if proxy is not None:
                ip = json.loads(proxy)['proxy']
                request.meta["proxy"] = 'https://' + str(ip)
                print(str(ip))
        else:
            proxy = requests.get(PROXY_POOL_URL + "/http").text
            if proxy is not None:
                ip = json.loads(proxy)['proxy']
                request.meta["proxy"] = 'http://' + str(ip)
                print(str(ip))


class SeleniumMiddleware(object):

    def __init__(self):
        self.mongodb = MongoDB()
        self.chaojiying = Chaojiying('shenmegui1987', '1565244084', '924600')

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        # when the spider created
        self.chrome = webdriver.Chrome()

    def spider_closed(self, spider):
        self.chrome.quit()

    def click(self, username, password):
        time.sleep(1)
        wait = WebDriverWait(self.chrome, 5, 0.5)
        user_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][1]/div/div/input')))  # 根据具体情况改
        pwd_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][2]/div/div/input')))  # 根据具体情况改
        btn = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][3]/div/button')))  # 根据具体情况改
        user_input.send_keys(username)
        pwd_input.send_keys(password)
        time.sleep(1)
        btn.click()
        time.sleep(10)

    def write(self, username, password):
        wait = WebDriverWait(self.chrome, 5, 0.5)
        user_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][1]/div/div/input')))  # 根据具体情况改
        pwd_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][2]/div/div/input')))  # 根据具体情况改
        user_input.send_keys(username)
        pwd_input.send_keys(password)
        time.sleep(1)

    # 获取滑动验证图片位置
    def get_position(self, img_label):
        location = img_label.location
        size = img_label.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (left, top, right, bottom)

    # 获取浏览器截图
    def get_screenshot(self):
        screenshot = self.chrome.get_screenshot_as_png()
        f = BytesIO()
        f.write(screenshot)
        return Image.open(f)

    # 对比上两张图算位置
    def get_position_scale(self, screen_shot):
        height = self.chrome.execute_script('return document.documentElement.clientHeight')
        width = self.chrome.execute_script('return document.documentElement.clientWidth')
        x_scale = screen_shot.size[0] / (width + 10)
        y_scale = screen_shot.size[1] / (height)
        return (x_scale, y_scale)

    # 获取有缺口的滑动图片
    def get_slideimg_screenshot(self, screenshot, position, scale):
        x_scale, y_scale = scale
        position = [position[0] * x_scale, position[1] * y_scale, position[2] * x_scale, position[3] * y_scale]
        return screenshot.crop(position)

    # 比较原始和缺口图
    def compare_pixel(self, img1, img2, x, y):
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) <= threshold:
            if abs(pixel1[1] - pixel2[1]) <= threshold:
                if abs(pixel1[2] - pixel2[2]) <= threshold:
                    return True
        return False

    def compare(self, full_img, slice_img):
        left = 0
        for i in range(full_img.size[0]):
            for j in range(full_img.size[1]):
                if not self.compare_pixel(full_img, slice_img, i, j):
                    return i - 15
        return left - 15

    # 计算滑动轨迹
    def get_track(self, distance):
        '''
        拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
        匀变速运动基本公式：
        ①v=v0+at
        ②s=v0t+½at²
        ③v²-v0²=2as
        :param distance: 需要移动的距离
        :return: 存放每0.3秒移动的距离
        '''
        # 初速度
        v = 10
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 1
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 4 / 5

        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 2
            else:
                a = -3

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        return tracks

    # 移动
    def move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        """
        # 单纯的匀变速直线运动
        # ActionChains(browser).click_and_hold(slider).perform()
        # for x in tracks:
        #     ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # time.sleep(0.5)
        # ActionChains(browser).release().perform()

        # 走走停停式运动
        action_chains = webdriver.ActionChains(self.chrome)
        # 点击，准备拖拽
        action_chains.click_and_hold(slider)
        # 拖动次数，二到三次
        for x in tracks:
            dragCount = random.randint(2, 3)
            if dragCount == 2:
                # 总误差值
                sumOffsetx = random.randint(-15, 15)
                action_chains.move_by_offset(x + sumOffsetx, 0)
                # 暂停一会
                action_chains.pause(random.uniform(0.6, 0.9))
                # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
                action_chains.move_by_offset(-sumOffsetx, 0)
            elif dragCount == 3:
                # 总误差值
                sumOffsetx = random.randint(-15, 15)
                action_chains.move_by_offset(x + sumOffsetx, 0)
                # 暂停一会
                action_chains.pause(random.uniform(0.6, 0.9))

                # 已修正误差的和
                fixedOffsetX = 0
                # 第一次修正误差
                if sumOffsetx < 0:
                    offsetx = random.randint(sumOffsetx, 0)
                else:
                    offsetx = random.randint(0, sumOffsetx)

                fixedOffsetX = fixedOffsetX + offsetx
                action_chains.move_by_offset(-offsetx, 0)
                action_chains.pause(random.uniform(0.6, 0.9))

                # 最后一次修正误差
                action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
                action_chains.pause(random.uniform(0.6, 0.9))

            else:
                raise Exception("莫不是系统出现了问题？!")

        # 参考action_chains.drag_and_drop_by_offset()
        action_chains.release()
        action_chains.perform()

    def run(self):
        slice_img_label = WebDriverWait(self.chrome, 5, 0.5).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.geetest_slicebg')))  # 找到滑动图片标签，需修改
        self.chrome.execute_script(
            "document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'none'")  # 将小块隐藏，需修改
        full_img_label = self.chrome.find_element(By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg')  # 原始图片的标签，需修改
        position = self.get_position(slice_img_label)  # 获取滑动验证图片位置
        screenshot = self.get_screenshot()  # 获取浏览器截图
        position_scale = self.get_position_scale(screenshot)  # 对比上两张图算位置
        slice_img = self.get_slideimg_screenshot(screenshot, position, position_scale)  # 获取有缺口的滑动图片
        self.chrome.execute_script(
            "document.getElementsByClassName('geetest_canvas_fullbg')[0].style['display'] = 'block'")  # 在浏览器中显示原图，需修改
        screenshot = self.get_screenshot()  # 获取整个浏览器图片
        full_img = self.get_slideimg_screenshot(screenshot, position, position_scale)  # 截取滑动验证原图
        self.chrome.execute_script(
            "document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'block'")  # 将小块重新显示，需修改
        left = self.compare(full_img, slice_img)  # 比较原始和缺口图
        left = left / position_scale[0]  # 将该位置还原为浏览器中的位置
        slide_btn = self.chrome.find_element(By.CSS_SELECTOR, '.geetest_slider_button')  # 获取滑动按钮，需修改
        track = self.get_track(left)  # 计算滑动轨迹
        self.move_to_gap(slide_btn, track)  # 移动

    def detect_slide(self):
        if self.chrome.current_url == "https://captcha1.scrape.center/success":
            print("success")
        else:
            time.sleep(1)
            fresh = self.chrome.find_element(By.CSS_SELECTOR, "a.geetest_refresh_1")
            fresh.click()
            self.chrome.find_element(By.CSS_SELECTOR, "canvas.geetest_canvas_slice").click()
            time.sleep(5)
            self.run()
            self.detect_slide()

    def get_code(self, code_img):
        position = self.get_position(code_img)  # 获取验证图片位置
        screenshot = self.get_screenshot()  # 获取浏览器截图
        position_scale = self.get_position_scale(screenshot)  # 对比上两张图算位置
        code_img_final = self.get_slideimg_screenshot(screenshot, position, position_scale)  # 得到验证码图片
        # 灰度处理
        im = code_img_final.convert('L')
        # 设置二值化的阈值
        threshold = 170
        t = []
        for i in range(256):
            if i < threshold:
                t.append(0)
            else:
                t.append(1)
        # 通过表格转换成二进制图片，1的作用是白色，0就是黑色
        im = im.point(t, "1")
        return pytesseract.image_to_string(im).replace(' ', '')

    def input_code(self, code_img, code_input):
        code = self.get_code(code_img)
        code_input.clear()
        time.sleep(1)
        code_input.send_keys(code)
        time.sleep(1)
        btn = WebDriverWait(self.chrome, 5, 0.5).until(EC.presence_of_element_located(
            (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][4]/div/button')))  # 根据具体情况改
        btn.click()
        windows = self.chrome.window_handles
        self.chrome.switch_to.window(windows[-1])

    def detect_image(self, code_img, code_input):
        if self.chrome.current_url == "https://captcha7.scrape.center/success":
            print('success')
        else:
            code_img.click()
            self.input_code(code_img, code_input)
            self.detect_image(code_img, code_input)

    def pick_code(self):
        global pic_id
        time.sleep(5)
        ele = self.chrome.find_elements(By.CSS_SELECTOR, 'img.geetest_item_img')
        if len(ele) == 1:
            pick_img_label = self.chrome.find_element(By.CSS_SELECTOR, 'img.geetest_item_img')  # 获取点触图片标签
            src = pick_img_label.get_attribute('src')  # 获取点触图片链接
            img_content = requests.get(src).content  # 获取图片二进制内容
            f = BytesIO()
            f.write(img_content)
            img0 = Image.open(f)
            scale = [pick_img_label.size['width'] / img0.size[0],
                     pick_img_label.size['height'] / img0.size[1]]  # 获取图片与浏览器该标签大小的比例
            cjy = self.chaojiying
            result = cjy.PostPic(img_content, '9005')  # 发送图片并获取结果
            if result['err_no'] == 0:
                position = result['pic_str'].split('|')
                position = [[int(j) for j in i.split(',')] for i in position]
                for items in position:  # 模拟点击
                    webdriver.ActionChains(self.chrome).move_to_element_with_offset(pick_img_label, items[0] * scale[0],
                                                                                    items[1] * scale[
                                                                                        1]).click().perform()
                    time.sleep(1)
            # 点击登录
            certern_btn = self.chrome.find_element(By.CSS_SELECTOR, 'div.geetest_commit_tip')
            time.sleep(1)
            certern_btn.click()

    # 检测是否登陆成功
    def detect_word(self):
        current = self.chrome.current_url
        if current == 'https://captcha3.scrape.center/success':
            print('登陆成功')
        else:
            self.chaojiying.ReportError(pic_id)
            self.pick_code()
            self.detect_word()

    # request the website
    def process_request(self, request, spider):
        # 通过请求连接中包含的域名来分类，看通过哪种验证码破解方式
        # 滑动验证 如：https://captcha1.scrape.center/
        if urlparse(request.url).netloc in self.mongodb.get_all_by_condition(
                'slide'):  # 通过spider的名字：spider.name == 'slide':
            self.chrome.get(request.url)
            self.click('admin', 'admin')
            time.sleep(2)
            self.detect_slide()
            html = self.chrome.page_source
            return HtmlResponse(url=self.chrome.current_url, body=html.encode('utf-8'))

        # 图像验证 如：https://captcha7.scrape.center/
        elif urlparse(request.url).netloc in self.mongodb.get_all_by_condition('image'):  # spider.name == 'image':
            self.chrome.get(request.url)
            self.write('admin', 'admin')
            time.sleep(2)
            code_input = WebDriverWait(self.chrome, 5, 0.5).until(EC.presence_of_element_located(
                (By.XPATH,
                 '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][3]/div/div/div/div/input')))  # 根据具体情况改

            code_img = self.chrome.find_element(By.ID, 'captcha')

            self.detect_image(code_img, code_input)

            html = self.chrome.page_source
            return HtmlResponse(url=self.chrome.current_url, body=html.encode('utf-8'))

        # 语序验证 如：https://captcha3.scrape.center/
        elif urlparse(request.url).netloc in self.mongodb.get_all_by_condition(
                'word_order'):  # spider.name == 'word_order'
            self.chrome.get(request.url)
            self.click('admin', 'admin')
            self.pick_code()
            time.sleep(3)
            self.detect_word()
            return HtmlResponse(url=self.chrome.current_url)


class SouhuSeleniumMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        # when the spider created
        self.chrome = webdriver.Chrome()

    def spider_closed(self, spider):
        self.chrome.quit()

    # request the website
    def process_request(self, request, spider):
        if request.url != 'https://news.sohu.com/':
            time.sleep(2)
            self.chrome.get(request.url)
            WebDriverWait(self.chrome, 30, 1).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="read-num"]/em')))
            return HtmlResponse(url=request.url, body=self.chrome.page_source, request=request, encoding='utf-8',
                            status=200)
