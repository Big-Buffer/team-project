# import random
# import time
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from PIL import Image
# from six import BytesIO
#
#
# # 访问页面
# def get_url(url, user, password):
#     browser = webdriver.Chrome()
#     browser.get(url)
#     time.sleep(1)
#     wait = WebDriverWait(browser, 5, 0.5)
#     user_input = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][1]/div/div/input')))  # 根据具体情况改
#     pwd_input = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][2]/div/div/input')))  # 根据具体情况改
#     btn = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//form[@class=\'el-form\']/div[@class=\'el-form-item\'][3]/div/button')))  # 根据具体情况改
#     user_input.send_keys(user)
#     pwd_input.send_keys(password)
#     time.sleep(1)
#     btn.click()
#     time.sleep(10)
#     return browser
#
#
# # 获取滑动验证图片位置
# def get_position(img_label):
#     location = img_label.location
#     size = img_label.size
#     top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
#     return (left, top, right, bottom)
#
#
# # 获取浏览器截图
# def get_screenshot(browser):
#     screenshot = browser.get_screenshot_as_png()
#     f = BytesIO()
#     f.write(screenshot)
#     return Image.open(f)
#
#
# # 对比上两张图算位置
# def get_position_scale(browser, screen_shot):
#     height = browser.execute_script('return document.documentElement.clientHeight')
#     width = browser.execute_script('return document.documentElement.clientWidth')
#     x_scale = screen_shot.size[0] / (width + 10)
#     y_scale = screen_shot.size[1] / (height)
#     return (x_scale, y_scale)
#
#
# # 获取有缺口的滑动图片
# def get_slideimg_screenshot(screenshot, position, scale):
#     x_scale, y_scale = scale
#     position = [position[0] * x_scale, position[1] * y_scale, position[2] * x_scale, position[3] * y_scale]
#     return screenshot.crop(position)
#
#
# # 比较原始和缺口图
# def compare_pixel(img1, img2, x, y):
#     pixel1 = img1.load()[x, y]
#     pixel2 = img2.load()[x, y]
#     threshold = 60
#     if abs(pixel1[0] - pixel2[0]) <= threshold:
#         if abs(pixel1[1] - pixel2[1]) <= threshold:
#             if abs(pixel1[2] - pixel2[2]) <= threshold:
#                 return True
#     return False
#
#
# def compare(full_img, slice_img):
#     left = 0
#     for i in range(full_img.size[0]):
#         for j in range(full_img.size[1]):
#             if not compare_pixel(full_img, slice_img, i, j):
#                 return i-7
#     return left-7
#
#
# # 计算滑动轨迹
# def get_track(distance):
#     '''
#     拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
#     匀变速运动基本公式：
#     ①v=v0+at
#     ②s=v0t+½at²
#     ③v²-v0²=2as
#     :param distance: 需要移动的距离
#     :return: 存放每0.3秒移动的距离
#     '''
#     # 初速度
#     v = 10
#     # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
#     t = 1
#     # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
#     tracks = []
#     # 当前的位移
#     current = 0
#     # 到达mid值开始减速
#     mid = distance * 4 / 5
#
#     while current < distance:
#         if current < mid:
#             # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
#             a = 2
#         else:
#             a = -3
#
#         # 初速度
#         v0 = v
#         # 0.2秒时间内的位移
#         s = v0 * t + 0.5 * a * (t ** 2)
#         # 当前的位置
#         current += s
#         # 添加到轨迹列表
#         tracks.append(round(s))
#
#         # 速度已经达到v,该速度作为下次的初速度
#         v = v0 + a * t
#     return tracks
#
#
# # 移动
# def move_to_gap(browser, slider, tracks):
#     """
#     拖动滑块到缺口处
#     :param slider: 滑块
#     :param tracks: 轨迹
#     :return:
#     """
#     # ActionChains(browser).click_and_hold(slider).perform()
#     # for x in tracks:
#     #     ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
#     # time.sleep(0.5)
#     # ActionChains(browser).release().perform()
#
#     action_chains = webdriver.ActionChains(browser)
#     # 点击，准备拖拽
#     action_chains.click_and_hold(slider)
#     # 拖动次数，二到三次
#     for x in tracks:
#         dragCount = random.randint(2, 3)
#         if dragCount == 2:
#             # 总误差值
#             sumOffsetx = random.randint(-15, 15)
#             action_chains.move_by_offset(x + sumOffsetx, 0)
#             # 暂停一会
#             action_chains.pause(random.uniform(0.6, 0.9))
#             # 修正误差，防止被检测为机器人，出现图片被怪物吃掉了等验证失败的情况
#             action_chains.move_by_offset(-sumOffsetx, 0)
#         elif dragCount == 3:
#             # 总误差值
#             sumOffsetx = random.randint(-15, 15)
#             action_chains.move_by_offset(x + sumOffsetx, 0)
#             # 暂停一会
#             action_chains.pause(random.uniform(0.6, 0.9))
#
#             # 已修正误差的和
#             fixedOffsetX = 0
#             # 第一次修正误差
#             if sumOffsetx < 0:
#                 offsetx = random.randint(sumOffsetx, 0)
#             else:
#                 offsetx = random.randint(0, sumOffsetx)
#
#             fixedOffsetX = fixedOffsetX + offsetx
#             action_chains.move_by_offset(-offsetx, 0)
#             action_chains.pause(random.uniform(0.6, 0.9))
#
#             # 最后一次修正误差
#             action_chains.move_by_offset(-sumOffsetx + fixedOffsetX, 0)
#             action_chains.pause(random.uniform(0.6, 0.9))
#
#         else:
#             raise Exception("莫不是系统出现了问题？!")
#
#     # 参考action_chains.drag_and_drop_by_offset()
#     action_chains.release()
#     action_chains.perform()
#
#
# def run():
#     slice_img_label = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located(
#         (By.CSS_SELECTOR, 'div.geetest_slicebg')))  # 找到滑动图片标签，需修改
#     browser.execute_script(
#         "document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'none'")  # 将小块隐藏，需修改
#     full_img_label = browser.find_element(By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg')  # 原始图片的标签，需修改
#     position = get_position(slice_img_label)  # 获取滑动验证图片位置
#     screenshot = get_screenshot(browser)  # 获取浏览器截图
#     position_scale = get_position_scale(browser, screenshot)  # 对比上两张图算位置
#     slice_img = get_slideimg_screenshot(screenshot, position, position_scale)  # 获取有缺口的滑动图片
#     browser.execute_script(
#         "document.getElementsByClassName('geetest_canvas_fullbg')[0].style['display'] = 'block'")  # 在浏览器中显示原图，需修改
#     screenshot = get_screenshot(browser)  # 获取整个浏览器图片
#     full_img = get_slideimg_screenshot(screenshot, position, position_scale)  # 截取滑动验证原图
#     browser.execute_script(
#         "document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'block'")  # 将小块重新显示，需修改
#     left = compare(full_img, slice_img)  # 比较原始和缺口图
#     left = left / position_scale[0]  # 将该位置还原为浏览器中的位置
#     slide_btn = browser.find_element(By.CSS_SELECTOR, '.geetest_slider_button')  # 获取滑动按钮，需修改
#     track = get_track(left)  # 计算滑动轨迹
#     move_to_gap(browser, slide_btn, track)  # 移动
#
#
# # 主函数，使用时括号中定位均需修改
# if __name__ == '__main__':
#     browser = get_url('https://captcha1.scrape.center/', 'admin', 'admin')  # 网址，后两项为用户名和密码，需修改
#     time.sleep(2)
#     run()
#     time.sleep(1)
#     windows = browser.window_handles
#     browser.switch_to.window(windows[-1])
#     try:
#         success = browser.find_element(By.CSS_SELECTOR, 'h2.text-center')  # 获取显示结果的标签，需修改
#         if success.text == "登录成功":
#             login_btn = browser.find_element(By.CSS_SELECTOR, 'button.el-button')  # 如果验证成功，则点击登录按钮，需修改
#             login_btn.click()
#             print('success')
#         else:
#             print('fail')
#     except:
#         print("failed")
import scrapy
from scrapy_redis.spiders import RedisSpider


class SlideSpider(RedisSpider):
    name = 'slide'
    # start_urls = [
    #     'https://captcha1.scrape.center/'
    # ]
    redis_key = "slide:start_urls"

    def parse(self, response):
        pass

