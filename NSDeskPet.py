"""
NSDeskPet
原作者：B站  北极星Nighten
开放修改，可以二次分发
请勿用于盈利
"""
from re import L
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
import simplejson as json
from enum import Enum

pygame.init()
pygame.mixer.init()

class Language(Enum):
    ZH_HANS = 0
    EN_US = 1
    # ZH_APRILFOOL = 2
    
    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            # to cycle around
             index = 0
            #
            # to error out
            # raise StopIteration('end of enumeration reached')
        return members[index]

language: Language = Language.ZH_HANS;
loadedLanguages: dict[int, dict] = {}

class Language():
    
    @staticmethod
    def getLocalization() -> dict:
        global language
        global loadedLanguages
        
        if not (language.value in loadedLanguages):
            with open(f"localization/{language.name}.json", "r", encoding="UTF-8") as file:
                loadedLanguages[language.value] = json.load(file)
            
            file.close()
        
        return loadedLanguages.get(language.value, {});

    @staticmethod
    def loadKey(key: str) -> any:

        if not isinstance(key, str):
            raise TypeError("must be str qdnswfnnknkn")
        
        path: list[str] = key.split(".")
        
        start = path.pop(0)
        
        thing: any = Language.getLocalization().get(start, start)
        
        
        for i in path:
            if isinstance(thing, dict):
                thing = thing[i]
                continue;
            else:
                return thing

        return thing
        

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


from pets import *

#以下为桌宠的展示设置
class SpawnPetSet:
    def __init__(self):
        global displayObjs
        self.name = ""
        self.img = ""
        self.displayScale = 1
    def addNew(self):
        raise NotImplementedError()
class CYGSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.cryogen"
        self.img = "trp/cryogen.png"
        self.displayScale = 0.5
    def addNew(self):
        Cryogen().add()
class CalCloneSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.clamClone"
        self.img = "trp/calaclone1.png"
        self.displayScale = 0.5
    def addNew(self):
        CalamitasClone().add()
class AQTSSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.aquaticScoog"
        self.img = "trp/aqs/display.png"
        self.displayScale = 0.4
    def addNew(self):
        AquaticScourge().add()
class ADSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.deus"
        self.img = "trp/ad/display.png"
        self.displayScale = 0.4
    def addNew(self):
        AstrumDeus().add()

class CloverSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.clover"
        self.img = "trp/cd/cd0.png"
        self.displayScale = 0.3
    def addNew(self):
        CloverDance().add()

class AsAuSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.aureus"
        self.img = "trp/astrumau/aa1.png"
        self.displayScale = 0.3
    def addNew(self):
        AstrumAureus().add()

class BrElSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.brimmy"
        self.img = "trp/brel/fb1.png"
        self.displayScale = 0.6
    def addNew(self):
        BrimstoneElm().add()
class BirbSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.birb"
        self.img = "trp/birb/b1.png"
        self.displayScale = 0.6
    def addNew(self):
        Birb().add()
class CVSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.ceaseless"
        self.img = "trp/cv/c1.png"
        self.displayScale = 0.7
    def addNew(self):
        CrlsVoid().add()
class ClSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.crabulon"
        self.img = "trp/cl/c1.png"
        self.displayScale = 0.4
    def addNew(self):
        Crabulon().add()
class DsSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.desertScoog"
        self.img = "trp/dss/display.png"
        self.displayScale = 0.44
    def addNew(self):
        DesertScourge().add()
class DogSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.DoG"
        self.img = "trp/dog/display.png"
        self.displayScale = 0.4
    def addNew(self):
        DvOfGods().add()

class AresSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.ares"
        self.img = "trp/ars/xf09.png"
        self.displayScale = 0.4
    def addNew(self):
        Ares().add()
class ApolloSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.apollo"
        self.img = "trp/exeye/ap1.png"
        self.displayScale = 0.4
    def addNew(self):
        Apollo().add()
class ArtemisSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.artemis"
        self.img = "trp/exeye/at1.png"
        self.displayScale = 0.4
    def addNew(self):
        Artemis().add()
class ThanatosSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.thanatos"
        self.img = "trp/tnts/display.png"
        self.displayScale = 0.4
    def addNew(self):
        Thanatos().add()

class DreadonSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.drae"
        self.img = "trp/dd/d1.png"
        self.displayScale = 1
    def addNew(self):
        Draedon().add()
class ExoMcSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.exoMayhem"
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
        self.name = "pets.hive"
        self.img = "trp/hm/c1.png"
        self.displayScale = 0.8
    def addNew(self):
        HiveMind().add()
class AnhtSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.nahita"
        self.img = "trp/aal/a1.png"
        self.displayScale = 0.6
    def addNew(self):
        Anahita().add()
class LvtSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.leviathan"
        self.img = "trp/aal/l1.png"
        self.displayScale = 0.4
    def addNew(self):
        Lvt().add()
class OldDukeSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.oldDuke"
        self.img = "trp/od/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        OldDuke().add()

class PhSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.perf"
        self.img = "trp/ph/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        Perforator().add()
class PbgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.golia"
        self.img = "trp/gt/d1.png"
        self.displayScale = 0.5
    def addNew(self):
        PlaguebringerGoliath().add()
class PtgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.polter"
        self.img = "trp/ptg/l1.png"
        self.displayScale = 0.7
    def addNew(self):
        PolterGhast().add()

class PwSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.18plusWyrm"
        self.img = "trp/pw/display.png"
        self.displayScale = 0.4
    def addNew(self):
        Pw().add()
class PvdSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.prov"
        self.img = "trp/pvd/p1.png"
        self.displayScale = 0.5
    def addNew(self):
        Providence().add()
class SgSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.signus"
        self.img = "trp/sg/sg1.png"
        self.displayScale = 0.6
    def addNew(self):
        Signus().add()
class RavagerSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.ravager"
        self.img = "trp/ravager.png"
        self.displayScale = 0.37
    def addNew(self):
        Ravager().add()
class SlimeGodSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.slimegod"
        self.img = "trp/sgod/core.png"
        self.displayScale = 1
    def addNew(self):
        CrimsonSlime().add()
        EbonianSlime().add()
        SlimeGod().add()

class StormWeaverSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.weebaa"
        self.img = "trp/sw/display.png"
        self.displayScale = 0.5
    def addNew(self):
        StormWeaver().add()

class EoCSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.eoc"
        self.img = "trp/ce.png"
        self.displayScale = 0.7
    def addNew(self):
        EOC().add()

class CalamitasSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.clam"
        self.img = "trp/scl/fc0.png"
        self.displayScale = 1.8
    def addNew(self):
        Calamitas().add()

class YharpnSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.yharon"
        self.img = "trp/yh/y1.png"
        self.displayScale = 0.3
    def addNew(self):
        Yharon().add()

class SPSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.sepulcher"
        self.img = "trp/sp/head.png"
        self.displayScale = 1.6
    def addNew(self):
        SP().add()

class DowSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.wulfrumDevourer"
        self.img = "trp/dvw/dwh.png"
        self.displayScale = 0.9
    def addNew(self):
        DvOfWulfs().add()

class GozomaSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.goozma"
        self.img = "trp/gzm/frame_001.png"
        self.displayScale = 0.4
    def addNew(self):
        Goozma().add()
class SlimeKingSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.kingSlime"
        self.img = "trp/slimeking.png"
        self.displayScale = 0.7
    def addNew(self):
        SlimeKing().add()

class KingBeeSet(SpawnPetSet):
    def __init__(self):
        super().__init__()
        self.name = "pets.queenBee"
        self.img = "trp/kb/b1.png"
        self.displayScale = 0.6
    def addNew(self):
        KingBee().add()

def addTrSets(displayObjs: list):
    #添加泰拉/灾厄的展示设置
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


def addOtherSets(displayObjs: list):
    # 其余桌宠设置
    displayObjs.append(CloverSet())
    displayObjs.append(DowSet())

addTrSets(displayObjs)

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
                key = displayObjs[(page-1) * 6 + self.n].name;
                self.text = Language.loadKey(key)
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
class LanguageButton(glowstone.Obj): # YES
    # 切换音效是否开启按钮
    def __init__(self):
        super().__init__("trp/sd.png")
        self.mpr = False
        self.tsz = 1
    def update(self):
        global menuOpened, displayObjs, language
        super().update()
        if self.mouse_pointing() and self.tsz < 1.2:
            self.tsz += 0.1
        else:
            self.tsz = 1
        self.scale = [self.scale[0] + (self.tsz - self.scale[0])/10, self.scale[1] + (self.tsz - self.scale[1])/10]
        self.show = menuOpened
        if self.mouse_pressing() and not self.mpr:
            self.tsz = 0.1
            language = language.next();
        if glowstone.pressed():
            self.mpr = True
        if not glowstone.pressed():
            self.mpr = False
        self.setPos(menu.pos[0] + 230, menu.pos[1] - 200)
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
languageButton = LanguageButton()
languageButton.add()
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
