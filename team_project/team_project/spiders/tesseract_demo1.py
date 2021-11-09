import pytesseract
from PIL import Image

# cmd : tesseract demo.png a

# # demo1
# image = Image.open('code3.png')
# result = pytesseract.image_to_string(image)
# print(result)

# # demo2 灰度图像 二值化 Image对象调用convert()
# image = Image.open('code1.png')
# image = image.convert('L') # 转为灰度图像
# image = image.convert('1') # 传入 1 即可将图片进行二值化处理(默认阈值127)
# image.show()

# # demo3 指定二值化阈值 不能直接转化原图，要将原图先转为灰度图像，然后再指定二值化阈值
# image = Image.open('code2.png')
# image = image.convert('L')  #首先转化为灰度图像
# threshold = 150   #二值化阈值
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table,'1') # 灵魂
# image.show()
# # result = pytesseract.image_to_string(image)
# # print(result)

# # demo4 图像锐化   需要PIL中的ImageFilter模块   使用方法：Image对象.filter(ImageFilter.SHARPEN)
# from PIL import ImageFilter
# image = Image.open('code4.png')
# # image.show()
# image = image.convert('L')
# threshold = 200
# table = []
# for i in range(256):
#     if i < threshold:
#         table.append(0)
#     else:
#         table.append(1)
# image = image.point(table,'1')
# image = image.filter(ImageFilter.SHARPEN)
# image.show()
# result = pytesseract.image_to_string(image)
# print(result)

from scrapy_redis.spiders import RedisSpider


class CharacterSpider(RedisSpider):
    name = 'slide'
    # start_urls = [
    #     'https://www.qiushibaike.com/hot/page/1/'
    # ]
    redis_key = "slide:start_urls"

    def parse(self, response):
        pass