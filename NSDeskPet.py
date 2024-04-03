"""
NSDeskPet
原作者：B站  北极星Nighten
开放修改，可以二次分发
请勿用于盈利
"""
import glowstone
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
import time
import random
import mouse
import math
import os
import pygame
pygame.init()
pygame.mixer.init()

#初始化
displayObjs = []
distexts = []
page = 1
leftB, rightB = None, None
pls = True
menuOpened = False
deleteMode = False
thankMenuOpen = False

def playSound(file):
    # 使用Pygame播放声音
    if pls:
        pygame.mixer.Sound(file).play()

#异常处理钩子
def excepthook(type, value, traceback):
    print(type, value)
    sys.__excepthook__(type, value, traceback)
    sys.exit()
sys.excepthook = excepthook



class DPPart(glowstone.Obj):
    # 桌宠部分父类
    def __init__(self, i):
        super().__init__(i)
        self.owner = None
        self.live = True
    def update(self):
        super().update()
        if self.mouse_pressing() and deleteMode:
            self.discard()
        if not self.owner.live:
            self.discard()
    def discard(self):
        super().discard()
        self.live = False
        if self.owner in glowstone.objs:
            self.owner.discard()

class DP(glowstone.Obj):
    # 桌宠父类
    def __init__(self, i):
        super().__init__(i)
        self.live = True
        self.timer = 0
    def discard(self):
        super().discard()
        self.live = False
    def update(self):
        super().update()
        self.timer += 1
        if self.mouse_pressing() and deleteMode and not menu.mouse_pressing():
            self.discard()
    def add(self):
        self.pos = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        super().add()


#以下为桌宠的定义
class ImpactMouse(DP):
    def __init__(self):
        super().__init__("trp/other/impact.png")
        self.opacity = 0
        self.cy = False
        self.j = 0
    def update(self):
        super().update()
        if glowstone.pressed() and self.cy:
            self.pos = mouse.get_position()
            self.opacity = 1
            self.j = 0.06
            self.scale = [0, 0]
        if glowstone.pressed():
            self.cy = False
        else:
            self.cy = True

        if self.opacity > 0:
            self.opacity -= 0.04
            self.scale = [self.scale[0]+self.j, self.scale[1]+self.j]
            self.j *= 0.96

class CloverDance(DP):
    def __init__(self):
        super().__init__("trp/cd/cd0.png")
        self.muti_img = True
        self.frames = []
        self.scale = [0.45, 0.45]
        self.mpd = False
        for i in range(6):
            self.frames.append("trp/cd/cd{}.png".format(i))
        self.frameChangeTime = 15

    def update(self):
        super().update()
        if not mouse.is_pressed():
            self.mpd = False
        if self.mouse_pressing() and not self.mpd:
            self.mpd = True

        if self.mpd:
            self.setPos(mouse.get_position()[0], mouse.get_position()[1])

class Cryogen(DP):
    def __init__(self):
        super().__init__("trp/cryogen.png")
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.1
    def update(self):
        super().update()
        if random.randint(0, 100) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        self.a += 5
        self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
        self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98

class CalamitasClone(DP):
    def __init__(self):
        super().__init__("trp/calaclone1.png")
        self.muti_img = True
        self.frames = []
        for i in range(6):
            self.frames.append("trp/calaclone{}.png".format(str(i+1)))
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.05
    def update(self):
        super().update()
        if random.randint(0, 150) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.tgp[0], self.tgp[1], self.pos[0], self.pos[1]) > 120:
            self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
            self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98
        self.setAngle(glowstone.ag(self.dx, self.dy)-90)

class EOC(DP):
    def __init__(self):
        super().__init__("trp/ce.png")
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.05
    def update(self):
        super().update()
        if random.randint(0, 150) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.tgp[0], self.tgp[1], self.pos[0], self.pos[1]) > 120:
            self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
            self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        else:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98
        self.setAngle(glowstone.ag(self.dx, self.dy)-90)

class AQSCBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 30
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90

class AquaticScourge(DP):
    def __init__(self):
        super().__init__("trp/aqs/head.png")
        self.length = 50
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.dyj = 0.02
        self.speed = 0.05
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            if set2:
                ap = AQSCBody("trp/aqs/body2.png")

            else:
                ap = AQSCBody("trp/aqs/body.png")
            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/aqs/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        if self.pos[1] < 180:
            self.dy += 0.1
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.994
        if random.randint(0, 300) == 1:
            self.dyj = random.randint(4, 10) / 1000
        self.dy += self.dyj / 3
        if self.moved == 1:
            self.dx += 0.01
        else:
            self.dx -= 0.01
        self.setAngle(glowstone.ag(self.dx, self.dy)+90)
        if self.pos[1] > glowstone.screen_size()[1] + 10:
            self.dy -= 0.01
            if self.pos[0] < mouse.get_position()[0]:
                self.moved = 1
            else:
                self.moved = 0


class ADBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 36
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90
class AstrumDeus(DP):
    def __init__(self):
        super().__init__("trp/ad/head.png")
        self.length = 40
        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 3
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            if set2:
                ap = ADBody("trp/ad/body2.png")
            else:
                ap = ADBody("trp/ad/body.png")
            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/ad/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 760:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.6)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed

class AstrumAureus(DP):
    def __init__(self):
        super().__init__("trp/astrumau/aa1.png")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(6):
            self.frames.append("trp/astrumau/aa{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
    def update(self):
        super().update()
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - 188:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0, 1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 188:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 188:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 188
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992
class BrimstoneElm(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(8):
            self.frames.append("trp/brel/b{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.mode2 = False
        self.tgt = [1000, 600]
        self.scale = [1.4, 1.4]
    def update(self):
        if self.mode2:
            if self.dr:
                self.frames = []
                for i in range(4):
                    self.frames.append("trp/brel/ff{}.png".format(str(i + 1)))
            else:
                self.frames = []
                for i in range(4):
                    self.frames.append("trp/brel/f{}.png".format(str(i + 1)))
        else:
            if self.dr:
                self.frames = []
                for i in range(8):
                    self.frames.append("trp/brel/fb{}.png".format(str(i + 1)))
            else:
                self.frames = []
                for i in range(8):
                    self.frames.append("trp/brel/b{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if random.randint(0, 900) == 0:
            self.mode2 = not self.mode2
class DarkEng(DPPart):
    def __init__(self):
        super().__init__("")
        self.ctr = 0
        self.g = 0
        self.cf = 0
        self.f = 1
        self.muti_img = True
        self.mx = 800
        self.frames = []
        for i in range(8):
            self.frames.append("trp/cv/d{}.png".format(i+1))
    def update(self):
        super().update()
        self.cf += 1
        if self.cf > 8:
            self.cf = 0
            self.f += 1
        if self.f > 8:
            self.f = 1
        self.img = "img_cv\\d" + str(self.f) + ".png"
        self.ctr += 1.4
        self.g += 0.4
        self.a = self.g
        p = self.ctr
        mx = self.mx
        if self.ctr > mx * 2:
            self.ctr = 0
            p = 0
        if p > mx:
            p = mx * 2 - p
        self.setPos(self.owner.pos[0] + glowstone.vec(self.a)[0] * p, self.owner.pos[1] + glowstone.vec(self.a)[1] * p)
        self.a = 0
class Birb(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(8):
            self.frames.append("trp/birb/b{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.06
        self.tgt = [1000, 600]
        self.scale = [1.4, 1.4]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/birb/fb{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/birb/b{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]


class CrlsVoid(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(6):
            self.frames.append("trp/cv/c{}.png".format(str(i + 1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.0166
        self.tgt = [1000, 600]
        self.scale = [1.4, 1.4]
        a = 0
        dt = 0
        for i in range(9):
            if dt % 2 == 0:
                st = 0
            else:
                st = 90

            dt += 1
            d = DarkEng()
            d.owner = self
            d.ctr = st
            d.g = a
            d.add()
            a += 40
            d.mx = 400
        a = 0
        for i in range(3):
            ds = 0
            for i in range(4):
                d = DarkEng()
                d.owner = self
                d.g = a
                d.ctr = ds
                ds += 200
                d.add()
            a += 120
    def update(self):

        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
class Calamitas(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [2, 2]
        self.frames = []
        for i in range(13):
            self.frames.append("trp/scl/c{}.png".format(str(i)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 1.1
        self.move = True
    def update(self):
        super().update()
        if self.dr:
            self.frames = []
            for i in range(13):
                self.frames.append("trp/scl/fc{}.png".format(str(i)))
        else:
            self.frames = []
            for i in range(13):
                self.frames.append("trp/scl/c{}.png".format(str(i)))

        if random.randint(0, 500) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
            self.move = random.randint(0, 1) == 0
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
            self.move = True
        if self.pos[0] < 0:
            self.dr = True
            self.move = True
        if self.movet > 0:
            if self.dr:
                self.dx = self.speed
            else:
                self.dx = -1 * self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 110:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 110:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 110
        if self.move:
            self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
            self.muti_img = True
        else:
            self.muti_img = False
            self.img = self.frames[0]

class Crabulon(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [1, 1]
        self.frames = []
        for i in range(6):
            self.frames.append("trp/cl/c{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
    def update(self):
        super().update()
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - 154:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 154:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 154:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 154
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992
class DSBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 40
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90

class DesertScourge(DP):
    def __init__(self):
        super().__init__("trp/dss/head.png")
        self.length = 20
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.dyj = 0.02
        self.speed = 0.02
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            ap = DSBody("trp/dss/body.png")

            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/dss/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        if self.pos[1] < 180:
            self.dy += 0.04
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.994
        if random.randint(0, 300) == 1:
            self.dyj = random.randint(4, 10) / 1000
        self.dy += self.dyj / 1
        if self.moved == 1:
            self.dx += 0.01
        else:
            self.dx -= 0.01
        self.setAngle(glowstone.ag(self.dx, self.dy)+90)
        if self.pos[1] > glowstone.screen_size()[1] + 10:
            self.dy -= 0.016
            if self.pos[0] < mouse.get_position()[0]:
                self.moved = 1
            else:
                self.moved = 0
        if self.pos[0] < 0:
            self.moved = 1
        elif self.pos[0] > glowstone.screen_size()[0]:
            self.moved = 0
class DogBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 46
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
class DvOfGods(DP):
    def __init__(self):
        super().__init__("trp/dog/head.png")
        self.length = 60
        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 6
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            ap = DogBody("trp/dog/body.png")
            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/dog/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 760:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.6)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed

class AresPart(DPPart):
    def __init__(self, i):
        super().__init__(i)
        self.scale = [1.6, 1.6]
        self.xp = 0
        self.yp = 0
    def update(self):
        super().update()
        self.pos = [self.owner.pos[0] + self.xp, self.owner.pos[1] + self.yp]
        self.setAngle(glowstone.ag(mouse.get_position()[0]-self.pos[0], mouse.get_position()[1] - self.pos[1]))

class Ares(DP):
    def __init__(self):
        super().__init__("trp/ars/xf09.png")
        self.scale = [1.6, 1.6]
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.06
        self.tgt = [1000, 600]
        self.scale = [1.4, 1.4]
        part = AresPart("trp/ars/x1")
        part.xp = -360
        part.yp = 70
        part.owner = self
        part.add()
        part = AresPart("trp/ars/x2")
        part.xp = -260
        part.yp = 140
        part.owner = self
        part.add()
        part = AresPart("trp/ars/x3")
        part.xp = 260
        part.yp = 140
        part.owner = self
        part.add()
        part = AresPart("trp/ars/x4")
        part.xp = 360
        part.yp = 70
        part.owner = self
        part.add()
    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/birb/fb{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/birb/b{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

class Apollo(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(7):
            self.frames.append("trp/exeye/ap{}.png".format(str(i+1)))
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.08
    def update(self):
        super().update()
        if random.randint(0, 120) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.tgp[0], self.tgp[1], self.pos[0], self.pos[1]) > 120:
            self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
            self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98
        self.setAngle(glowstone.ag(self.dx, self.dy)+90)
class Artemis(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(7):
            self.frames.append("trp/exeye/at{}.png".format(str(i+1)))
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.08
    def update(self):
        super().update()
        if random.randint(0, 120) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.tgp[0], self.tgp[1], self.pos[0], self.pos[1]) > 120:
            self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
            self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98
        self.setAngle(glowstone.ag(self.dx, self.dy)+90)
class TnBodya(DPPart):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(5):
            self.frames.append("trp/tnts/tba{}.png".format(i + 1))
        self.follow = None
        self.spacing = 90
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90
class TnBodyb(DPPart):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(5):
            self.frames.append("trp/tnts/tbb{}.png".format(i + 1))
        self.follow = None
        self.spacing = 90
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90
class TnTail(DPPart):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(5):
            self.frames.append("trp/tnts/tbt{}.png".format(i + 1))
        self.follow = None
        self.spacing = 90
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
        self.a += 90
class Thanatos(DP):
    def __init__(self):
        super().__init__("")
        self.length = 36
        self.muti_img = True
        self.frames = []
        for i in range(5):
            self.frames.append("trp/tnts/tbh{}.png".format(i+1))

        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 6
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            if set2:
                ap = TnBodya()
            else:
                ap = TnBodyb()
            ap.owner = self
            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap
        ap = TnTail()
        ap.owner = self
        ap.follow = syg
        ap.add()
        bodies.append(ap)

        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.a -= 90
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], mouse.get_position()[0], mouse.get_position()[1]) > 760:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(mouse.get_position()[0] - self.pos[0], mouse.get_position()[1] - self.pos[1]), 1.3)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed
        self.a += 90
class Draedon(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(12):
            self.frames.append("trp/dd/d{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.06
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(12):
                self.frames.append("trp/dd/fd{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(12):
                self.frames.append("trp/dd/d{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

class HiveMind(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [1, 1]
        self.frames = []
        for i in range(16):
            self.frames.append("trp/hm/c{}.png".format(str(i+1)))
        self.mvt = 200

    def update(self):
        super().update()
        if random.randint(0, 900) == 0 and self.mvt <= 0:
            self.mvt = 200
        if self.mvt >= 100:
            self.scale = [(self.mvt-100)/100, (self.mvt-100)/100]
        elif self.mvt > 0:
            self.scale = [(100-self.mvt)/100, (100-self.mvt)/100]
        else:
            self.scale = [1, 1]
        if self.mvt == 100:
            self.pos = [random.randint(-200, 200)+mouse.get_position()[0], glowstone.screen_size()[1] - 120]
        self.mvt -= 2
class Perforator(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [1, 1]
        self.frames = []
        for i in range(10):
            self.frames.append("trp/ph/l{}.png".format(str(i+1)))
        self.mvt = 200

    def update(self):
        super().update()
        if random.randint(0, 900) == 0 and self.mvt <= 0:
            self.mvt = 200
        if self.mvt >= 100:
            self.scale = [(self.mvt-100)/100 * 1.5, (self.mvt-100)/100 * 1.5]
        elif self.mvt > 0:
            self.scale = [(100-self.mvt)/100 * 1.5, (100-self.mvt)/100 * 1.5]
        else:
            self.scale = [1.5, 1.5]
        if self.mvt == 100:
            self.pos = [random.randint(-200, 200)+mouse.get_position()[0], glowstone.screen_size()[1] - 120]
        self.mvt -= 2
class Anahita(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [0.7, 0.7]
        self.frames = []
        for i in range(6):
            self.frames.append("trp/aal/a{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.06
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/aal/fa{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/aal/a{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
class Lvt(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        self.frameChangeTime = 20
        for i in range(6):
            self.frames.append("trp/aal/l{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.02
        self.tgt = [1000, 600]
        self.scale = [1.1, 1.1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/aal/fl{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/aal/l{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
class OldDuke(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(7):
            self.frames.append("trp/od/l{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.07
        self.tgt = [1000, 600]
        self.scale = [1.4, 1.4]

    def update(self):
        if not self.dr:
            self.frames = []
            for i in range(7):
                self.frames.append("trp/od/fl{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(7):
                self.frames.append("trp/od/l{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]



class PlaguebringerGoliath(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(6):
            self.frames.append("trp/gt/d{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.09
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/gt/fd{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/gt/d{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]


class KingBee(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(8):
            self.frames.append("trp/kb/b{}.png".format(str(i + 1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.09
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(8):
                self.frames.append("trp/kb/fb{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(8):
                self.frames.append("trp/kb/b{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

    def get_file(self, name, path):
        if "瘟疫细胞罐" in name:
            sp = PlaguebringerGoliath()
            sp.add()
            sp.tgt = self.tgt
            sp.dx = self.dx
            sp.dy = self.dy
            sp.movet = self.movet
            sp.dr = self.dr
            sp.pos = self.pos
            self.discard()

class Yharon(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(5):
            self.frames.append("trp/yh/y{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.09
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(5):
                self.frames.append("trp/yh/y{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(5):
                self.frames.append("trp/yh/fy{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
class PtgHook(DPPart):
    def __init__(self):
        super().__init__("trp/ptg/ph1.png")
        self.pos = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        self.targetPos = self.pos
    def update(self):
        super().update()
        if random.randint(1, 100) == 1:
            self.targetPos = (self.owner.pos[0] + random.randint(-340, 340), self.owner.pos[1] + random.randint(-340, 340))
        self.a = glowstone.ag(self.targetPos[0] - self.pos[0], self.targetPos[1] - self.pos[1])
        self.pos[0] += glowstone.vec(self.a)[0] * 15
        self.pos[1] += glowstone.vec(self.a)[1] * 15
        if glowstone.get_distance(self.pos[0], self.pos[1], self.targetPos[0], self.targetPos[1]) < 16:
            self.pos[0] = self.targetPos[0]
            self.pos[1] = self.targetPos[1]
            self.img = "trp/ptg/ph2.png"
        else:
            self.img = "trp/ptg/ph1.png"
        self.a = glowstone.ag(self.pos[0] - self.owner.pos[0], self.pos[1] - self.owner.pos[1])
    def prePaint(self, painter):
        super().other_paint(painter)
        self.paintChain(painter, "trp/ptg/pc.png", self.owner.pos, self.pos)
class PolterGhast(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(4):
            self.frames.append("trp/ptg/l{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.frameChangeTime = 28
        self.movet = 0
        self.dr = True
        self.speed = 0.05
        self.tgt = [1000, 600]
        self.scale = [1, 1]
        hk = PtgHook()
        hk.owner = self
        hk.add()
        hk = PtgHook()
        hk.owner = self
        hk.add()
        hk = PtgHook()
        hk.owner = self
        hk.add()
        hk = PtgHook()
        hk.owner = self
        hk.add()
        self.top()
    def update(self):
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
        self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.99
        self.dy *= 0.99
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.a = glowstone.ag(self.dx, self.dy) + 90

class PwBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 56
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
class Pw(DP):
    def __init__(self):
        super().__init__("trp/pw/head.png")
        self.length = 70
        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 2.8
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            if set2:
                ap = PwBody("trp/pw/body2.png")
            else:
                ap = PwBody("trp/pw/body.png")
            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/pw/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 1160:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.6)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed
class Providence(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.scale = [1, 1]
        self.frames = []
        for i in range(3):
            self.frames.append("trp/pvd/p{}.png".format(str(i+1)))
        if time.localtime(time.time()).tm_hour > 18 and time.localtime(time.time()).tm_hour < 4:
            self.frames = []
            for i in range(3):
                self.frames.append("trp/pvd/pn{}.png".format(str(i + 1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.06
        self.tgt = [1000, 600]
        self.scale = [1, 1]
        self.frameChangeTime = 12
        self.tmr = 0
    def update(self):
        super().update()
        self.tmr += 1
        if self.tmr % 1000 == 1:
            self.frames = []
            for i in range(3):
                self.frames.append("trp/pvd/p{}.png".format(str(i + 1)))
            if time.localtime(time.time()).tm_hour >= 18 or time.localtime(time.time()).tm_hour <= 4:
                self.frames = []
                for i in range(3):
                    self.frames.append("trp/pvd/pn{}.png".format(str(i + 1)))
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

class Signus(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.frames = []
        for i in range(6):
            self.frames.append("trp/sg/sg{}.png".format(str(i+1)))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/sg/fsg{}.png".format(str(i + 1)))
        else:
            self.frames = []
            for i in range(6):
                self.frames.append("trp/sg/sg{}.png".format(str(i + 1)))
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

class Ravager(DP):
    def __init__(self):
        super().__init__("trp/ravager.png")
        self.scale = [1.05, 1.05]
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
    def update(self):
        super().update()
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - 170:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 170:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 170:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 170
        if self.pos[1] == glowstone.screen_size()[1] - 170:
            self.pos = [self.pos[0], self.pos[1] + self.dy]
        else:
            self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992

class CrimsonSlime(DP):
    def __init__(self):
        super().__init__("trp/sgod/c1.png")
        self.scale = [1.05, 1.05]
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.fr = 6
        self.timer = 0
    def update(self):
        super().update()
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - 120:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
            self.fr = 6
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 120:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 120:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 120
        if self.pos[1] == glowstone.screen_size()[1] - 120:
            self.pos = [self.pos[0], self.pos[1] + self.dy]
        else:
            self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992
        if self.fr > 0:
            self.img = "trp/sgod/c{}.png".format(7 - self.fr)
            if self.timer % 6 == 0:
                self.fr -= 1
        else:
            self.img = "trp/sgod/c1.png"
        self.timer += 1
class EbonianSlime(DP):
    def __init__(self):
        super().__init__("trp/sgod/e1.png")
        self.scale = [1.05, 1.05]
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.fr = 6
        self.timer = 0
    def update(self):
        super().update()
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - 120:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
            self.fr = 6
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - 120:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - 120:
            if self.dy > 0:
                self.dy = 0
            self.pos[1] = glowstone.screen_size()[1] - 120
        if self.pos[1] == glowstone.screen_size()[1] - 120:
            self.pos = [self.pos[0], self.pos[1] + self.dy]
        else:
            self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992
        if self.fr > 0:
            self.img = "trp/sgod/e{}.png".format(7 - self.fr)
            if self.timer % 6 == 0:
                self.fr -= 1
        else:
            self.img = "trp/sgod/e1.png"
        self.timer += 1

class SlimeGod(DP):
    def __init__(self):
        super().__init__("trp/sgod/core.png")
        self.tgp = [600, 600]
        self.dx = 0
        self.dy = 0
        self.speed = 0.1
    def update(self):
        super().update()
        if random.randint(0, 100) == 1:
            self.tgp = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        self.a += 5
        self.dx += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[0] * self.speed
        self.dy += glowstone.vec(glowstone.ag(self.tgp[0] - self.pos[0], self.tgp[1] - self.pos[1]))[1] * self.speed
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.98
        self.dy *= 0.98

class SWBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 40
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
class StormWeaver(DP):
    def __init__(self):
        super().__init__("trp/sw/head.png")
        self.length = 40
        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 3
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            ap = SWBody("trp/sw/body.png")

            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/sw/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 760:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.6)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed
class Arm(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.forearm = None
    def update(self):
        super().update()
        self.setPos(self.forearm.pos[0] + glowstone.vec(self.forearm.a)[0] * 70, self.forearm.pos[1] + glowstone.vec(self.forearm.a)[1] * 70)
        self.a = self.forearm.follow.a

class Forearm(DPPart):
    def __init__(self, img, o):
        super().__init__(img)
        self.owner = o
        self.follow = None
        self.right = True
        self.anmtick = 0
        self.arm = Arm("trp/sp/arm2.png")
        self.arm.owner = self.owner
        self.arm.forearm = self
        self.arm.add()
    def update(self):
        super().update()
        self.setPos(self.follow.pos[0], self.follow.pos[1])

        self.setAngle(self.follow.a)

        self.setPos(self.pos[0] + glowstone.vec(self.a)[0] * 20, self.pos[1] + glowstone.vec(self.a)[1] * 20)
        self.anmtick += 5
        if self.anmtick > 400:
            self.anmtick += 5
        if self.anmtick > 1000:
            self.anmtick = 0
        if self.anmtick <= 400:
            az = (self.anmtick / 400) * 180
        else:
            az = ((600 - (self.anmtick - 400)) / 600) * 180
        if self.right:
            az *= -1

        if self.right:
            self.a -= 36
        else:
            self.a += 36
        az *= 0.6
        self.a += az

class SPBody(DPPart):
    def __init__(self, img, o):
        super().__init__(img)
        self.owner = o
        self.follow = None
        self.drawArm = False
        self.spacing = 46
        self.armpxm = QPixmap("trp/sp/arm1.png")
        self.forearmpxm = QPixmap("trp/sp/arm2.png")
        self.timer = 0

    def addArm(self):
        self.h1 = Forearm("trp/sp/arm1.png", self.owner)
        self.h2 = Forearm("trp/sp/arm1.png", self.owner)
        self.h1.right = False
        self.h1.follow = self
        self.h2.follow = self
        self.h1.add()
        self.h2.add()
        self.h1.owner = self.owner
        self.h2.owner = self.owner
        self.lt = [0, 0]
        self.rt = [0, 0]
        at = random.randint(0, 1000)
        self.h1.anmtick = at
        at += 600
        if at > 1000:
            at -= 1000
        self.h2.anmtick = at

    def prePaint(self, painter):
        if self.drawArm:

            if glowstone.get_distance(self.pos[0], self.pos[1], self.larm[0], self.larm[1]) >= 159:
                self.larm = [self.pos[0] - 159 * glowstone.vec(glowstone.ag(self.pos[0] - self.larm[0], self.pos[1] - self.larm[1]))[0], self.pos[1] - 159 * glowstone.vec(glowstone.ag(self.pos[0] - self.larm[0], self.pos[1] - self.larm[1]))[1]]
            if glowstone.get_distance(self.pos[0], self.pos[1], self.rarm[0], self.rarm[1]) >= 159:
                self.rarm = [
                self.pos[0] - 159 * glowstone.vec(glowstone.ag(self.pos[0] - self.rarm[0], self.pos[1] - self.rarm[1]))[
                    0],
                self.pos[1] - 159 * glowstone.vec(glowstone.ag(self.pos[0] - self.rarm[0], self.pos[1] - self.rarm[1]))[
                    1]]

            self.drawArms(painter, self.pos[0], self.pos[1], self.larm[0], self.larm[1], False)
            self.drawArms(painter, self.pos[0], self.pos[1], self.rarm[0], self.rarm[1], True)
    def drawArms(self, painter, x1, y1, x2, y2, right=True):
        r1 = r2 = 80
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        n = False
        if d > r1 + r2:
            n = True

        if d < abs(r1 - r2):
            n = True
        if d == 0:
            return
        if not n and glowstone.get_distance(x1, y1, x2, y2) <= r1 + r2:
            a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(r1 ** 2 - a ** 2)
            x3 = x1 + a * (x2 - x1) / d
            y3 = y1 + a * (y2 - y1) / d
            x4 = x3 + h * (y2 - y1) / d
            y4 = y3 - h * (x2 - x1) / d
            if not right:
                dx, dy = x4, y4
            else:
                dx, dy = x4 - 2 * h * (y2 - y1) / d, y4 + 2 * h * (x2 - x1) / d
            self.drawPixmap(painter, self.armpxm, (x1, y1), glowstone.ag(dx - x1, dy - y1))
            self.drawPixmap(painter, self.forearmpxm, (dx, dy), glowstone.ag(x2 - dx, y2 - dy))
    def dfSet(self):
        tl = 165
        tl2 = 76
        self.lt = [
            self.pos[0] + glowstone.vec(self.getAngle())[0] * tl + glowstone.vec(self.getAngle() - 90)[0] * tl2,
            self.pos[1] + glowstone.vec(self.getAngle())[1] * tl + glowstone.vec(self.getAngle() - 90)[1] * tl2]
        self.rt = [
            self.pos[0] + glowstone.vec(self.getAngle())[0] * tl + glowstone.vec(self.getAngle() + 90)[0] * tl2,
            self.pos[1] + glowstone.vec(self.getAngle())[1] * tl + glowstone.vec(self.getAngle() + 90)[1] * tl2]
        self.larm = self.lt
        self.rarm = self.rt
    def update(self):
        super().update()
        self.timer += 1
        if self.timer == 4:
            self.dfSet()
        tl = 165
        tl2 = 76
        ls = 6
        mvl = [self.lt[0] - self.larm[0], self.lt[1] - self.larm[1]]
        mvr = [self.rt[0] - self.rarm[0], self.rt[1] - self.rarm[1]]
        if mvl[0] > ls:
            mvl[0] = ls
        if mvl[0] < -ls:
            mvl[0] = -ls
        if mvl[1] > ls:
            mvl[1] = ls
        if mvl[1] < -ls:
            mvl[1] = -ls
        if mvr[0] > ls:
            mvr[0] = ls
        if mvr[0] < -ls:
            mvr[0] = -ls
        if mvr[1] > ls:
            mvr[1] = ls
        if mvr[1] < -ls:
            mvr[1] = -ls
        self.larm = [self.larm[0] + mvl[0], self.larm[1] + mvl[1]]
        self.rarm = [self.rarm[0] + mvr[0], self.rarm[1] + mvr[1]]
        td = 140
        self.lta = [self.pos[0] + glowstone.vec(self.getAngle())[0] * tl + glowstone.vec(self.getAngle() - 90)[0] * tl2,
                    self.pos[1] + glowstone.vec(self.getAngle())[1] * tl + glowstone.vec(self.getAngle() - 90)[1] * tl2]
        self.rta = [
            self.pos[0] + glowstone.vec(self.getAngle())[0] * tl + glowstone.vec(self.getAngle() + 90)[0] * tl2,
            self.pos[1] + glowstone.vec(self.getAngle())[1] * tl + glowstone.vec(self.getAngle() + 90)[1] * tl2]
        if (glowstone.get_distance(self.lta[0], self.lta[1], self.larm[0], self.larm[1]) > td and self.rt == self.rarm) or glowstone.get_distance(self.lt[0], self.lt[1], self.lta[0], self.lta[1]) > 160:
            self.lt = self.lta
        if (glowstone.get_distance(self.rta[0], self.rta[1], self.rarm[0], self.rarm[1]) > td and self.lt == self.larm) or glowstone.get_distance(self.rt[0], self.rt[1], self.rta[0], self.rta[1]) > 160:
            self.rt = self.rta

        if glowstone.get_distance(self.pos[0], self.pos[1], self.larm[0], self.larm[1]) >= 160:
            self.larm = [
                self.pos[0] - 160 * glowstone.vec(glowstone.ag(self.pos[0] - self.larm[0], self.pos[1] - self.larm[1]))[
                    0],
                self.pos[1] - 160 * glowstone.vec(glowstone.ag(self.pos[0] - self.larm[0], self.pos[1] - self.larm[1]))[
                    1]]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.rarm[0], self.rarm[1]) >= 160:
            self.rarm = [
                self.pos[0] - 160 * glowstone.vec(glowstone.ag(self.pos[0] - self.rarm[0], self.pos[1] - self.rarm[1]))[
                    0],
                self.pos[1] - 160 * glowstone.vec(glowstone.ag(self.pos[0] - self.rarm[0], self.pos[1] - self.rarm[1]))[
                    1]]

        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]

class SP(DP):
    def __init__(self):
        super().__init__("trp/sp/head.png")
        self.length = 25
        self.tgp = [600, 600]
        self.dyj = 0.023
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 1.3
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        self.facingMouse = False
        for i in range(self.length):
            if set2:
                ap = SPBody("trp/sp/body2.png", self)
                if not i + 1 == self.length:
                    ap.drawArm = True
            else:
                ap = SPBody("trp/sp/body.png", self)

            set2 = not set2
            ap.follow = syg
            ap.pos = self.pos.copy()
            ap.dfSet()
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/sp/tail.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()

    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if self.facingMouse:
            self.setAngle(glowstone.ag(mouse.get_position()[0] - self.pos[0], mouse.get_position()[1] - self.pos[1]))
        else:
            if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 760:
                self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.4)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed

class DowBody(DPPart):
    def __init__(self, img):
        super().__init__(img)
        self.follow = None
        self.spacing = 116
    def update(self):
        super().update()
        self.setAngle(glowstone.ag(self.follow.pos[0] - self.pos[0], self.follow.pos[1] - self.pos[1]))
        self.pos = [self.follow.pos[0] - glowstone.vec(self.getAngle())[0] * self.spacing, self.follow.pos[1] - glowstone.vec(self.getAngle())[1] * self.spacing]
class DvOfWulfs(DP):
    def __init__(self):
        super().__init__("trp/dvw/dwh.png")
        self.length = 45
        self.tgp = [600, 600]
        self.dyj = 0.02
        self.dx = 0
        self.dy = 0
        self.moved = 1
        self.speed = 6
        syg = self
        set2 = True
        self.dx = 6
        bodies = []
        for i in range(self.length):
            ap = DogBody("trp/dvw/dwb.png")
            ap.owner = self

            set2 = not set2
            ap.follow = syg
            ap.add()
            bodies.append(ap)
            syg = ap

        ap.img = "trp/dvw/dwt.png"
        tn = len(bodies) - 1
        for i in range(len(bodies)):
            bodies[tn].top()
            tn -= 1
        self.top()
    def update(self):
        super().update()
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        if glowstone.get_distance(self.pos[0], self.pos[1], glowstone.screen_size()[0]/2, glowstone.screen_size()[1]/2) > 760:
            self.a = glowstone.rotateTo(self.a, glowstone.ag(glowstone.screen_size()[0]/2 - self.pos[0], glowstone.screen_size()[1]/2 - self.pos[1]), 0.6)
        self.dx = glowstone.vec(self.a)[0] * self.speed
        self.dy = glowstone.vec(self.a)[1] * self.speed
class Gozoma(DP):
    def __init__(self):
        super().__init__("")
        self.muti_img = True
        self.framesa = []
        self.framesb = []
        self.frameChangeTime = 2
        for i in range(518):
            n = str(i+1)
            if len(n) == 1:
                n = "00" + n
            if len(n) == 2:
                n = "0" + n
            self.framesa.append("trp/gzm/frame_{}.png".format(n))
            self.framesb.append("trp/gzm/fframe_{}.png".format(n))
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.tgt = [1000, 600]
        self.scale = [1, 1]

    def update(self):
        if self.dr:
            self.frames = self.framesb
        else:
            self.frames = self.framesa
        super().update()
        if random.randint(0, 200) == 0:
            self.tgt = [random.randint(0, glowstone.screen_size()[0]), random.randint(0, glowstone.screen_size()[1])]
        if glowstone.get_distance(self.pos[0], self.pos[1], self.tgt[0], self.tgt[1]) > 80:
            self.dx += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[0]
            self.dy += self.speed * glowstone.vec(glowstone.ag(self.tgt[0] - self.pos[0], self.tgt[1] - self.pos[1]))[1]
        self.dx *= 0.994
        self.dy *= 0.994
        self.dr = self.dx > 0
        self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]

class SlimeKing(DP):
    def __init__(self):
        super().__init__("trp/slimeking.png")
        self.scale = [1, 1]
        self.dx = 0
        self.dy = 0
        self.movet = 0
        self.dr = True
        self.speed = 0.03
        self.fr = 6
        self.timer = 0
    def update(self):
        super().update()
        sety = 130
        if random.randint(0, 160) == 0 and self.pos[1] == glowstone.screen_size()[1] - sety:
            self.dy = random.randint(-15, -5)
            self.dx *= 3
            self.fr = 6
            self.scale[1] = 1 - self.dy / 15 * 0.7
        if random.randint(0, 300) == 0:
            self.dr = random.randint(0,1) == 0
            self.movet = random.randint(100, 600)
        if self.pos[0] > glowstone.screen_size()[0]:
            self.dr = False
        if self.pos[0] < 0:
            self.dr = True
        if self.movet > 0:
            if self.dr:
                self.dx += self.speed
            else:
                self.dx -= self.speed
            self.movet -= 1
        if self.pos[1] < glowstone.screen_size()[1] - sety:
            self.dy += 0.2
        if self.pos[1] > glowstone.screen_size()[1] - sety:
            if self.dy > 0:
                self.dy = 0
                self.scale[1] = 1
            self.pos[1] = glowstone.screen_size()[1] - sety
        if self.pos[1] == glowstone.screen_size()[1] - sety:
            self.pos = [self.pos[0], self.pos[1] + self.dy]
        else:
            self.pos = [self.pos[0] + self.dx, self.pos[1] + self.dy]
        self.dx *= 0.992
        self.timer += 1
        self.scale[0] = 1 / self.scale[1]
        if self.scale[1] > 1:
            self.scale[1] -= (self.scale[1] - 1) / 60

#以下为桌宠的展示设置
class SpawnPetSet:
    def __init__(self):
        global displayObjs
        self.name = ""
        self.img = ""
        self.displayScale = 1
    def addNew(self):
        print("Error")
class CYGSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "极地冰灵"
        self.img = "trp/cryogen.png"
        self.displayScale = 0.5
    def addNew(self):
        Cryogen().add()
class CalCloneSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "灾厄之影"
        self.img = "trp/calaclone1.png"
        self.displayScale = 0.5
    def addNew(self):
        CalamitasClone().add()
class AQTSSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "渊海灾虫"
        self.img = "trp/aqs/display.png"
        self.displayScale = 0.4
    def addNew(self):
        AquaticScourge().add()
class ADSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "星神游龙"
        self.img = "trp/ad/display.png"
        self.displayScale = 0.4
    def addNew(self):
        AstrumDeus().add()

class CloverSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "Clover"
        self.img = "trp/cd/cd0.png"
        self.displayScale = 0.3
    def addNew(self):
        CloverDance().add()

class AsAuSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "白金星舰"
        self.img = "trp/astrumau/aa1.png"
        self.displayScale = 0.3
    def addNew(self):
        AstrumAureus().add()

class BrElSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "硫磺火元素"
        self.img = "trp/brel/fb1.png"
        self.displayScale = 0.6
    def addNew(self):
        BrimstoneElm().add()
class BirbSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "痴愚金龙"
        self.img = "trp/birb/b1.png"
        self.displayScale = 0.6
    def addNew(self):
        Birb().add()
class CVSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "无尽虚空"
        self.img = "trp/cv/c1.png"
        self.displayScale = 0.7
    def addNew(self):
        CrlsVoid().add()
class ClSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "菌生蟹"
        self.img = "trp/cl/c1.png"
        self.displayScale = 0.4
    def addNew(self):
        Crabulon().add()
class DsSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "荒漠灾虫"
        self.img = "trp/dss/display.png"
        self.displayScale = 0.44
    def addNew(self):
        DesertScourge().add()
class DogSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "神明吞噬者"
        self.img = "trp/dog/display.png"
        self.displayScale = 0.4
    def addNew(self):
        DvOfGods().add()

class AresSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "XF09-阿瑞斯"
        self.img = "trp/ars/xf09.png"
        self.displayScale = 0.4
    def addNew(self):
        Ares().add()
class ApolloSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "阿波罗"
        self.img = "trp/exeye/ap1.png"
        self.displayScale = 0.4
    def addNew(self):
        Apollo().add()
class ArtemisSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "阿尔忒弥斯"
        self.img = "trp/exeye/at1.png"
        self.displayScale = 0.4
    def addNew(self):
        Artemis().add()
class ThanatosSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "塔纳托斯"
        self.img = "trp/tnts/display.png"
        self.displayScale = 0.4
    def addNew(self):
        Thanatos().add()

class DreadonSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "嘉登"
        self.img = "trp/dd/d1.png"
        self.displayScale = 1
    def addNew(self):
        Draedon().add()
class ExoMcSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "星流巨械 全"
        self.img = "trp/exomc.png"
        self.displayScale = 0.23
    def addNew(self):
        Draedon().add()
        Ares().add()
        Apollo().add()
        Artemis().add()
        Thanatos().add()
class HiveMindSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "腐巢意志"
        self.img = "trp/hm/c1.png"
        self.displayScale = 0.8
    def addNew(self):
        HiveMind().add()
class AnhtSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "阿纳西塔"
        self.img = "trp/aal/a1.png"
        self.displayScale = 0.6
    def addNew(self):
        Anahita().add()
class LvtSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "利维坦"
        self.img = "trp/aal/l1.png"
        self.displayScale = 0.4
    def addNew(self):
        Lvt().add()
class OldDukeSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "硫海遗爵"
        self.img = "trp/od/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        OldDuke().add()

class PhSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "血肉宿主"
        self.img = "trp/ph/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        Perforator().add()
class PbgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "歌莉娅"
        self.img = "trp/gt/d1.png"
        self.displayScale = 0.5
    def addNew(self):
        PlaguebringerGoliath().add()
class PtgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "噬魂幽花"
        self.img = "trp/ptg/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        PolterGhast().add()

class PwSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "始源妖龙"
        self.img = "trp/pw/display.png"
        self.displayScale = 0.4
    def addNew(self):
        Pw().add()
class PvdSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "亵渎天神"
        self.img = "trp/pvd/p1.png"
        self.displayScale = 0.5
    def addNew(self):
        Providence().add()
class SgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "西格纳斯"
        self.img = "trp/sg/sg1.png"
        self.displayScale = 0.6
    def addNew(self):
        Signus().add()
class RavagerSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "毁灭魔像"
        self.img = "trp/ravager.png"
        self.displayScale = 0.37
    def addNew(self):
        Ravager().add()
class SlimeGodSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "史莱姆之神"
        self.img = "trp/sgod/core.png"
        self.displayScale = 1
    def addNew(self):
        CrimsonSlime().add()
        EbonianSlime().add()
        SlimeGod().add()

class StormWeaverSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "风暴编织者"
        self.img = "trp/sw/display.png"
        self.displayScale = 0.5
    def addNew(self):
        StormWeaver().add()

class EoCSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "克苏鲁之眼"
        self.img = "trp/ce.png"
        self.displayScale = 0.7
    def addNew(self):
        EOC().add()

class CalamitasSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "至尊灾厄"
        self.img = "trp/scl/fc0.png"
        self.displayScale = 1.8
    def addNew(self):
        Calamitas().add()

class YharpnSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "犽戎"
        self.img = "trp/yh/y1.png"
        self.displayScale = 0.3
    def addNew(self):
        Yharon().add()

class SPSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "灾坟魔物"
        self.img = "trp/sp/head.png"
        self.displayScale = 1.6
    def addNew(self):
        SP().add()

class DowSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "钨钢吞噬者"
        self.img = "trp/dvw/dwh.png"
        self.displayScale = 0.9
    def addNew(self):
        DvOfWulfs().add()

class GozomaSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "古泽玛"
        self.img = "trp/gzm/frame_001.png"
        self.displayScale = 0.4
    def addNew(self):
        Gozoma().add()
class SlimeKingSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "史莱姆王"
        self.img = "trp/slimeking.png"
        self.displayScale = 0.7
    def addNew(self):
        SlimeKing().add()

class KingBeeSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "蜂王"
        self.img = "trp/kb/b1.png"
        self.displayScale = 0.6
    def addNew(self):
        KingBee().add()

def addTrSets():
    #添加泰拉/灾厄的展示设置
    global displayObjs
    displayObjs.append(EoCSet())
    displayObjs.append(CYGSet())
    displayObjs.append(CalCloneSet())
    displayObjs.append(AQTSSet())
    displayObjs.append(ADSet())
    displayObjs.append(BrElSet())
    displayObjs.append(ClSet())
    displayObjs.append(DsSet())
    displayObjs.append(AsAuSet())
    displayObjs.append(KingBeeSet())
    displayObjs.append(BirbSet())
    displayObjs.append(CVSet())
    displayObjs.append(DogSet())
    displayObjs.append(SlimeGodSet())
    displayObjs.append(AresSet())
    displayObjs.append(ApolloSet())
    displayObjs.append(ArtemisSet())
    displayObjs.append(ThanatosSet())
    displayObjs.append(DreadonSet())
    displayObjs.append(ExoMcSet())
    displayObjs.append(CalamitasSet())
    displayObjs.append(HiveMindSet())
    displayObjs.append(PhSet())
    displayObjs.append(AnhtSet())
    displayObjs.append(LvtSet())
    displayObjs.append(OldDukeSet())
    displayObjs.append(PbgSet())
    displayObjs.append(PtgSet())
    displayObjs.append(PwSet())
    displayObjs.append(PvdSet())
    displayObjs.append(SgSet())
    displayObjs.append(RavagerSet())
    displayObjs.append(YharpnSet())
    displayObjs.append(StormWeaverSet())
    displayObjs.append(SPSet())
    displayObjs.append(GozomaSet())
    displayObjs.append(SlimeKingSet())


def addOtherSets():
    # 其余桌宠设置
    displayObjs.append(CloverSet())
    displayObjs.append(DowSet())


addTrSets()
# 打开菜单界面
def openWindow():
    global menuOpened
    menuOpened = True
    for i in distexts:
        i.obj.top()
        i.newadd.top()
    leftB.top()
    rightB.top()

class addButton(glowstone.Obj):
    # 打开菜单按钮
    def __init__(self, i):
        super().__init__(i)
        self.std = False
        self.tsz = 1
        self.tgtx = 0
        self.sty = 80
    def update(self):
        global menuOpened,thankMenuOpen
        super().update()
        if self.mouse_pointing():
            self.tsz = 1.2
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        if menuOpened:
            self.show = False
        elif not menuOpened:
            self.show = True
            if not self.std:
                self.std = True
                self.setPos(glowstone.screen_size()[0] - 20, self.sty)
                self.tgtx = glowstone.screen_size()[0] - 20
            if mouse.get_position()[0] > glowstone.screen_size()[0] - 42:
                self.tgtx = glowstone.screen_size()[0] - 20
            if mouse.get_position()[0] <= glowstone.screen_size()[0] - 42:
                self.tgtx = glowstone.screen_size()[0] + 40
            self.setPos(self.pos[0] + 0.12 * (self.tgtx - self.pos[0]), self.sty)
            if self.mouse_pressing() and self.show:
                openWindow()
                playSound("trp/op.mp3")
                thankMenuOpen = False

            if self.mouse_pressing(0x02):
                self.sty = mouse.get_position()[1]

class AddPet(glowstone.Obj):
    # 添加桌宠按钮
    def __init__(self, i):
        super().__init__(i)
        self.prsd = False
        self.ads = None
        self.tsz = 1

    def update(self):
        global menuOpened
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        if menuOpened:
            if self.mouse_pressing() and not self.prsd and self.show:
                self.prsd = True
                self.ads.addNew()
                self.tsz = 0
                playSound("trp/cls.mp3")

            if not glowstone.pressed():
                self.prsd = False
            if glowstone.pressed():
                self.prsd = True

class pageButton(glowstone.Obj):
    # 翻页按钮
    def __init__(self, i):
        super().__init__(i)
        self.right = True
        self.paged = False
        self.tsz = 1
    def update(self):
        global menuOpened, page, displayObjs
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        self.show = menuOpened
        if self.right:
            self.show = not page == math.ceil(len(displayObjs) / 6) and menuOpened
        else:
            self.show = not page == 1 and menuOpened
        if self.right:
            self.pos = [menu.pos[0] + 280, menu.pos[1] + 40]
        else:
            self.pos = [menu.pos[0] - 280, menu.pos[1] + 40]
        if menuOpened:
            if self.mouse_pressing() and not self.paged and self.show:
                self.paged = True
                playSound("trp/cls.mp3")
                if self.right:
                    page += 1
                else:
                    page -= 1
                self.tsz = 0
        if not glowstone.pressed():
            self.paged = False
        if glowstone.pressed():
            self.paged = True
        if page < 1:
            page = 1
        if page > math.ceil(len(displayObjs) / 6):
            page = math.ceil(len(displayObjs) / 6)

buttoncls = None
class Menu(glowstone.Obj):
    # 菜单
    def __init__(self, i):
        super().__init__(i)
        self.show = False
        self.pos = [500, 300]
        self.mpx = 0
        self.std = False
        self.mpy = 0
        self.prsd = False
    def update(self):
        global distexts
        super().update()
        if buttoncls.mouse_pressing():
            self.show = False
            return
        if menuOpened:
            self.show = True
        elif not menuOpened:
            self.show = False
        if self.mouse_pressing() and not self.prsd and not buttoncls.mouse_pressing() and not delt.mouse_pressing() and not buttonthank.mouse_pressing():
            if not self.std and self.pos[1] > mouse.get_position()[1] + 160:
                self.prsd = True
                self.std = True
                self.mpx = mouse.get_position()[0] - self.pos[0]
                self.mpy = mouse.get_position()[1] - self.pos[1]

        if self.prsd:
            self.setPos(mouse.get_position()[0] - self.mpx, mouse.get_position()[1] - self.mpy)
        if not glowstone.pressed():
            self.prsd = False
            self.std = False
        if glowstone.pressed():
            self.std = True
        self.top()
        for i in distexts:
            i.obj.top()
            i.newadd.top()
        delt.top()
        leftB.top()
        rightB.top()
        buttoncls.top()
        buttonthank.top()
        settingButton.top()
        buttonSd.top()
menu = Menu("trp/menu.png")

class PageShowText(glowstone.Text):
    # 当前页数文本
    def update(self):
        global page
        self.text = str(page) + "/" + str(math.ceil(len(displayObjs) / 6))
        self.show = menuOpened
        self.pos = [menu.pos[0] - 60, menu.pos[1] - 168]

pgs = PageShowText()
pgs.add()
class Dst(glowstone.Text):
    # 展示单元
    def __init__(self, txt=""):
        super().__init__(txt)
        self.posp = [0, 0]
        self.n = 0
        self.obj = glowstone.Obj("trp/none.png")
        self.obj.add()
        self.newadd = AddPet("trp/addButton.png")
        self.newadd.add()
    def update(self):
        super().update()
        self.obj.refreshPM()
        try:
            self.newadd.ads = displayObjs[(page - 1) * 6 + self.n]
            self.obj.pos = [self.pos[0] + 60, self.pos[1] - 80]
            self.obj.show = menuOpened
            self.newadd.pos = [self.pos[0] + 140, self.pos[1] - 12]
            self.newadd.show = menuOpened
            self.pos = [menu.pos[0] + self.posp[0], menu.pos[1] + self.posp[1]]
            self.show = menuOpened
            self.obj.scale = [displayObjs[(page - 1) * 6 + self.n].displayScale,
                              displayObjs[(page - 1) * 6 + self.n].displayScale]
            if page == math.ceil(len(displayObjs) / 2) and self.n > len(displayObjs) % 6:
                self.show = False
                self.obj.show = False
                self.newadd.show = False
            else:
                self.show = menuOpened
                self.obj.show = menuOpened
                self.newadd.show = menuOpened
                self.text = displayObjs[(page-1) * 6 + self.n].name
                self.obj.img = displayObjs[(page-1) * 6 + self.n].img
                self.obj.scale = [displayObjs[(page-1) * 6 + self.n].displayScale, displayObjs[(page-1) * 6 + self.n].displayScale]
                self.obj.refreshPM()
        except:
            self.text = ""
            self.show = False
            self.obj.show = False
            self.newadd.show = False

# 添加展示单元
for i in range(6):
    dst = Dst("")
    dst.size = 13
    distexts.append(dst)
    dst.add()
    dst.n = i

# 设置展示单元相对坐标
distexts[0].posp = [-290, -7]
distexts[1].posp = [-100, -7]
distexts[2].posp = [100, -7]
distexts[3].posp = [-290, 190]
distexts[4].posp = [-100, 190]
distexts[5].posp = [100, 190]

menu.add()

class closeButton(glowstone.Obj):
    # 关闭菜单按钮
    def __init__(self, i):
        super().__init__(i)
        self.std = False
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened
        super().update()
        if self.mouse_pointing():
            self.tsz = 1.2
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        if self.mouse_pressing() and menuOpened:
            menuOpened = False
            playSound("trp/cls.mp3")
        if menuOpened:
            self.show = True
        elif not menuOpened:
            self.show = False
        self.setPos(menu.pos[0] + 280, menu.pos[1] - 180)
class DelToggleButton(glowstone.Obj):
    # 切换删除模式按钮
    def __init__(self):
        super().__init__("trp/delmode.png")
        self.std = False
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened,deleteMode
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        if self.mouse_pressing() and not self.mpr and menuOpened:
            deleteMode = not deleteMode
            self.mpr = True
            self.tsz = 0.1
            if deleteMode:
                playSound("trp/op.mp3")
            else:
                playSound("trp/cls.mp3")
        if not glowstone.pressed():
            self.mpr = False
        if glowstone.pressed():
            self.mpr = True
        if menuOpened:
            self.show = True
        elif not menuOpened:
            self.show = False
        if deleteMode:
            self.img = "trp/delmodeon.png"
        else:
            self.img = "trp/delmode.png"
        self.refreshPM()
        self.setPos(menu.pos[0] + 230, menu.pos[1] - 180)
tkmenu = None
class STButton(glowstone.Obj):
    # 特别鸣谢按钮
    def __init__(self):
        super().__init__("trp/crd.png")
        self.std = False
        self.utm = 6
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened, thankMenuOpen, tkmenu
        super().update()
        if self.mouse_pointing():
            self.tsz = 1.2
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        if self.mouse_pressing() and self.utm > 0 and not self.mpr and self.show:
            thankMenuOpen = True
            self.mpr = True
            playSound("trp/op.mp3")
            tkmenu.mpr = True
            menuOpened = False
        if not glowstone.pressed():
            self.mpr = False
        if glowstone.pressed():
            self.mpr = True
        if menuOpened:
            self.show = True
            self.utm = 3
        self.utm -= 1
        self.setPos(menu.pos[0] + 180, menu.pos[1] - 180)
        if not menuOpened:
            self.show = False
settingOpend = False
class SettingButton(glowstone.Obj):
    # 切换额外桌宠按钮
    def __init__(self):
        super().__init__("trp/setting.png")
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened, thankMenuOpen, tkmenu, settingOpend, displayObjs
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        self.show = menuOpened
        if self.mouse_pressing() and not self.mpr and self.show:
            self.tsz = 0.1
            settingOpend = not settingOpend

            displayObjs = []
            addTrSets()
            if settingOpend:
                addOtherSets()
            if settingOpend:
                playSound("trp/op.mp3")
            else:
                playSound("trp/cls.mp3")
        if glowstone.pressed():
            self.mpr = True
        if not glowstone.pressed():
            self.mpr = False
        self.setPos(menu.pos[0] + 130, menu.pos[1] - 180)
        if settingOpend:
            self.img = "trp/settingon.png"
        else:
            self.img = "trp/setting.png"
        self.refreshPM()
class SoundButton(glowstone.Obj):
    # 切换音效是否开启按钮
    def __init__(self):
        super().__init__("trp/sd.png")
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened, pls,displayObjs
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        self.show = menuOpened
        if self.mouse_pressing() and not self.mpr:
            self.tsz = 0.1
            pls = not pls
            if pls:
                playSound("trp/op.mp3")
        if glowstone.pressed():
            self.mpr = True
        if not glowstone.pressed():
            self.mpr = False
        self.setPos(menu.pos[0] + 80, menu.pos[1] - 180)
        if pls:
            self.img = "trp/sd.png"
        else:
            self.img = "trp/sdc.png"
        self.refreshPM()
class Sttext(glowstone.Text):
    # 特别鸣谢文本
    def update(self):
        super().update()
        self.color = (255, 242, 0)
        self.show = thankMenuOpen and tkmenu.scale[0] >= 1


thanks = []

# 尝试读取特别鸣谢列表
try:
    tkr = open("trp/thanklist.txt", "r", encoding="GBK")
    tkr.seek(0, 0)
    r = tkr.read()
    thanks = r.split("\n")
    tkr.close()
except:
    try:
        tkr = open("trp/thanklist.txt", "r", encoding="UTF-8")
        tkr.seek(0, 0)
        r = tkr.read()
        thanks = r.split("\n")
        tkr.close()
    except:
        thanks = ["无法获取特别鸣谢列表"]

spos = [280, 400]
# 添加特别鸣谢文本
for i in thanks:
    stxtf = Sttext(i)
    stxtf.pos = spos.copy()
    stxtf.add()
    stxtf.size = 36
    if spos[0] == 280:
        spos[0] = 1000
    elif spos[0] == 1000:
        spos[0] = 280
        spos[1] += 66

class SpecialThanksL(glowstone.Obj):
    # 特别鸣谢标题
    def __init__(self):
        super().__init__("trp/special_thanks/stl1.png")
        self.muti_img = True
        self.frames = []
        for i in range(11):
            self.frames.append("trp/special_thanks/stl{}.png".format(i+1))
        self.frameChangeTime = 9
        self.scale = [3, 3]
    def update(self):
        global menuOpened, thankMenuOpen
        super().update()
        self.show = thankMenuOpen and tkmenu.scale[0] >= 1
        self.setPos(400, 300)
spct = SpecialThanksL()
spct.add()
class ThankMenu(glowstone.Obj):
    # 鸣谢窗口
    def __init__(self):
        super().__init__("trp/thanks.png")
        self.std = False
        self.mpr = True
        self.scale = [0, 0]
    def update(self):
        global menuOpened, thankMenuOpen
        super().update()
        if self.mouse_pressing() and not self.mpr:
            thankMenuOpen = False
            self.mpr = True
            playSound("trp/cls.mp3")
        if not glowstone.pressed():
            self.mpr = False
        if glowstone.pressed():
            self.mpr = True
        if thankMenuOpen:
            self.show = True
            if self.scale[0] < 1:
                self.scale[0] += 0.1
                self.scale[1] += 0.1

        elif not thankMenuOpen and self.scale[0] <= 0:
            self.show = False
        if not thankMenuOpen:
            if self.scale[0] > 0:
                self.scale[0] -= 0.1
                self.scale[1] -= 0.1
        self.top()
        spct.top()
        self.setPos(1000, 530)

#绿幕
# gb = glowstone.Obj("trp/gb.png")
# gb.add()
# gb.scale = [4, 4]
# gb.pos = [900, 500]

# 添加按钮
buttonadd = addButton("trp/addButton.png")
buttonadd.add()
buttonSd = SoundButton()
buttonSd.add()
delt = DelToggleButton()
delt.add()
buttoncls = closeButton("trp/closeButton.png")
buttoncls.add()
buttonthank = STButton()
buttonthank.add()
settingButton = SettingButton()
settingButton.add()
tkmenu = ThankMenu()
tkmenu.add()
leftB, rightB = pageButton("trp/left.png"), pageButton("trp/right.png")
leftB.right = False
rightB.right = True
leftB.add()
rightB.add()

# 启动窗口
glowstone.run_window()

#关闭后退出
glowstone.app_exit()