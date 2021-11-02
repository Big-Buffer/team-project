from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
from six import BytesIO
import time
from selenium.webdriver import ActionChains
#访问页面
def get_url(url,user,password):
    browser = webdriver.Chrome()
    browser.get(url)
    browser.maximize_window()
    wait = WebDriverWait(browser,10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_radar_btn')))
    user_input = browser.find_element_by_id('username')
    pwd_input = browser.find_element_by_id('password')
    btn = browser.find_element_by_css_selector('.geetest_radar_btn')
    user_input.send_keys(user)
    pwd_input.send_keys(password)
    btn.click()
    time.sleep(0.5)
    return browser
#获取滑动验证图片位置
def get_position(img_label):
    location = img_label.location
    size = img_label.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']
    return (left, top, right, bottom)
#获取浏览器截图
def get_screenshot(browser):
    screenshot = browser.get_screenshot_as_png()
    f = BytesIO()
    f.write(screenshot)
    return Image.open(f)
#对比上两张图算位置
def get_position_scale(browser,screen_shot):
    height = browser.execute_script('return document.documentElement.clientHeight')
    width = browser.execute_script('return document.documentElement.clientWidth')
    x_scale = screen_shot.size[0] / (width+10)
    y_scale = screen_shot.size[1] / (height)
    return (x_scale,y_scale)
#获取有缺口的滑动图片
def get_slideimg_screenshot(screenshot,position,scale):
    x_scale,y_scale = scale
    position = [position[0] * x_scale, position[1] * y_scale, position[2] * x_scale, position[3] * y_scale]
    return screenshot.crop(position)
#比较原始和缺口图
def compare_pixel(img1,img2,x,y):
    pixel1 = img1.load()[x,y]
    pixel2 = img2.load()[x,y]
    threshold = 50
    if abs(pixel1[0]-pixel2[0])<=threshold:
        if abs(pixel1[1]-pixel2[1])<=threshold:
            if abs(pixel1[2]-pixel2[2])<=threshold:
                return True
    return False

def compare(full_img,slice_img):
    left = 0
    for i in range(full_img.size[0]):
        for j in range(full_img.size[1]):
            if not compare_pixel(full_img,slice_img,i,j):
                return i
    return left
#计算滑动轨迹
def get_track(distance):
    """
    根据偏移量获取移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0

    while current < distance:
        if current < mid:
            # 加速度为正 2
            a = 4
        else:
            # 加速度为负 3
            a = -3
        # 初速度 v0
        v0 = v
        # 当前速度 v = v0 + at
        v = v0 + a * t
        # 移动距离 x = v0t + 1/2 * a * t^2
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track
#移动
def move_to_gap(browser,slider, tracks):
    """
    拖动滑块到缺口处
    :param slider: 滑块
    :param tracks: 轨迹
    :return:
    """
    ActionChains(browser).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()
#主函数，使用时括号中定位均需修改
if __name__ == '__main__':
    browser = get_url('https://captcha1.scrape.center/','111','***')  #网址，后两项为用户名和密码，需修改
    time.sleep(1)
    slice_img_label = browser.find_element_by_css_selector('div.geetest_slicebg') #找到滑动图片标签，需修改
    browser.execute_script("document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'none'") #将小块隐藏，需修改
    full_img_label = browser.find_element_by_css_selector('canvas.geetest_canvas_fullbg') #原始图片的标签，需修改
    position = get_position(slice_img_label) #获取滑动验证图片位置
    screenshot = get_screenshot(browser) #获取浏览器截图
    position_scale = get_position_scale(browser,screenshot) #对比上两张图算位置
    slice_img = get_slideimg_screenshot(screenshot,position,position_scale) #获取有缺口的滑动图片
    browser.execute_script("document.getElementsByClassName('geetest_canvas_fullbg')[0].style['display'] = 'block'") #在浏览器中显示原图，需修改
    screenshot = get_screenshot(browser) #获取整个浏览器图片
    full_img = get_slideimg_screenshot(screenshot,position,position_scale) # 截取滑动验证原图
    browser.execute_script("document.getElementsByClassName('geetest_canvas_slice')[0].style['display'] = 'block'")  #将小块重新显示，需修改
    left = compare(full_img,slice_img) #比较原始和缺口图
    left = left / position_scale[0] #将该位置还原为浏览器中的位置
    slide_btn = browser.find_element_by_css_selector('.geetest_slider_button') #获取滑动按钮，需修改
    track = get_track(left) #计算滑动轨迹
    move_to_gap(browser,slide_btn,track) #移动
    success = browser.find_element_by_css_selector('.geetest_success_radar_tip') #获取显示结果的标签，需修改
    time.sleep(2)
    if success.text == "验证成功":
        login_btn = browser.find_element_by_css_selector('button.j-login-btn') #如果验证成功，则点击登录按钮，需修改
        login_btn.click()
    else:
        print(success.text)
        print('失败') 
