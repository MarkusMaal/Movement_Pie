import pygame as pie
from pygame import gfxdraw
from random import randint

class FsEntry:
    def __init__(self, filename, family, size, color):
        self.name = filename
        self.family = family
        self.size = size
        self.color = color
        self.render = self.GenText(family, size, filename, True, color)
        self.shadow = self.GenText(family, size, filename, True, "black")
    
    def GenText(self, family, size, text, antialias, color):
        return pie.font.SysFont(family, size, False, False).render(text, antialias, color)
    
    def DisplayText(self, screen, xy, disp_shadow = False):
        if disp_shadow:
            screen.blit(self.shadow, (xy[0] + 2, xy[1] + 2))
        screen.blit(self.render, xy)
    
    def ChangeText(self, text):
        self.name = text
        self.render = self.GenText(self.family, self.size, text, True, self.color)
        self.shadow = self.GenText(self.family, self.size, text, True, "black")

def ChangeColors(original, bg, fg):
    new = original
    for y in range(12):
        for x in range(8):
            borw = new.get_at((x, y))
            if borw == (255, 255, 255):
                gfxdraw.pixel(new, x, y, fg)
            else:
                gfxdraw.pixel(new, x, y, bg)
    return new

def SayMessage(message, s, resolution):
    savetext = FsEntry(message, "Lucida Console", 12, "white")
    green_level = 0
    blink_cycle = 0
    clk = pie.time.Clock()
    while True:
        qt = False
        for e2 in pie.event.get():
            if e2.type == pie.QUIT:
                qt = True
                break
            elif e2.type == pie.KEYDOWN:
                qt = True
                break
        if qt: break
        bg_col = (0, green_level, 255)
        green_level, blink_cycle = PulseBlue(green_level, blink_cycle, 3)
        pie.draw.rect(s, bg_col, pie.Rect(resolution[0] // 2 - 150, resolution[1] // 2 - 15, 300, 30))
        savetext.DisplayText(s, (resolution[0] // 2 - 140, resolution[1] // 2 - 5))
        pie.display.flip()
        clk.tick(60)

def PulseBlue(green_level, blink_cycle, speed):
    if blink_cycle == 0:
        green_level += speed
        if green_level > 128:
            green_level = 128
            blink_cycle = 1
    elif blink_cycle == 1:
        green_level -= speed
        if green_level < 0:
            green_level = 0
            blink_cycle = 0
    return green_level, blink_cycle

def RandomColor():
    return (randint(0, 128), randint(0, 128), randint(0, 129))

def FileName(s, caption, enable_blacklist = True):
    clk = pie.time.Clock()
    title = FsEntry(caption, "Lucida Console", 20, "white")
    text = FsEntry("", "Lucida Console", 12, "white")
    backspace_down = False
    delete_down = False
    pos_keys = {"left": False, "right": False}
    position = 4
    insert = True
    blacklist = {}
    if enable_blacklist: blacklist = {"/", "\\", "|", "?", ":", "!", "\"", "#", "%", "&", "(", ")", "*", "+", ",", ";", "<", ">", "=", "[", "]", "^", "`", "{", "}"}
    while True:
        for e in pie.event.get():
            if e.type == pie.QUIT:
                return None
                break
            elif e.type == pie.KEYDOWN:
                if e.key == pie.K_RETURN:
                    return text.name
                elif e.key == pie.K_ESCAPE:
                    return None
                elif e.key == pie.K_BACKSPACE:
                    backspace_down = True
                elif e.key == pie.K_DELETE:
                    delete_down = True
                elif e.key == pie.K_LEFT:
                    pos_keys["left"] = True
                elif e.key == pie.K_RIGHT:
                    pos_keys["right"] = True
                elif e.key == pie.K_END:
                    position = len(text.name)
                elif e.key == pie.K_HOME:
                    position = 0
                elif e.key == pie.K_INSERT:
                    insert = not insert
                elif e.key == pie.K_PAGEUP:
                    position -= len(text.name) // 4
                elif e.key == pie.K_PAGEDOWN:
                    position += len(text.name) // 4
                elif e.unicode in blacklist or e.key == pie.K_LSHIFT or e.key == pie.K_RSHIFT:
                    continue
                else:
                    if len(text.name) < 43:
                        if insert:
                            text.ChangeText(text.name[:position] + e.unicode + text.name[position:])
                        else:
                            text.ChangeText(text.name[:position] + e.unicode + text.name[position+1:])
                        position += 1
            elif e.type == pie.KEYUP:
                if e.key == pie.K_BACKSPACE:
                    backspace_down = False
                elif e.key == pie.K_DELETE:
                    delete_down = False
                elif e.key == pie.K_LEFT:
                    pos_keys["left"] = False
                elif e.key == pie.K_RIGHT:
                    pos_keys["right"] = False
        if backspace_down and position > 0:
            text.ChangeText(text.name[:position-1] + text.name[position:])
            position -= 1
        elif delete_down and position < len(text.name):
            text.ChangeText(text.name[:position] + text.name[position+1:])
        if pos_keys["left"]: position -= 1
        elif pos_keys["right"]: position += 1
        if position < 0:
            position = 0
        elif position > len(text.name):
            position = len(text.name)
        s.fill("black")
        title.DisplayText(s, (10, 20))
        pie.draw.rect(s, "midnightblue", pie.Rect(10, 50, 300, 16))
        if insert:
            pie.draw.rect(s, "white", pie.Rect(11+7*position, 50, 1, 16))
        else:
            pie.draw.rect(s, "white", pie.Rect(10+7*position, 50, 7, 16))
        text.DisplayText(s, (10, 50))
        pie.display.flip()
        clk.tick(15)
