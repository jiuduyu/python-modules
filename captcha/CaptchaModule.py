# encoding:utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from DownModule import DownModule as DownClass
import random
import os


class CaptchaModule(object):

    width = 60 * 4
    height = 60
    fileName = ''
    fontFile = "C:/Windows/Fonts/LHANDW.TTF"
    fontSize = 40
    noFontUrl = 'http://down.zhaozi.cn/gfonts/b/Bachelor.ttf'
    fileType = '.jpg'
    captchaSavePath = './captchas'

    def __init__(self, *args, **kwargs):
        super(CaptchaModule, self).__init__(*args, **kwargs)

    @staticmethod
    def createVerificationCode(width=None, height=None, codeLength=4, captchaSavePath=None, ifFill=True, ifFilter=False):
        CaptchaModule.fontExist()
        CaptchaModule.width = width if width else CaptchaModule.width
        CaptchaModule.height = height if height else CaptchaModule.height
        CaptchaModule.image = Image.new(
            'RGB', (CaptchaModule.width, CaptchaModule.height), (255, 255, 255))
        CaptchaModule.font = ImageFont.truetype(
            CaptchaModule.fontFile, CaptchaModule.fontSize)
        # 创建Draw对象:
        CaptchaModule.draw = ImageDraw.Draw(
            CaptchaModule.image)
        for x in range(CaptchaModule.width):  # 填充每个像素:
            for y in range(CaptchaModule.height):
                CaptchaModule.draw.point(
                    (x, y), fill=CaptchaModule.rondColorPixel(ifFill))
        for t in range(codeLength):  # 输出文字
            word = CaptchaModule.rondChar()
            CaptchaModule.draw.text((60 * t + 10, 10), word,
                                    font=CaptchaModule.font, fill=CaptchaModule.rndColorPlan())
            CaptchaModule.fileName += str(word)
        if ifFilter:
            CaptchaModule.image = CaptchaModule.image.filter(
                ImageFilter.BLUR)
        captchaName = CaptchaModule.fileName + CaptchaModule.fileType
        CaptchaModule.image.save(captchaName, 'jpeg')
        CaptchaModule.saveCaptcha(captchaSavePath)

    @staticmethod
    def saveCaptcha(captchaSavePath=None):
        CaptchaModule.captchaSavePath = captchaSavePath if captchaSavePath else CaptchaModule.captchaSavePath
        captchaName = CaptchaModule.fileName + CaptchaModule.fileType
        DownClass.makePath(CaptchaModule.captchaSavePath)
        if os.path.isfile(DownClass.downFile(captchaName)):
            os.remove(captchaName)

    @staticmethod
    def rondChar():
        return chr(random.randint(65, 90))

    @staticmethod
    def rondColorPixel(ifRond=True):
        if ifRond:
            return (random.randint(70, 250), random.randint(70, 250), random.randint(70, 250))
        else:
            return (255, 255, 255)

    @staticmethod
    def rndColorPlan():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    @staticmethod
    def fontExist(fontUrl=None):  #
        CaptchaModule.noFontUrl = fontUrl if fontUrl else CaptchaModule.noFontUrl
        if os.path.isfile(CaptchaModule.fontFile):
            return True
        else:
            CaptchaModule.fontFile = DownClass.downFile(
                CaptchaModule.noFontUrl)

    def __str__(self):
        return self.fileName
# exmple:
#CaptchaModule.createVerificationCode(400, None, 6)
