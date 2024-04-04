
from PyQt5.QtGui import QPixmap
from NSDeskPet import DP, DPPart

import glowstone
import mouse
import random
import time
import math


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
        self.refreshPM()
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
class Goozma(DP): # goozma goozma goozma!!!
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
