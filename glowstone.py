import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QDesktopWidget, QTextBrowser, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QPixmap, QPainter, QTransform, QFont, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer
import ctypes
import random
import mouse
import math

def excepthook(type, value, traceback):
    print(type, value)
    sys.__excepthook__(type, value, traceback)
    sys.exit()

sys.excepthook = excepthook
def vec(theta):
    radians = math.radians(theta)
    x = math.cos(radians)
    y = math.sin(radians)
    return x, y
def rotateTo(angleNow, angleTo, rotateSpeed, sameSpeed=True):
    tz = 0
    if abs(angleNow + 360 - angleTo) < abs(angleTo - angleNow):
        tz = angleTo - angleNow - 360
    else:
        if abs(angleTo + 360 - angleNow) < abs(angleTo - angleNow):
            tz = angleTo + 360 - angleNow
        else:
            tz = angleTo - angleNow
    if sameSpeed:
        if tz > rotateSpeed:
            tz = rotateSpeed
        if tz < (rotateSpeed * -1):
            tz = rotateSpeed * -1
    else:
        tz *= rotateSpeed
    return angleNow + tz

def ag(x, y):
    theta = math.degrees(math.atan2(y, x))
    return theta

def get_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance
timers = []
objs = []

class Timer:
    def __init__(self, time=0, reverse=False, runWhenFinish=None):
        global timers
        self.timeInit = time
        self.time = time
        self.rev = reverse
        self.RWF = runWhenFinish
        timers.append(self)
    def update(self):
        if self.rev:
            self.time -= 1
            if self.time <= 0:
                if self.RWF is not None:
                    self.RWF()
        else:
            self.time += 1

    def reset(self):
        self.time = self.timeInit

    def getTime(self):
        return self.time

    def delete(self):
        global timers
        for tmd in range(len(timers)):
            if timers[tmd] is self:
                timers.pop(tmd)
                break
texts = []
class Text:
    def __init__(self, txt=""):
        self.text = txt
        self.pos = [0, 0]
        self.color = (0, 0, 0)
        self.size = 20
        self.show = True
    def update(self):
        pass
    def add(self):
        global texts
        texts.append(self)

def pressed(button=0x01):
    return (bool(ctypes.windll.user32.GetAsyncKeyState(button) & 0x8000))
class Obj:
    def __init__(self, img):
        # 初始化
        # 图像路径
        self.img = img
        # 默认角度
        self.a = 0
        # 默认坐标
        self.pos = [0, 0]
        # 显示？
        self.show = True
        # 透明度
        self.opacity = 1

        self.pixmap = None
        # 计时器
        self.counter = 0
        # 大小
        self.scale = [1, 1]
        # 是否启用多帧图
        self.muti_img = False
        # 每帧间隔时间（单位为0.01s）
        self.frameChangeTime = 10
        # 帧图列表，按顺序填入每一帧的路径
        self.frames = [img]
        # 当前帧
        self.frame = 0
        # 切换帧图倒计时
        self.timeUntilFrameChange = 10
        # 倒计时速度
        self.countSpeed = 1
    def add(self):
        # 将对象投入使用
        global objs
        objs.append(self)

    def get_file(self, name, path):
        # 当拖放文件到该对象时调用
        pass

    def mouse_pointing(self):
        # 鼠标是否悬浮在该对象上
        x, y = mouse.get_position()
        x1, y1, x2, y2 = self.get_rect()[0][0], self.get_rect()[0][1], self.get_rect()[1][0], self.get_rect()[1][1]
        return x1 <= x <= x2 and y1 <= y <= y2

    def mouse_pressing(self, button=0x01):
        # 是否被鼠标按住
        x, y = mouse.get_position()
        x1, y1, x2, y2 = self.get_rect()[0][0], self.get_rect()[0][1], self.get_rect()[1][0], self.get_rect()[1][1]
        return x1 <= x <= x2 and y1 <= y <= y2 and (bool(ctypes.windll.user32.GetAsyncKeyState(button) & 0x8000))
    def other_paint(self, painter):
        # 额外绘制
        pass

    def end_paint(self, painter):
        #在绘制完所有对象后的绘制操作
        pass

    def setScale(self, sx, sy):
        #设置尺寸
        self.scale = [sx, sy]

    def getScale(self):
        #获取尺寸
        return self.scale

    def drawPixmap(self, painter, pxm, pos, rotate=0, scale=None):
        # 绘制一个 QPixmap
        if scale is None:
            scale = [1, 1]
        transform = QTransform()
        transform.translate(int(pos[0]),
                            int(pos[1]))
        transform.rotate(rotate)
        transform.scale(scale[0], scale[1])
        pxm = pxm.transformed(transform)
        painter.drawPixmap(round(pos[0] - pxm.width()/2), round(pos[1]-pxm.height()/2), pxm)


    def setPos(self, x, y):
        # 设置坐标
        self.pos = [x, y]


    def getPos(self):
        # 获取坐标，以[x, y]的形式返回
        return self.pos


    def setAngle(self, a):
        # 设置角度
        self.a = a

    def top(self):
        # 将该对象的绘制顺序设置为最顶部
        global objs
        for i in range(len(objs)):
            if objs[i] is self:
                objs.pop(i)
                break
        objs.append(self)


    def getAngle(self):
        # 获取角度
        return self.a

    def refreshPM(self):
        # 刷新Pixmap
        self.pixmap = QPixmap(self.img)

    def update(self):
        # 每次更新执行
        if self.counter % 100 == 0:
            self.refreshPM()
        if self.muti_img:
            self.timeUntilFrameChange -= 1
            nrf = False
            if self.timeUntilFrameChange <= 0:
                self.timeUntilFrameChange = self.frameChangeTime
                self.frame += 1
                nrf = True
            if self.frame > len(self.frames) - 1:
                self.frame = 0
                nrf = True
            self.img = self.frames[self.frame]
            if nrf:
                self.refreshPM()
        self.counter += self.countSpeed
    def discard(self):
        #设置这个对象不再绘制和更新，可使用add()函数重新加入
        for i in range(len(objs)):
            if objs[i] == self:
                objs.pop(i)
                break

    def getCounter(self):
        # 获取计时器时间
        return self.counter

    def resetCounter(self):
        # 重置计时器
        self.counter = 0

    def setCountSpeed(self, cs):
        # 设置计时器计时速度
        self.countSpeed = cs

    def getCountSpeed(self):
        #获取计时器计时速度
        return self.countSpeed

    def get_rect(self):
        # 获取矩形
        if self.pixmap == None:
            return ((0, 0), (0, 0))
        return ((self.pos[0] - self.pixmap.width() * self.getScale()[0] / 2, self.pos[1] - self.pixmap.height() * self.getScale()[1] / 2), (self.pos[0] + self.pixmap.width() * self.scale[1] / 2, self.pos[1] + self.pixmap.height() * self.scale[1] / 2))
    def collide(self, obj):
        # 是否碰撞到了另一个对象

        # 获取矩形四个角坐标
        x1_1, y1_1, x2_1, y2_1 = self.get_rect()[0][0], self.get_rect()[0][1], self.get_rect()[1][0], self.get_rect()[1][1]
        x1_2, y1_2, x2_2, y2_2 = obj.get_rect()[0][0], obj.get_rect()[0][1], obj.get_rect()[1][0], obj.get_rect()[1][1]

        # 检查水平方向上是否有重叠
        horizontal_overlap = (x1_1 < x2_2) and (x2_1 > x1_2)

        # 检查垂直方向上是否有重叠
        vertical_overlap = (y1_1 < y2_2) and (y2_1 > y1_2)

        # 如果水平和垂直方向上都有重叠，则矩形接触
        return horizontal_overlap and vertical_overlap

    def prePaint(self, painter):
        # 默认绘制之前的绘制
        pass

    def paintChain(self, painter, imgPath, pos1, pos2, spacing = None):
        # 用一个图片绘制一个”锁链“链接两个坐标
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setBrush(Qt.white)
        self.image_path = imgPath
        self.pixmap = QPixmap(self.image_path)

        if spacing == None:
            spacing = self.pixmap.width()
        transform = QTransform()
        transform.translate(pos1[0],
                            pos1[1])

        transform.rotate(ag(pos1[0] - pos2[0], pos1[1] - pos2[1]))
        agl = ag(pos1[0] - pos2[0], pos1[1] - pos2[1])
        transformed_pixmap = self.pixmap.transformed(transform)
        self.pixmap = transformed_pixmap
        self.image_position = [pos1[0] - self.pixmap.width() / 2, pos2[1] - self.pixmap.height() / 2]
        # 绘制图片

        cx, cy = pos2[0] - self.pixmap.width() / 2, pos2[1] - self.pixmap.height() / 2
        for i in range(int(get_distance(pos1[0] - self.pixmap.width() / 2, pos1[1] - self.pixmap.height() / 2, pos2[0] - self.pixmap.width() / 2, pos2[1] - self.pixmap.height() / 2) / spacing + 1) * 2):
            painter.setOpacity(1.0)
            painter.drawPixmap(cx, cy, transformed_pixmap)
            cx += vec(agl)[0] * spacing / 2
            cy += vec(agl)[1] * spacing / 2

#透明背景
trans_background = True

#背景颜色，不建议使用，有Bug，推荐加一个图像比较小的背景控件然后缩放到全屏
backColor = (255, 255, 255)


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ct = 100
        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        if trans_background:
            self.setAttribute(Qt.WA_TranslucentBackground)

        # 创建标签用于显示图片
        self.label = QLabel(self)
        self.info = ""
        self.label.setGeometry(0, 0, self.width(), self.height())
        self.text_browser = QLabel(self)
        self.text_browser.setStyleSheet("color:rgb(90,90,170); font-size:36px;")
        self.text_browser.setGeometry(10, self.height() - 10, 1000, 80)

        self.txttime = 0
        # 加载图片
        self.image_path = ""
        self.pixmap = QPixmap(self.image_path)

        # 初始位置和角度
        self.image_position = [0, 0]
        self.image_angle = 0

        # 创建定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_window)
        self.timer.start(10)  # 设置定时器的时间间隔（毫秒）
        # 显示窗口
        self.showFullScreen()
        self.z = 0
        self.t = 0
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("泰拉桌宠")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # 接受拖放文件事件
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 拖放文件事件
        global objs
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            fname = file_path.split("/")[len(file_path.split("/")) - 1]
            for i in objs:
                if i.mouse_pointing():
                    i.get_file(fname, file_path)

    def exit_application(self):
        # 退出应用程序
        sys.exit()

    def paintEvent(self, event):
        # 绘制对象
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setBrush(Qt.white)
        for i in objs:
            if not i.show:
                continue
            if i.pixmap == None:
                i.pixmap = QPixmap(i.img)
            self.pixmap = i.pixmap
            if self.pixmap == None:
                continue
            painter.setOpacity(i.opacity)
            self.image_angle = i.a
            # 设置图片位置和角度
            transform = QTransform()
            transform.translate(int(self.image_position[0]),
                                int(self.image_position[1]))
            transform.rotate(self.image_angle)
            transform.scale(i.scale[0], i.scale[1])
            transformed_pixmap = self.pixmap.transformed(transform)

            self.pixmap = transformed_pixmap
            self.image_position = [i.pos[0] - self.pixmap.width()/2, i.pos[1] - self.pixmap.height()/2]

            # 绘制图片
            i.prePaint(painter)
            painter.drawPixmap(round(self.image_position[0]), round(self.image_position[1]), self.pixmap)
            painter.setOpacity(i.opacity)
            i.other_paint(painter)
        for i in texts:
            if i.show:
                font = QFont("Arial", i.size)
                painter.setFont(font)
                painter.setPen(QColor(i.color[0], i.color[1], i.color[2]))
                painter.drawText(i.pos[0], i.pos[1], i.text)
        for i in objs:
            painter.setOpacity(i.opacity)
            i.end_paint(painter)


    def update_window(self):
        # 更新
        for i in timers:
            i.update()
        idx = len(objs) - 1
        for i in range(len(objs)):
            objs[idx].update()
            idx -= 1
        for i in texts:
            i.update()
        self.update()
app = None
window = None
def screen_size():
    # 获取屏幕大小，请勿在窗口创建前调用
    return (window.width(), window.height())



def run_window():
    # 启动窗口，持续执行直到关闭
    global app, window, backColor
    app = QApplication(sys.argv)
    window = TransparentWindow()

def app_exit():
    #退出程序
    global app
    sys.exit(app.exec_())