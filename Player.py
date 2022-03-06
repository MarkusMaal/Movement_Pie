import pygame as pie
import json, sys
from random import randint

class Level:
    def __init__(self, filename):
        # this variable contains every symbol that can be assigned to
        # a color or texture
        """
        # -?@!.,ä
        õü~|><_:;
        ¤%&/()=£$
        €{[]}*ˇ^\
        123456789
        0ABCDEFGH
        IJKLMNOPQ
        RSTUVWXYZ
        abcdefghi
        jklmnopqr
        stuvwxyz"
        """
        self.defaults = {"#": "white", " ": "black", "-": "gray", "?": "magenta", "@": "orange", "!": "yellow", ".": "violet", ",": "purple", "ä": "lightgray",
                              "õ": "silver", "ü": "dimgray", "~": "blue", "|": "brown", ">": "alicblue", "<": "antiquewhite", "_": "aqua", ":": "aquamarine", ";": "azure",
                              "¤": "beige", "%": "bisque", "&": "blanchedalmond", "/": "blueviolet", "(": "burlywood", ")": "cadetblue", "=": "chartreuse", "£": "chocolate", "$": "coral",
                              "€": "cornflowerblue", "{": "cornsilk", "[": "crimson", "]": "cyan", "}": "darkblue", "*": "darkcyan", "Ü": "darkgoldenrod", "^": "darkgreen", "\\": "darkkhaki",
                              "1": "darkmagenta", "2": "darkolivegreen", "3": "darkorange", "4": "darkorchid", "5": "darkred", "6": "darksalmon", "7": "darkseagreen", "8": "darkslateblue", "9": "darkslategray",
                              "0": "darkturquoise", "A": "darkviolet", "B": "deeppink", "C": "deepskyblue", "D": "dimgray", "E": "dodgerblue", "F": "firebrick", "G": "floralwhite", "H": "forestgreen",
                              "I": "fuchsia", "J": "grainsboro", "K": "ghostwhite", "L": "gold", "M": "goldenrod", "N": "green", "O": "greenyellow", "P": "honeydew", "Q": "hotpink",
                              "R": "indianred", "S": "indigo", "T": "ivory", "U": "khaki", "V": "lawngreen", "W": "lightblue", "X": "lightcoral", "Y": "lime", "Z": "limegreen",
                              "a": "linen", "b": "maroon", "c": "mediumaquamarine", "d": "mediumblue", "e": "midnightblue", "f": "mintcream", "g": "moccasin", "h": "navajowhite", "i": "navy",
                              "j": "olive", "k": "olivedrab", "l": "orangered", "m": "orchid", "n": "papayawhip", "o": "peachpuff", "p": "peru", "q": "pink", "r": "plum",
                              "s": "powderblue", "t": "rebeccapurple", "u": "royalblue", "v": "saddlebrown", "w": "snow", "x": "teal", "y": "tomato", "z": "wheat", "\"": "yellowgreen"}
        self.ValidTextures = self.defaults.copy()
        self.LoadCustom(filename)

    def SwitchMap(self, mapname):
        self.filename = mapname
        self.ValidTexture = self.defaults.copy()
        self.LoadCustom(self.filename)
    
    def LoadTexture(self):
        if not self.texture == ":":
            texturepack = pie.image.load(f"Maps/Textures/{self.texture}")
            # 10x3 tekstuurilehe laadimine
            i = 0
            for y in range(0, 11 * self.high, self.high):
                for x in range(0, 9 * self.wide, self.wide):
                    cpd = pie.Surface((self.wide, self.high))
                    cpd.blit(texturepack, (0, 0), (x, y, x + 50, y + 50))
                    # tekstuuriviitade abil saab luua sõnastiku
                    # millega on lihtne tekstuuridele viidata
                    #
                    # kui tekstuuriviidet ei eksisteeri, kasutatakse
                    # võtmena tekstuuri ID-d
                    self.ValidTextures[list(self.ValidTextures.keys())[i]] = cpd
                    i+=1
    
    def LoadCustom(self, filename):
        with open(f"Maps/{filename}", "r", encoding="windows-1252") as raw_json:
            # open json file and decode it
            json_data = json.loads(raw_json.read())
            self.name = json_data["name"]
            self.author = json_data["author"]
            self.x = json_data["x"]
            self.y = json_data["y"]
            self.x2 = json_data["x2"]
            self.y2= json_data["y2"]
            self.finish_x = json_data.get("finish_x", -1)
            self.finish_y = json_data.get("finish_y", -1)
            self.finish_x2 = json_data.get("finish_x2", -1)
            self.finish_y2 = json_data.get("finish_y2", -1)
            self.data = json_data["data"]
            self.texture = json_data.get("texture", ":")
            self.walls = []
            self.entities = []
            self.character = json_data.get("character", "--")
            self.character2 = json_data.get("character2", "--")
            self.bulletl = json_data.get("bulletl", "<")
            self.bulletr = json_data.get("bulletr", ">")
            self.gravity = json_data.get("gravity", 0)
            self.jump = json_data.get("jump", 0)
            self.script = json_data.get("script", [])
            self.high = json_data.get("high", 16)
            self.wide = json_data.get("wide", 8)
            self.LoadTexture()
            self.character = json_data.get("character", "@")
            self.shoot = json_data.get("shoot", self.data.copy())
            for ents in json_data.get("entities", []):
                coord_x = ents.split("x")[0]
                coord_y = ents.split("x")[1]
                if coord_x == "": coord_x = "0"
                if coord_y == "": coord_y = "0"
                coord_x = int(coord_x)
                coord_y = int(coord_y)
                ent_data = ents.split("x")[-1]
                self.entities.append([coord_x, coord_y, ent_data])
            for coordinate in json_data.get("walls", []):
                coords = coordinate.split("x")
                coord_x = coords[0]
                coord_y = coords[1]
                if coord_x == "": coord_x = "0"
                if coord_y == "": coord_y = "0"
                coord_xy = (int(coord_x), int(coord_y))
                self.walls.append(coord_xy)

    def ChangeData(self, xy, char):
        y = xy[1]
        x = xy[0]
        self.data[y] = self.data[y][:x] + char + self.data[y][x+1:]
    
    def Shoot(self, xy): self.ChangeData(xy, self.shoot[y][x])
    
    def GetData(self): return self.data.copy()
    
    def Draw(self, screen):
        for y, line in enumerate(self.data):
            for x, block in enumerate(line):
                if self.texture == ":":
                    pie.draw.rect(screen, self.ValidTextures[block], pie.Rect(x * self.wide, y * self.high, self.wide, self.high))
                else:
                    screen.blit(self.ValidTextures[block], (x * self.wide, y * self.high))
        return screen

    def DrawEntity(self, screen):
        for ent in self.entities:
            if self.texture == ":":
                pie.draw.rect(screen, self.ValidTextures[ent[2]], pie.Rect(ent[0] * self.wide, ent[1] * self.high, self.wide, self.high))
            else:
                screen.blit(self.ValidTextures[ent[2]], (ent[0] * self.wide, ent[1] * self.high))
        return screen

    def CheckEntCollide(self, entity):
        ca = self.entities[entity]
        for i, ent in enumerate(self.entities):
            if not i == entity:
                if ent[0] == ca[0] and ent[1] == ca[1]:
                    return True
        return False
    
    def MoveEntity(self, plr, mx, my):
        for i, ent in enumerate(self.entities):
            if ent[0] == plr.x + mx and ent[1] == plr.y + my:
                if mx == -1:
                    if plr.x + mx > 0:
                        self.entities[i][0] -= 1
                        if self.CheckEntCollide(i) or self.CheckEntityWalls(self.entities[i][0], self.entities[i][1]):
                            self.entities[i][0] += 1
                            plr.x += 1
                    else:
                        plr.x += 1
                elif mx == 1:
                    if plr.x + mx < len(self.data[0]) - 1:
                        self.entities[i][0] += 1
                        if self.CheckEntCollide(i) or self.CheckEntityWalls(self.entities[i][0], self.entities[i][1]):
                            self.entities[i][0] -= 1
                            plr.x -= 1
                    else:
                        plr.x -= 1
                elif my == -1:
                    if plr.y + my > 0:
                        self.entities[i][1] -= 1
                        if self.CheckEntCollide(i) or self.CheckEntityWalls(self.entities[i][0], self.entities[i][1]):
                            self.entities[i][1] += 1
                            plr.y += 1
                    else:
                        plr.y += 1
                elif my == 1:
                    if plr.y + my < len(self.data) - 1:
                        self.entities[i][1] += 1
                        if self.CheckEntCollide(i) or self.CheckEntityWalls(self.entities[i][0], self.entities[i][1]):
                            self.entities[i][1] -= 1
                            plr.y -= 1
                    else:
                        plr.y -= 1
        return plr
    
    def CheckEntityWalls(self, ent_x, ent_y):
        for wall in self.walls:
            if wall == (ent_x, ent_y):
                return True
        return False
    
    def Ifcheck(lvl, plr):
        backup_x = plr.bx
        backup_y = plr.by
        plr.bx = int(plr.bx)
        plr.by = int(plr.by)
        for line in lvl.script:
            exec(line)
        if not plr == None:
            if plr.x > len(lvl.data[0]) - 1:
                plr.x = len(lvl.data[0]) - 1
                plr.lx = int(plr.x)
            elif plr.x < 0:
                plr.x = 0
                plr.lx = 0
            if plr.y > len(lvl.data) - 1:
                plr.y = len(lvl.data) - 1
                plr.ly = int(plr.x)
            elif plr.y < 0:
                plr.y = 0
                plr.ly = 0
            if plr.bx > len(lvl.data[0]) - 1:
                plr.bullet = 0
            if plr.x == lvl.finish_x and plr.y == lvl.finish_y:
                plr.finished = True
        plr.bx = backup_x
        plr.by = backup_y
        return plr


class Player:
    def __init__(self, x, y, w, h, color, bcolor, shoot):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bullet = 0
        self.bx = -1
        self.by = -1
        self.lx = int(x)
        self.ly = int(y)
        self.jump = 0
        self.finished = False
        self.draw_texture = False
        self.color = color
        self.maxshoot = shoot
        self.shoot = shoot
        self.bcolor = bcolor
    
    def Draw(self, screen, plr):
        if not plr.finished:
            if not self.bullet == 0:
                self.MoveBullet()
                if not self.draw_texture and not self.bullet == 0:
                    pie.draw.rect(screen, self.bcolor[int(self.bullet)-1])
                elif not self.bullet == 0:
                    screen.blit(self.bcolor[int(self.bullet)-1], (int(self.bx) * self.w, int(self.by) * self.h))
            if not self.draw_texture:
                pie.draw.rect(screen, self.color, pie.Rect(self.x * self.w, self.y * self.h, self.w, self.h))
            else:
                screen.blit(self.color, (self.x * self.w, self.y * self.h))

    def CheckPlayerCollide(self, plr2):
        if self.x == plr2.x and self.y == plr2.y:
            self.x = self.lx
            self.y = self.ly
        if int(self.bx) == plr2.x and int(self.by) == plr2.y:
            return True
        return False

    def Fire(self, state):
        if self.bullet == 0:
            self.bullet = state
            self.bx = int(self.x)
            self.by = int(self.y)
    
    def Move(self, x, y, walls):
        if self.bullet == 0:
            self.lx = int(self.x)
            self.ly = int(self.y)
            self.x += x
            self.y += y
            self.CheckWall(walls)

    def MoveBullet(self):
        if self.bullet == 2:
            self.bx += 1/6
            if self.shoot <= 0:
                self.shoot = int(self.maxshoot)
                self.bullet = 0
            else:
                self.shoot -= 1/6
        elif self.bullet == 1:
            self.bx -= 1/6
            if self.shoot <= 0:
                self.shoot = int(self.maxshoot)
                self.bullet = 0
            else:
                self.shoot -= 1/6
        else:
            self.shoot = int(self.maxshoot)
        if self.bx < 0:
            self.bullet = 0

    def Teleport(self, x, y):
        self.x = x
        self.y = y
    
    def CheckWall(self, walls):
        for wall in walls:
            if wall == (self.x, self.y):
                self.x = int(self.lx)
                self.y = int(self.ly)
            elif wall == (int(self.bx), int(self.by)):
                self.bullet = 0
            elif wall == (int(self.bx)-1, int(self.by)) and self.bullet == 1:
                self.bullet = 0
            elif wall == (int(self.bx)+1, int(self.by)) and self.bullet == 2:
                self.bullet = 0


def Preview(name):
    level = Level(name)
    surf = pie.Surface((0, 0))
    try:
        surf = pie.Surface((level.wide * len(level.data[0]), level.high * len(level.data)))
        level.Draw(surf)
    except:
        pass
    return surf


def PlayCustom(name, character, character2, shoot, gmode, resolution, fullscreen):
    pie.mouse.set_visible(False)
    level = Level(name)
    if not level.character == "--":
        character = level.character
    if not level.character2 == "--":
        character2 = level.character2
    players = []
    if gmode == "single":
        players = [Player(level.x, level.y, level.wide, level.high, level.ValidTextures[character], (level.ValidTextures[level.bulletl], level.ValidTextures[level.bulletr]), shoot)]
        players[0].draw_texture = not level.texture == ":"
    elif gmode == "multi":
        players = [Player(level.x, level.y, level.wide, level.high, level.ValidTextures[character], (level.ValidTextures[level.bulletl], level.ValidTextures[level.bulletr]), shoot)]
        players.append(Player(level.x2, level.y2, level.wide, level.high, level.ValidTextures[character2], (level.ValidTextures[level.bulletl], level.ValidTextures[level.bulletr]), shoot))
        players[0].draw_texture = not level.texture == ":"
        players[1].draw_texture = not level.texture == ":"
    ctrl = 0
    if len(level.data) == 0:
        level.data.append([])
    old_resolution = resolution
    resolution = (len(level.data[0]) * level.wide, len(level.data) * level.high)

    pie.init()
    pie.display.set_caption(f"{level.name} by {level.author}")
    if hasattr(sys, 'getwindowsversion'):
        if sys.getwindowsversion().major >= 10:
            resolution = (resolution[0], len(level.data) * level.high + level.high)
    if not fullscreen:
        s = pie.display.set_mode(resolution)
        old_resolution = resolution
    else:
        s = pie.display.set_mode(old_resolution, pie.FULLSCREEN)

    keysdown = {"w": False, "a": False, "s": False, "d": False}
    dummy_plr = Player(0, 0, 0, 0, "black", "black", 0)
    clk = pie.time.Clock()
    update_cycle = 0
    while True:
        exit_all = False
        for e in pie.event.get():
            if e.type == pie.QUIT:
                exit_all = True
                pie.quit()
                break
            elif e.type == pie.KEYDOWN:
                if e.key == pie.K_ESCAPE:
                    exit_all = True
                    break
                elif e.key == pie.K_1:
                    ctrl = 0
                elif e.key == pie.K_2:
                    ctrl = 1
                elif e.key == pie.K_SPACE:
                    if not gmode == "headless": players[ctrl].Fire(2)
                elif e.key == pie.K_BACKSPACE:
                    if not gmode == "headless": players[ctrl].Fire(1)
                elif e.key == pie.K_UP and (not level.gravity == 1 or players[ctrl].jump == 0): keysdown["w"] = True
                elif e.key == pie.K_LEFT and (not level.gravity == 1 or players[ctrl].jump == 0): keysdown["a"] = True
                elif e.key == pie.K_DOWN: keysdown["s"] = True
                elif e.key == pie.K_RIGHT and (not level.gravity == 1 or players[ctrl].jump == 0): keysdown["d"] = True
            elif e.type == pie.KEYUP:
                if e.key == pie.K_UP: keysdown["w"] = False
                elif e.key == pie.K_LEFT: keysdown["a"] = False
                elif e.key == pie.K_DOWN and level.gravity == 0: keysdown["s"] = False
                elif e.key == pie.K_RIGHT: keysdown["d"] = False
        checkmore = False
        if not gmode == "headless" and update_cycle == 5:
            if players[ctrl].jump > 0 and not keysdown["w"]:
                players[ctrl].jump -= 1
            if level.gravity == 1:
                keysdown["s"] = True
                if level.jump == 0:
                    keysdown["w"] = False
            if keysdown["w"]:
                if not level.gravity == 1 or players[ctrl].jump < level.jump:
                    level.MoveEntity(players[ctrl], 0, -1)
                    players[ctrl].Move(0, -1, level.walls)
                    checkmore = True
                    players[ctrl].jump += 1
                    if level.gravity == 1 and keysdown["a"]:
                        level.MoveEntity(players[ctrl], -1, 0)
                        players[ctrl].Move(-1, 0, level.walls)
                    elif level.gravity == 1 and keysdown["d"]:
                        level.MoveEntity(players[ctrl], 1, 0)
                        players[ctrl].Move(1, 0, level.walls)
                else:
                    level.MoveEntity(players[ctrl], 0, 1)
                    players[ctrl].Move(0, 1, level.walls)
                    checkmore = True
                    if level.gravity == 1 and keysdown["a"]:
                        level.MoveEntity(players[ctrl], -1, 0)
                        players[ctrl].Move(-1, 0, level.walls)
                    elif level.gravity == 1 and keysdown["d"]:
                        level.MoveEntity(players[ctrl], 1, 0)
                        players[ctrl].Move(1, 0, level.walls)
            elif keysdown["a"]:
                if not level.gravity == 1 or players[ctrl].jump == 0:
                    level.MoveEntity(players[ctrl], -1, 0)
                    players[ctrl].Move(-1, 0, level.walls)
                    checkmore = True
                    if level.gravity == 1:
                        level.MoveEntity(players[ctrl], 0, 1)
                        players[ctrl].Move(0, 1, level.walls)
            elif keysdown["d"]:
                if not level.gravity == 1 or players[ctrl].jump == 0:
                    level.MoveEntity(players[ctrl], 1, 0)
                    players[ctrl].Move(1, 0, level.walls)
                    checkmore = True
                    if level.gravity == 1:
                        level.MoveEntity(players[ctrl], 0, 1)
                        players[ctrl].Move(0, 1, level.walls)
            elif keysdown["s"]:
                level.MoveEntity(players[ctrl], 0, 1)
                players[ctrl].Move(0, 1, level.walls)
                checkmore = True
                if level.gravity == 1 and keysdown["a"]:
                    level.MoveEntity(players[ctrl], -1, 0)
                    players[ctrl].Move(-1, 0, level.walls)
                elif level.gravity == 1 and keysdown["d"]:
                    level.MoveEntity(players[ctrl], 1, 0)
                    players[ctrl].Move(1, 0, level.walls)
            if checkmore: players[ctrl] = level.Ifcheck(players[ctrl])
        elif gmode == "headless":
            level.Ifcheck(None)
        update_cycle += 1
        if update_cycle == 6: update_cycle = 0
        if level.gravity == 1 and update_cycle == 5:
            for ent in level.entities:
                dummy_plr.x = ent[0]
                dummy_plr.y = ent[1] - 1
                level.MoveEntity(dummy_plr, 0, 1)
        if exit_all:
            break
        s.fill([128, 128, 128])
        surf = pie.Surface((len(level.data[0]) * level.wide, len(level.data) * level.high))
        level.Draw(surf)
        level.DrawEntity(surf)
        finished = 0
        for plr1 in players:
            for plr2 in players:
                if not plr1 == plr2:
                    if plr1.CheckPlayerCollide(plr2):
                        if not plr1.bullet == 0:
                            players.remove(plr2)
                        elif not plr2.bullet == 0:
                            players.remove(plr1)
        for plr in players:
            plr.Draw(surf, plr)
            plr = level.Ifcheck(plr)
            if plr.finished: finished += 1
            if update_cycle == 5:
                plr.CheckWall(level.walls)
        if resolution[1] < resolution[0]:
            new_height = int(resolution[1]*(old_resolution[0] / resolution[0]))
            s.blit(pie.transform.scale(surf, (old_resolution[0], new_height)), (0, (old_resolution[1] // 2 - new_height // 2)))
        else:
            new_width = resolution[0]*(old_resolution[1] / resolution[1])
            s.blit(pie.transform.scale(surf, (new_width, old_resolution[1])), ((old_resolution[0] // 2 - new_width // 2), 0))
        if not gmode == "headless" and players[ctrl].finished:
            ctrl += 1
            if ctrl > len(players) - 1:
                ctrl = 0
        if not gmode == "headless" and finished == len(players):
            break
        pie.display.flip()
        clk.tick(60)
