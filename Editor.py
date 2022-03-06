from Common import *
from random import randint
import pygame as pie
import os, json

class PlayerMap:
    def __init__(self, filename, screen):
        self.filename = filename
        self.disp = screen
        if not self.filename.lower().endswith(".json"):
            self.filename += ".json"
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
        self.convert_mode = False
        self.batch_chars = """# -?@!.,„ä~|><_:;%&/()=${[]}*?^\\123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"€‚…†‡‰‹¨ˇ¸‘’“”•–—™›¯˛ ¢£¤¦§Ø©Ŗ«¬­®Æ°±²³´µ¶·ø¹»¼½¾æĄĮĀĆÅĘĒČÉŹĖĢĶĻŠŃŅÓŌÕÖ×ŁŚŪÜŻŽßąįćäåęēčéźėķīļšńņóōõ÷ųłųłśūüżŗÄĪŲāģöž+0"""
        self.ValidTextures = {"#": "white", " ": "black", "-": "gray", "?": "magenta", "@": "orange", "!": "yellow", ".": "violet", ",": "purple", "ä": "lightgray",
                              "õ": (200, 224, 224), "ü": "dimgray", "~": "blue", "|": "brown", ">": "alicblue", "<": "antiquewhite", "_": "aqua", ":": "aquamarine", ";": "azure",
                              "¤": "beige", "%": "bisque", "&": "blanchedalmond", "/": "blueviolet", "(": "burlywood", ")": "cadetblue", "=": "chartreuse", "£": "chocolate", "$": "coral",
                              "€": "cornflowerblue", "{": "cornsilk", "[": "crimson", "]": "cyan", "}": "darkblue", "*": "darkcyan", "Ü": "darkgoldenrod", "^": "darkgreen", "\\": "darkkhaki",
                              "1": "darkmagenta", "2": "darkolivegreen", "3": "darkorange", "4": "darkorchid", "5": "darkred", "6": "darksalmon", "7": "darkseagreen", "8": "darkslateblue", "9": "darkslategray",
                              "0": "darkturquoise", "A": "darkviolet", "B": "deeppink", "C": "deepskyblue", "D": "dimgray", "E": "dodgerblue", "F": "firebrick", "G": "floralwhite", "H": "forestgreen",
                              "I": "fuchsia", "J": "grainsboro", "K": "ghostwhite", "L": "gold", "M": "goldenrod", "N": "green", "O": "greenyellow", "P": "honeydew", "Q": "hotpink",
                              "R": "indianred", "S": "indigo", "T": "ivory", "U": "khaki", "V": "lawngreen", "W": "lightblue", "X": "lightcoral", "Y": "lime", "Z": "limegreen",
                              "a": "linen", "b": "maroon", "c": "mediumaquamarine", "d": "mediumblue", "e": "midnightblue", "f": "mintcream", "g": "moccasin", "h": "navajowhite", "i": "navy",
                              "j": "olive", "k": "olivedrab", "l": "orangered", "m": "orchid", "n": "papayawhip", "o": "peachpuff", "p": "peru", "q": "pink", "r": "plum",
                              "s": "powderblue", "t": "rebeccapurple", "u": "royalblue", "v": "saddlebrown", "w": "snow", "x": "teal", "y": "tomato", "z": "wheat", "\"": "yellowgreen"}
    
    def CreateMap(self):
        s = self.disp
        self.name = FileName(s, "Set map name (not filename)")
        self.author = FileName(s, "Set author's name")
        self.ChooseTexture(s)
        self.data = ["#"]
        self.x = 1
        self.y = 1
        self.x2 = 1
        self.y2 = 1
        self.finish_x = -1
        self.finish_y = -1
        self.finish_x2 = -1
        self.finish_y2 = -1
        self.walls = []
        self.script = []
        self.entities = []
        self.high = 24
        self.wide = 16
        self.gravity = 0
        self.jump = 0
        self.high, self.wide = self.SetTextureDims()
        self.LoadTexture()
        self.SetSize()
        self.Save()
    
    def ChooseTexture(self, s):
        caption = FsEntry("Choose texture file:", "Lucida Console", 20, "white")
        texture_entries = []
        for file in os.listdir("./Maps/Textures"):
            if file.endswith(".png"):
                texture_entries.append(FsEntry(file, "Lucida Console", 12, "white"))
        stop = False
        select = 0
        clk = pie.time.Clock()
        self.texture = ""
        while self.texture == "":
            for e in pie.event.get():
                if e.type == pie.QUIT:
                    stop = True
                elif e.type == pie.KEYDOWN:
                    if e.key == pie.K_UP:
                        select -= 1
                    elif e.key == pie.K_DOWN:
                        select += 1
                    elif e.key == pie.K_RETURN:
                        self.texture = texture_entries[select].name
            if stop: break
            s.fill("midnightblue")
            caption.DisplayText(s, (10, 10))
            if select < 0:
                select = len(texture_entries) - 1
            elif select > len(texture_entries) - 1:
                select = 0
            for i, entry in enumerate(texture_entries):
                if select == i:
                    pie.draw.rect(s, "blue", pie.Rect(10, 40 + i * 10, 200, 10))
                entry.DisplayText(s, (10, 40 + i * 10))
            pie.display.flip()
            clk.tick(60)
            
    def Fill(self, compare, target, x, y, kind):
        # fill either blocks or wall positions
        backup = None
        if kind == "rng":
            backup = tuple(target)
            target = target[randint(0, len(target) - 1)]
        if compare == target and not kind == "rng":
            return
        if x > len(self.data[0]) - 1: return
        elif y > len(self.data) - 1: return
        elif x < 0: return
        elif y < 0: return
        if kind == "block" or kind == "rng":
            self.data[y] = self.data[y][:x] + target + self.data[y][x+1:]
        elif kind == "wall":
            if not (x, y) in self.walls: self.walls.append((x, y))
            else: return
        # There is some recursion here.
        # To understand it, you must understand the
        # fourth word from the previous sentence.
        if x > 0 and self.data[y][x - 1] == compare:
            if not kind == "rng":
                self.Fill(compare, target, x - 1, y, kind)
            else:
                self.Fill(compare, backup, x - 1, y, kind)
        if x < len(self.data[y]) - 1 and self.data[y][x + 1] == compare:
            if not kind == "rng":
                self.Fill(compare, target, x + 1, y, kind)
            else:
                self.Fill(compare, backup, x + 1, y, kind)
        if y > 0 and self.data[y - 1][x] == compare:
            if not kind == "rng":
                self.Fill(compare, target, x, y - 1, kind)
            else:
                self.Fill(compare, backup, x, y - 1, kind)
        if y < len(self.data) - 1 and self.data[y + 1][x] == compare:
            if not kind == "rng":
                self.Fill(compare, target, x, y + 1, kind)
            else:
                self.Fill(compare, backup, x, y + 1, kind)
    
    def Save(self):
        with open(f"Maps/{self.filename}", "w", encoding="windows-1252") as file:
            file.write("{\n")
            file.write(f"\t\"name\": \"{self.name}\",\n")
            file.write(f"\t\"author\": \"{self.author}\",\n")
            file.write(f"\t\"texture\": \"{self.texture}\",\n")
            file.write(f"\t\"x\": {self.x},\n")
            file.write(f"\t\"y\": {self.y},\n")
            file.write(f"\t\"x2\": {self.x2},\n")
            file.write(f"\t\"y2\": {self.y2},\n")
            self.bulletl = self.bulletl.replace("\\", "\\\\").replace("\"", "\\\"")
            self.bulletr = self.bulletr.replace("\\", "\\\\").replace("\"", "\\\"")
            self.character = self.character.replace("\\", "\\\\").replace("\"", "\\\"")
            self.character2 = self.character2.replace("\\", "\\\\").replace("\"", "\\\"")
            if self.convert_mode: file.write(f"\t\"character\": \"{self.character}\",\n")
            if self.convert_mode: file.write(f"\t\"character2\": \"{self.character2}\",\n")
            if self.convert_mode: file.write(f"\t\"bulletl\": \"{self.bulletl}\",\n")
            if self.convert_mode: file.write(f"\t\"bulletr\": \"{self.bulletr}\",\n")
            if not self.finish_x == -1: file.write(f"\t\"finish_x\": {self.finish_x},\n")
            if not self.finish_y == -1: file.write(f"\t\"finish_y\": {self.finish_y},\n")
            if not self.finish_x2 == -1: file.write(f"\t\"finish_x2\": {self.finish_x2},\n")
            if not self.finish_y2 == -1: file.write(f"\t\"finish_y2\": {self.finish_y2},\n")
            file.write(f"\t\"high\": {self.high},\n")
            file.write(f"\t\"wide\": {self.wide},\n")
            file.write(f"\t\"gravity\": {self.gravity},\n")
            file.write(f"\t\"jump\": {self.jump},\n")
            file.write("\t\"data\": [\n")
            for i, line in enumerate(self.data):
                file.write(f"\t\t\"")
                for char in line:
                    try:
                        file.write(char)
                    except:
                        file.write(" ")
                        print(f"Failed to write {char}")
                file.write("\"")
                if i < len(self.data) - 1:
                    file.write(",")
                file.write("\n")
            file.write("\t]")
            if not len(self.walls) + len(self.script) + len(self.entities) == 0:
                file.write(",")
            file.write("\n")
            if len(self.entities) > 0:
                file.write("\t\"entities\": [\n\t\t")
                for i, ent in enumerate(self.entities):
                    ent_str = f"{ent[0]}x{ent[1]}x{ent[2]}"
                    try:
                        file.write(f"\"{ent_str}\"")
                    except:
                        file.write(f"\"?\"")
                    if i < len(self.entities) - 1:
                        file.write(", ")
                file.write("\n\t]")
                if len(self.walls) + len(self.script) > 0:
                    file.write(",\n")
                else:
                    file.write("\n")
            if len(self.walls) > 0:
                file.write("\t\"walls\": [\n\t\t")
                for i, wall in enumerate(self.walls):
                    wall_strx = str(wall[0])
                    wall_stry = str(wall[1])
                    if wall_strx == "0": wall_strx = ""
                    if wall_stry == "0": wall_stry = ""
                    wall_str = wall_strx + "x" + wall_stry
                    file.write(f"\"{wall_str}\"")
                    if i < len(self.walls) - 1:
                        file.write(", ")
                file.write("\n\t]")
                if len(self.script) > 0:
                    file.write(",\n")
                else:
                    file.write("\n")
            if len(self.script) > 0:
                file.write("\t\"script\": [\n")
                for i, line in enumerate(self.script):
                    file.write(f"\t\t\"{line}\"")
                    if i < len(self.script) - 1:
                        file.write(",\n")
                    else:
                        file.write("\n")
                file.write("\t]\n")
            file.write("}")
            
    
    def SetTextureDims(self):
        s = self.disp
        caption = FsEntry(f"Set texture dimensions ({self.wide}x{self.high})", "Lucida Console", 20, "white")
        subtext = FsEntry("This specifies how many pixels long and high one texture is on the texture map", "Lucida Console", 12, "white")
        text_w = self.wide
        text_h = self.high
        done = False
        clk = pie.time.Clock()
        while True:
            for e in pie.event.get():
                if e.type == pie.QUIT:
                    stop = True
                elif e.type == pie.KEYDOWN:
                    if e.key == pie.K_UP:
                        text_h -= 1
                        caption.ChangeText(f"Set texture dimensions ({text_w}x{text_h})")
                    elif e.key == pie.K_DOWN:
                        text_h += 1
                        caption.ChangeText(f"Set texture dimensions ({text_w}x{text_h})")
                    elif e.key == pie.K_LEFT:
                        text_w -= 1
                        caption.ChangeText(f"Set texture dimensions ({text_w}x{text_h})")
                    elif e.key == pie.K_RIGHT:
                        text_w += 1
                        caption.ChangeText(f"Set texture dimensions ({text_w}x{text_h})")
                    elif e.key == pie.K_RETURN:
                        done = True
                        break
            if done:
                return int(text_h), int(text_w)
            s.fill("midnightblue")
            caption.DisplayText(s, (10, 10))
            subtext.DisplayText(s, (10, 35))
            for y in range(0, text_h * 4, 4):
                for x in range(0, text_w * 4, 4):
                    if x // 4 < self.wide and y // 4 < self.high:
                        pie.draw.rect(s, "white", pie.Rect(x+10, y+50, 2, 2))
                    else:
                        pie.draw.rect(s, "yellow", pie.Rect(x+10, y+50, 2, 2))
            pie.display.flip()
            clk.tick(60)
        return
    
    def SetWall(self, x, y):
        if (x, y) in self.walls:
            self.walls.remove((x, y))
        else:
            self.walls.append((x, y))
    
    def GravitySetup(self, resolution):
        s = self.disp
        def1, def2, def3 = "Lucida Console", 10, "white"
        grav_s = "disabled"
        if self.gravity > 0:
            grav_s = "enabled"
        bg_color = RandomColor()
        gravity_menu = [FsEntry(f"Gravity status: {grav_s}", def1, def2, def3),
                        FsEntry(f"Jumping power: {self.jump}", def1, def2, def3),
                        FsEntry(f"Return to editor", def1, def2, def3)]
        ex_g = False
        select = 0
        blink_cycle = 0
        green_level = 0
        sel_col = (0, green_level, 255)
        clk = pie.time.Clock()
        pie.mouse.set_visible(True)
        trigger = False
        direction = 1
        antibounce = 0
        while not ex_g:
            for e in pie.event.get():
                if e.type == pie.QUIT:
                    ex_g = True
                    break
                elif e.type == pie.KEYDOWN:
                    if e.key == pie.K_UP:
                        select -= 1
                    elif e.key == pie.K_DOWN:
                        select += 1
                    elif e.key == pie.K_ESCAPE:
                        ex_g = True
                        break
                    elif e.key == pie.K_RIGHT:
                        trigger = True
                        direction = 1
                    elif e.key == pie.K_LEFT:
                        trigger = True
                        direction = -1
                    elif e.key == pie.K_RETURN:
                        trigger = True
                        direction = 1
            box_dims = 160, 40
            bx, by = resolution[0] // 2 - box_dims[0]//2, resolution[1] // 2 - box_dims[1]//2
            pie.draw.rect(s, bg_color, pie.Rect(bx, by, box_dims[0], box_dims[1]))
            list_start = by + 5
            if select > len(gravity_menu) - 1:
                select = 0
            elif select < 0:
                select = len(gravity_menu) - 1
            green_level, blink_cycle = PulseBlue(green_level, blink_cycle, 4)
            sel_col = (0, green_level, 255)
            mouse = pie.mouse.get_pos()
            if mouse[0] > bx + 5 and mouse[0] < bx + box_dims[0] - 5:
                if mouse[1] > by + 5 and mouse[1] < by + box_dims[1] - 5:
                    select = (mouse[1] - by - 5) // 10
            if pie.mouse.get_pressed()[0] and antibounce == 0:
                trigger = True
                direction = 1
            elif pie.mouse.get_pressed()[-1] and antibounce == 0:
                trigger = True
                direction = -1
            if antibounce > 0:
                antibounce -= 1
            if trigger:
                trigger = False
                antibounce = 10
                if select == 0:
                    if self.gravity == 0:
                        self.gravity = 1
                    else:
                        self.gravity = 0
                    grav_s = "disabled"
                    if self.gravity > 0:
                        grav_s = "enabled"
                elif select == 1:
                    self.jump += direction
                    if self.jump == 6:
                        self.jump = 0
                    elif self.jump < 0:
                        self.jump = 5
                elif select == 2:
                    break
                gravity_menu[0].ChangeText(f"Gravity status: {grav_s}")
                gravity_menu[1].ChangeText(f"Jumping power: {self.jump}")
            for i in range(len(gravity_menu)):
                if i == select:
                    pie.draw.rect(s, sel_col, pie.Rect(bx + 5, list_start + 10 * i, box_dims[0] - 10, 10))
                gravity_menu[i].DisplayText(s, (bx + 5, list_start + 10 * i))
            pie.display.flip()
            clk.tick(60)
    def SetSize(self):
        s = self.disp
        data_w = len(self.data[0])
        data_h = len(self.data)
        caption = FsEntry(f"Set map size ({data_w}x{data_h})", "Lucida Console", 20, "white")
        done = False
        clk = pie.time.Clock()
        stop = False
        while True:
            for e in pie.event.get():
                if e.type == pie.QUIT:
                    stop = True
                elif e.type == pie.KEYDOWN:
                    if e.key == pie.K_UP:
                        data_h -= 1
                        caption.ChangeText(f"Set map size ({data_w}x{data_h})")
                    elif e.key == pie.K_DOWN:
                        data_h += 1
                        caption.ChangeText(f"Set map size ({data_w}x{data_h})")
                    elif e.key == pie.K_LEFT:
                        data_w -= 1
                        caption.ChangeText(f"Set map size ({data_w}x{data_h})")
                    elif e.key == pie.K_RIGHT:
                        data_w += 1
                        caption.ChangeText(f"Set map size ({data_w}x{data_h})")
                    elif e.key == pie.K_RETURN:
                        done = True
                        break
            if stop:
                break
            if done:
                done = False
                new_data = []
                for y in range(0, data_h):
                    new_line = ""
                    for x in range(0, data_w):
                        if x < len(self.data[0]) and y < len(self.data):
                            new_line += self.data[y][x]
                        else:
                            new_line += "#"
                    new_data.append(new_line)
                self.data = new_data.copy()
                break
            s.fill("midnightblue")
            caption.DisplayText(s, (10, 10))
            for y in range(0, data_h * self.high, self.high):
                for x in range(0, data_w * self.wide, self.wide):
                    col = ""
                    if x // self.wide < len(self.data[0]) and y // self.high < len(self.data):
                        if data_w < len(self.data[0]) or data_h < len(self.data):
                            col = "red"
                        else:
                            col = "white"
                    else:
                        col = (0, 255, 0)
                    pie.draw.rect(s, col, pie.Rect(x+10, y+40, self.wide//2, self.high//2))
            pie.display.flip()
            clk.tick(60)

        if stop:
            return
    
    def LoadBatchFile(self, filename):
        split = 20
        self.name = filename.replace(".cmd", "")
        self.LoadBatchTexture()
        with open(filename, "r", encoding="windows-1252") as file:
            for line in file:
                if line.lower().startswith("set color="):
                    split = 40
        with open(filename, "r", encoding="windows-1252") as file:
            lasty = 0
            self.data = []
            data_line = ""
            self.finish_x = -1
            self.finish_x2 = -1
            self.finish_y = -1
            self.finish_y2 = -1
            self.walls = []
            self.script = []
            for line in file:
                line_ident = line.split("=")[0].lower().replace("set /a ", "").replace("set ", "")
                line_value = line.split("=")[1].replace("\r\n", "").replace("\r", "").replace("\n", "")
                if line_ident == "author":
                    self.author = line_value
                elif line_ident.startswith("a"):
                    # convert 1D coordinates to 2D
                    coord_x0 = int(line_ident[1:])
                    coord_y = coord_x0 // split
                    coord_x = coord_x0 - coord_y * split
                    data_line += line_value
                    if not coord_y == lasty:
                        self.data.append(data_line)
                        lasty = int(coord_y)
                        data_line = ""
                elif line_ident == "start":
                    if not "+" in line_value:
                        self.y = int(line_value) // split
                        self.x = int(line_value) - self.y * split
                    else:
                        self.y = int(line_value.split("+")[0]) // split
                        self.x = int(line_value.split("+")[0]) - self.y * split
                elif line_ident == "start2":
                    if not "+" in line_value:
                        self.y2 = int(line_value) // split
                        self.x2 = int(line_value) - self.y2 * split
                    else:
                        self.y2 = int(line_value.split("+")[0]) // split
                        self.x2 = int(line_value.split("+")[0]) - self.y2 * split
                elif line_ident == "finish":
                    if not "+" in line_value:
                        self.finish_y = int(line_value) // split
                        self.finish_x = int(line_value) - self.finish_y * split
                    else:
                        self.finish_y = int(line_value.split("+")[0]) // split
                        self.finish_x = int(line_value.split("+")[0]) - self.finish_y * split
                elif line_ident == "finish2":
                    if not "+" in line_value:
                        self.finish_y2 = int(line_value) // split
                        self.finish_x2 = int(line_value) - self.finish_y2 * split
                    else:
                        self.finish_y2 = int(line_value.split("+")[0]) // split
                        self.finish_x2 = int(line_value.split("+")[0]) - self.finish_y2 * split
                        
    
    def LoadBatchTexture(self):
        texturepack = pie.image.load(f"Maps/Textures/batch_file.png")
        self.texture = "batch_file.png"
        i = 0
        self.wide = 8
        self.high = 12
        for x in range(0, len(self.batch_chars) * self.wide, self.wide):
            cpd = pie.Surface((self.wide, self.high))
            cpd.blit(texturepack, (0, 0), (x, 0, x + self.wide, self.high))
            self.ValidTextures[self.batch_chars[i]] = cpd
            i+=1
            
    def LoadTexture(self):
        if not self.texture == ":":
            texturepack = pie.image.load(f"Maps/Textures/{self.texture}")
            # 10x3 tekstuurilehe laadimine
            i = 0
            for y in range(0, 11 * self.high, self.high):
                for x in range(0, 9 * self.wide, self.wide):
                    cpd = pie.Surface((self.wide, self.high))
                    cpd.blit(texturepack, (0, 0), (x, y, x + 50, y + 50))
                    self.ValidTextures[list(self.ValidTextures.keys())[i]] = cpd
                    i+=1
    
    def Draw(self):
        surf = pie.Surface((self.wide * len(self.data[0]), self.high * len(self.data)))
        for y, line in enumerate(self.data):
            for x, block in enumerate(line):
                if self.texture == ":":
                    pie.draw.rect(surf, self.ValidTextures[block], pie.Rect(x * self.wide, y * self.high, self.wide, self.high))
                else:
                    try:
                        surf.blit(self.ValidTextures[block.replace("Û", "Ū")], (x * self.wide, y * self.high))
                    except:
                        pass
        return surf
    
    def DrawEntity(self, surf):
        for ent in self.entities:
            if self.texture == ":":
                pie.draw.rect(surf, self.ValidTextures[ent[2]], pie.Rect(ent[0] * self.wide, ent[1] * self.high, self.wide, self.high))
            else:
                surf.blit(self.ValidTextures[ent[2]], (ent[0] * self.wide, ent[1] * self.high))
        return surf
    
    def DrawPallette(self, pallette):
        surf = pie.Surface((4 * self.wide, self.high))
        for i in range(4):
            surf.blit(self.ValidTextures[pallette[i]], (i * self.wide, 0))
        return surf
    
    def GetTextureMatrix(self, editblock):
        surf = pie.Surface((self.wide * 9, self.high * 11))
        keys = list(self.ValidTextures.keys())
        i = 0
        for y in range(0, self.high * 11, self.high):
            for x in range(0, self.wide * 9, self.wide):
                if not editblock == keys[i] or randint(1,3) == 2:
                    if self.texture == ":":
                        try:
                            pie.draw.rect(surf, self.ValidTextures[keys[i]], pie.Rect(x, y, self.wide, self.high))
                        except:
                            pass
                    else:
                        if i < len(keys):
                            try:
                                surf.blit(self.ValidTextures[keys[i]], (x, y))
                            except:
                                pass
                i += 1
        return surf
    
    def SetBlock(self, block, x, y):
        self.data[y] = self.data[y][:x] + block + self.data[y][x+1:]
    
    def LoadCustom(self):
        filename = self.filename
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
            self.character = json_data.get("character", "--")
            self.character2 = json_data.get("character2", "--")
            self.bulletl = json_data.get("bulletl", "--")
            self.bulletr = json_data.get("bulletr", "--")
            if not self.character == "--":
                self.convert_mode = True
            self.data = json_data["data"]
            self.texture = json_data.get("texture", ":")
            self.walls = []
            self.entities = []
            self.script = []
            for line in json_data.get("script", []):
                self.script.append(line.replace("\"", "\\\""))
            self.high = json_data.get("high", 16)
            self.wide = json_data.get("wide", 8)
            self.LoadTexture()
            self.gravity = json_data.get("gravity", 0)
            self.jump = json_data.get("jump", 0)
            self.character = json_data.get("character", "@")
            self.shoot = json_data.get("shoot", self.data.copy())
            for entity in json_data.get("entities", []):
                ent_split = entity.split("x")
                self.entities.append([int(ent_split[0]), int(ent_split[1]), ent_split[2]])
            for coordinate in json_data.get("walls", []):
                coords = coordinate.split("x")
                coord_x = coords[0]
                coord_y = coords[1]
                if coord_x == "": coord_x = "0"
                if coord_y == "": coord_y = "0"
                coord_xy = (int(coord_x), int(coord_y))
                self.walls.append(coord_xy)

def InitMap(name):
    return PlayerMap(name)

def GetEight(line, script):
    eightlines = []
    for i in range(line, line+8):
        try:
            eightlines.append(FsEntry(script[i], "Lucida Console", 12, "white"))
        except:
            break
    return eightlines

def EditScript(fullscript, s):
    scroll = 0
    sx, sy = 0, 0
    quit_view = False
    clk = pie.time.Clock()
    if fullscript == []:
        fullscript = ["#", "# Insert custom scripts here!", "#", "# See help.txt for more detailed information", "#"]
    for i in range(len(fullscript)):
        fullscript[i] = fullscript[i].replace("\\\"", "\"").replace("\\\\", "\\")
    caption = FsEntry("Script editor (press escape to quit)", "Lucida Console", 17, "white")
    sublimes = GetEight(scroll, fullscript)
    while not quit_view:
        for e in pie.event.get():
            if e.type == pie.QUIT:
                quit_view = True
            elif e.type == pie.KEYDOWN:
                if e.key == pie.K_UP:
                    sy -= 1
                    if scroll+sy > 0 and scroll+sy < len(sublimes) - 1 and sx > len(sublimes[scroll+sy].name):
                        sx = len(sublimes[scroll+sy].name)
                    elif sx > len(sublimes[scroll+sy].name):
                        sx = 0
                elif e.key == pie.K_DOWN:
                    sy += 1
                    if scroll+sy < len(sublimes) - 2 and scroll+sy > 0 and sx > len(sublimes[scroll+sy].name):
                        sx = len(sublimes[scroll+sy].name)
                    elif sx > len(sublimes[scroll+sy].name):
                        sx = 0
                elif e.key == pie.K_LEFT:
                    sx -= 1
                    if sx < 0:
                        sy -= 1
                        try:
                            sx = len(sublimes[scroll+sy].name)
                        except:
                            sx = 0
                elif e.key == pie.K_RIGHT:
                    sx += 1
                    if scroll+sy < len(sublimes) - 1 and sx > len(sublimes[scroll+sy].name):
                        sy += 1
                        sx = 0
                    elif sx > len(sublimes[scroll+sy].name):
                        sx -= 1
                elif e.key == pie.K_ESCAPE:
                    quit_view = True
                elif e.key == pie.K_DELETE:
                    position_y = scroll + sy
                    position_x = sx
                    if sx == len(fullscript[position_y]):
                        fullscript[position_y] = fullscript[position_y] + fullscript[position_y + 1]
                        del fullscript[position_y+1]
                    else:
                        fullscript[position_y] = fullscript[position_y][:position_x] + fullscript[position_y][position_x+1:]
                    sublimes = GetEight(scroll, fullscript)
                elif e.key == pie.K_BACKSPACE:
                    position_y = scroll + sy
                    position_x = sx
                    if len(fullscript[position_y]) > 0:
                        fullscript[position_y] = fullscript[position_y][:position_x-1] + fullscript[position_y][position_x:]
                        sx -= 1
                    else:
                        del fullscript[position_y]
                        sy -= 1
                        position_y -= 1
                        sx = len(fullscript[position_y])
                    sublimes = GetEight(scroll, fullscript)
                elif e.key == pie.K_LSHIFT and e.key == pie.K_RSHIFT:
                    continue
                elif e.key == pie.K_RETURN:
                    position_y = scroll + sy
                    position_x = sx
                    fullscript[position_y] = fullscript[position_y][:position_x]
                    fullscript.append("")
                    fullscript[position_y + 1] = fullscript[position_y][position_x:]
                    sublimes = GetEight(scroll, fullscript)
                    sy += 1
                    sx = 0
                else:
                    position_y = scroll + sy
                    position_x = sx
                    fullscript[position_y] = fullscript[position_y][:position_x] + e.unicode + fullscript[position_y][position_x:]
                    sublimes = GetEight(scroll, fullscript)
                    sx += 1
        s.fill("black")
        caption.DisplayText(s, (10, 10))
        for y, lime in enumerate(sublimes):
            lime.DisplayText(s, (10, 30+y*15))
        if sy > 8:
            scroll += 1
            if scroll > len(fullscript):
                scroll = len(fullscript) - 1
            sublimes = GetEight(scroll, fullscript)
            sy = 7
        elif sy < 0:
            scroll -= 1
            if scroll < 0:
                scroll = 0
            sublimes = GetEight(scroll, fullscript)
            sy = 0
        pie.draw.rect(s, "lightgray", pie.Rect(10 + 7 * sx, 30 + sy * 15, 1, 15))
        pie.display.flip()
        clk.tick(60)
    for i in range(len(fullscript)):
        fullscript[i] = fullscript[i].replace("\\", "\\\\").replace("\"", "\\\"")
    return fullscript

def HelpMe(s):
    exit_help = False
    clk = pie.time.Clock()
    resolution = s.get_size()
    green_level = 0
    blink_cycle = 0
    okText = FsEntry("OK", "Lucida Console", 12, "white")
    instructions = (
                    FsEntry("Key shortcuts", "Lucida Console", 12, "white"),
                    FsEntry("", "Lucida Console", 12, "white"),
                    FsEntry("F1 - Help", "Lucida Console", 12, "white"),
                    FsEntry("Arrow keys - In normal mode changes position, in scroll mode moves camera", "Lucida Console", 12, "white"),
                    FsEntry("Scroll lock - Switch between normal and scrolling modes", "Lucida Console", 12, "white"),
                    FsEntry("WASD - Choose block", "Lucida Console", 12, "white"),
                    FsEntry("Space - Place block", "Lucida Console", 12, "white"),
                    FsEntry("Enter - Place wall marker", "Lucida Console", 12, "white"),
                    FsEntry("Ctrl + E - Script editor", "Lucida Console", 12, "white"),
                    FsEntry("Ctrl + S - Save", "Lucida Console", 12, "white"),
                    FsEntry("Escape - Close editor (any unsaved changes will be lost)", "Lucida Console", 12, "white"),
                    FsEntry("ZXCV - Set start, start 2, finish, finish 2 locations", "Lucida Console", 12, "white"),
                    FsEntry("Tab - Place a movable object", "Lucida Console", 12, "white"),
                    FsEntry("O - Mark this spot as shootable (use script editor to remove)", "Lucida Console", 12, "white"),
                    FsEntry("I - Add a teleport (use script editor to remove)", "Lucida Console", 12, "white"),
                    FsEntry("T - Trails mode, this will keep placing the selected block as you move around", "Lucida Console", 12, "white"),
                    FsEntry("F - Flood tool, this will fill the area with selected block", "Lucida Console", 12, "white"),
                    FsEntry("G - Flood wall tool, this is similar to the flood tool, but", "Lucida Console", 12, "white"),
                    FsEntry("    instead of placing blocks, it places wall markers", "Lucida Console", 12, "white"),
                    FsEntry("H - RNG flood tool, will fill the area with random blocks", "Lucida Console", 12, "white"),
                    FsEntry("F2 - Reset zoom", "Lucida Console", 12, "white"),
                    FsEntry("F3 - Zoom out", "Lucida Console", 12, "white"),
                    FsEntry("F4 - Zoom in", "Lucida Console", 12, "white"),
                    FsEntry("F5 - Gravity settings", "Lucida Console", 12, "white"),
                    FsEntry("F6 - Change texture pack", "Lucida Console", 12, "white"),
                    FsEntry("F7 - Change map size", "Lucida Console", 12, "white"),
                    FsEntry("F8 - Change single block dimensions", "Lucida Console", 12, "white"),
                    FsEntry("F9 - Show/Hide wall markers", "Lucida Console", 12, "white"),
                    FsEntry("F10 - Show/Hide text", "Lucida Console", 12, "white"),
                    FsEntry("F11 - Show/Hide block chooser", "Lucida Console", 12, "white"),
                    FsEntry("F12 - (Un)lock cursor onto/from actual block locations", "Lucida Console", 12, "white"),
                    FsEntry("Numpad 1-4 - Pick block to pallette. Numpad 1 will set your main selection as well.", "Lucida Console", 12, "white"),
                    FsEntry("Home/End - Move to the beginning/end of the line", "Lucida Console", 12, "white"),
                    FsEntry("Page Up/Down - Move to the beginning/end of the column", "Lucida Console", 12, "white"),
                    FsEntry("Delete/Insert - Shift the current row/column", "Lucida Console", 12, "white"),
                    FsEntry("Left click - Place block/Select block", "Lucida Console", 12, "white"),
                    FsEntry("Middle mouse button (hold) - Move camera", "Lucida Console", 12, "white"),
                    FsEntry("Right click - Place wall markers", "Lucida Console", 12, "white")
                    )
    while not exit_help:
        for e in pie.event.get():
            if e.type == pie.QUIT:
                exit_help = True
            elif e.type == pie.KEYDOWN:
                if e.key == pie.K_RETURN:
                    exit_help = True
        if pie.mouse.get_pressed()[0]:
            exit_help = True
        instruction_height = len(instructions) * 10 + 40
        pie.draw.rect(s, "darkcyan", pie.Rect(resolution[0] // 2 - 295, resolution[1] // 2 - instruction_height // 2, 590, instruction_height))
        green_level, blink_cycle = PulseBlue(green_level, blink_cycle, 3)
        sel_col = (0, green_level, 255)
        DrawButton(s, okText, resolution[0] // 2 - 20, resolution[1] // 2 + instruction_height // 2 - 20, 40, sel_col)
        for y, inst in enumerate(instructions):
            inst.DisplayText(s, (resolution[0] // 2 - 285, resolution[1] // 2 - instruction_height // 2 + 10 + y * 10))
        pie.display.flip()
        clk.tick(60)

def DrawButton(s, text, x, y, w, color):
    h = text.render.get_height()
    pie.draw.rect(s, color, pie.Rect(x, y, w, h))
    text.DisplayText(s, (x + w // 2 - text.render.get_width() // 2, y))

def GetScale(plrmap, scale):
    try:
        return round(((scale[0]*scale[1])/(plrmap.high*len(plrmap.data)*len(plrmap.data[0])*plrmap.wide)*100), 2)
    except:
        return 0

def EditMap(plrmap, fullscreen, resolution):
    exit_now = False
    if not fullscreen:
        resolution = (600, 400)
        s = pie.display.set_mode(resolution)
    else:
        s = pie.display.set_mode(resolution, pie.FULLSCREEN)
    clk = pie.time.Clock()
    if len(plrmap.data) == 0:
        plrmap.data.append(["#"])
    scale = [len(plrmap.data[0]) * plrmap.wide, len(plrmap.data) * plrmap.high]
    d1, d2, d3 = "Lucida Console", 12, "white"
    e_x = 0
    e_y = 0
    scale_value = GetScale(plrmap, scale)
    status_texts = {"mapname": FsEntry(plrmap.name, d1, 20, d3),
                    "author": FsEntry(f"by {plrmap.author}", d1, d2, d3),
                    "position": FsEntry(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)", d1, d2, d3),
                    "starts": FsEntry(f"Start 1: {plrmap.x}x{plrmap.y}, Start 2: {plrmap.x2}x{plrmap.y2}", d1, d2, d3),
                    "finishes": FsEntry(f"Finish 1: {plrmap.finish_x}x{plrmap.finish_y}, Finish 2: {plrmap.finish_x2}x{plrmap.finish_y2}", d1, d2, d3),
                    "hint": FsEntry("To see a list of possible keyboard commands, press F1", d1, d2, d3)}
    draw_text = True
    draw_walls = True
    draw_matrix = True
    draw_char = True
    trails = False
    block_keys = tuple(plrmap.ValidTextures.keys())
    block_pos = 0
    block_select = "#"
    rwide = scale[0] / len(plrmap.data[0])
    rhigh = scale[1] / len(plrmap.data)
    mdisp_x, mdisp_y = resolution[0]//2-len(plrmap.data[0])*plrmap.wide//2, resolution[1]//2-len(plrmap.data)*plrmap.high//2
    bdisp_x, bdisp_y = resolution[0]-9*plrmap.wide, resolution[1]//2-14*plrmap.high//2
    scroll = False
    antibounce = 10
    bg_1 = RandomColor()[0]
    bg_2 = RandomColor()[1]
    bg_3 = RandomColor()[2]
    c_1 = 0
    c_2 = 0
    c_3 = 0
    rng_pallette = ["#", "#", "#", "#"]
    teleport_memory = (-1, -1)
    while True:
        bdisp = plrmap.GetTextureMatrix(block_select)
        for e in pie.event.get():
            if e.type == pie.QUIT:
                exit_now = True
                break
            elif e.type == pie.KEYDOWN:
                if e.key == pie.K_ESCAPE:
                    exit_now = True
                    break
                elif e.key == pie.K_UP:
                    if not scroll:
                        e_y -= 1
                        status_texts["position"].ChangeText(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)")
                    else:
                        mdisp_y += plrmap.high
                elif e.key == pie.K_DOWN:
                    if not scroll:
                        e_y += 1
                        status_texts["position"].ChangeText(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)")
                    else:
                        mdisp_y -= plrmap.high
                elif e.key == pie.K_LEFT:
                    if not scroll:
                        e_x -= 1
                        status_texts["position"].ChangeText(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)")
                    else:
                        mdisp_x += plrmap.wide
                elif e.key == pie.K_RIGHT:
                    if not scroll:
                        e_x += 1
                        status_texts["position"].ChangeText(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)")
                    else:
                        mdisp_x -= plrmap.wide
                elif e.key == pie.K_SCROLLLOCK:
                    scroll = not scroll
                elif e.key == pie.K_TAB:
                    plrmap.entities.append((e_x, e_y, block_select))
                elif e.key == pie.K_o:
                    plrmap.script.append(f"if (plr.bx, plr.by) == ({e_x}, {e_y}): lvl.ChangeData((plr.bx, plr.by), \\\"{block_select}\\\")")
                    SayMessage("Shootable object marked.", s, resolution)
                elif e.key == pie.K_i:
                    if teleport_memory == (-1, -1):
                        teleport_memory = (e_x, e_y)
                    else:
                        plrmap.script.append(f"if (plr.x, plr.y) == ({teleport_memory[0]}, {teleport_memory[1]}): plr.Teleport({e_x}, {e_y})")
                        teleport_memory = (-1, -1)
                        SayMessage("Teleport added. Press any key...", s, resolution)

                elif e.key == pie.K_e and pie.key.get_mods() & pie.KMOD_CTRL:
                    plrmap.script = EditScript(plrmap.script, s)
                elif e.key == pie.K_s and pie.key.get_mods() & pie.KMOD_CTRL:
                    plrmap.Save()
                    SayMessage("Map saved. Press any key to continue...", s, resolution)
                elif e.key == pie.K_w:
                    block_pos -= 9
                    if block_pos < 0:
                        block_pos += 99
                    block_select = block_keys[block_pos]
                elif e.key == pie.K_a:
                    block_pos -= 1
                    if block_pos < 0:
                        block_pos += 99
                    block_select = block_keys[block_pos]
                elif e.key == pie.K_s:
                    block_pos += 9
                    if block_pos > 98:
                        block_pos -= 99
                    block_select = block_keys[block_pos]
                elif e.key == pie.K_d:
                    block_pos += 1
                    if block_pos > 98:
                        block_pos -= 99
                    block_select = block_keys[block_pos]
                elif e.key == pie.K_z:
                    plrmap.x = e_x
                    plrmap.y = e_y
                    status_texts["starts"].ChangeText(f"Start 1: {plrmap.x}x{plrmap.y}, Start 2: {plrmap.x2}x{plrmap.y2}")
                elif e.key == pie.K_t:
                    trails = not trails
                elif e.key == pie.K_x:
                    plrmap.x2 = e_x
                    plrmap.y2 = e_y
                    status_texts["starts"].ChangeText(f"Start 1: {plrmap.x}x{plrmap.y}, Start 2: {plrmap.x2}x{plrmap.y2}")
                elif e.key == pie.K_c:
                    plrmap.finish_x = e_x
                    plrmap.finish_y = e_y
                    status_texts["finishes"].ChangeText(f"Finish 1: {plrmap.finish_x}x{plrmap.finish_y}, Finish 2: {plrmap.finish_x2}x{plrmap.finish_y2}")
                elif e.key == pie.K_v:
                    plrmap.finish_x2 = e_x
                    plrmap.finish_y2 = e_y
                    status_texts["finishes"].ChangeText(f"Finish 1: {plrmap.finish_x}x{plrmap.finish_y}, Finish 2: {plrmap.finish_x2}x{plrmap.finish_y2}")
                elif e.key == pie.K_f:
                    plrmap.Fill(plrmap.data[e_y][e_x], block_select, e_x, e_y, "block")
                elif e.key == pie.K_g:
                    plrmap.Fill(plrmap.data[e_y][e_x], block_select, e_x, e_y, "wall")
                elif e.key == pie.K_h:
                    plrmap.Fill(plrmap.data[e_y][e_x], tuple(rng_pallette), e_x, e_y, "rng")
                elif e.key == pie.K_SPACE:
                    plrmap.SetBlock(block_select, e_x, e_y)
                elif e.key == pie.K_RETURN:
                    plrmap.SetWall(e_x, e_y)
                elif e.key == pie.K_F1:
                    HelpMe(s)
                elif e.key == pie.K_F2:
                    scale[0] = len(plrmap.data[0]) * plrmap.wide
                    scale[1] = len(plrmap.data) * plrmap.high
                    rwide = plrmap.wide
                    rhigh = plrmap.high
                    scale_value = 100.0
                elif e.key == pie.K_F4:
                    if scale[1] * 1.1 * scale[0] * 1.1 > 33554432:
                        errortext = FsEntry("Error 001: Maximum scale limit reached!", d1, d2, d3)
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
                            pie.draw.rect(s, "darkred", pie.Rect(resolution[0] // 2 - 150, resolution[1] // 2 - 15, 300, 30))
                            errortext.DisplayText(s, (resolution[0] // 2 - 140, resolution[1] // 2 - 5))
                            pie.display.flip()
                            clk.tick(60)
                        break
                    scale[0] *= 1.1
                    scale[1] *= 1.1
                    scale[0] = int(scale[0])
                    scale[1] = int(scale[1])
                    rwide = scale[0] // len(plrmap.data[0])
                    rhigh = scale[1] // len(plrmap.data)
                    scale_value = GetScale(plrmap, scale)
                elif e.key == pie.K_F3:
                    if scale[1] * 0.9 < plrmap.high or scale[0] * 0.9 < plrmap.wide:
                        errortext = FsEntry("Error 002: Minimum scale limit reached!", d1, d2, d3)
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
                            pie.draw.rect(s, "darkred", pie.Rect(resolution[0] // 2 - 150, resolution[1] // 2 - 15, 300, 30))
                            errortext.DisplayText(s, (resolution[0] // 2 - 140, resolution[1] // 2 - 5))
                            pie.display.flip()
                            clk.tick(60)
                        break
                    scale[0] *= 0.9
                    scale[1] *= 0.9
                    scale[0] = int(scale[0])
                    scale[1] = int(scale[1])
                    rwide = scale[0] // len(plrmap.data[0])
                    rhigh = scale[1] // len(plrmap.data)
                    scale_value = GetScale(plrmap, scale)
                elif e.key == pie.K_F5:
                    plrmap.GravitySetup(resolution)
                    antibounce = 10
                elif e.key == pie.K_F6:
                    plrmap.ChooseTexture(s)
                    plrmap.LoadTexture()
                elif e.key == pie.K_F7:
                    plrmap.SetSize()
                    mdisp_x, mdisp_y = resolution[0]//2-len(plrmap.data[0])*plrmap.wide//2, resolution[1]//2-len(plrmap.data)*plrmap.high//2
                    bdisp_x, bdisp_y = resolution[0]-9*plrmap.wide, resolution[1]//2-14*plrmap.high//2
                elif e.key == pie.K_F8:
                    plrmap.high, plrmap.wide = plrmap.SetTextureDims()
                    plrmap.LoadTexture()
                    mdisp_x, mdisp_y = resolution[0]//2-len(plrmap.data[0])*plrmap.wide//2, resolution[1]//2-len(plrmap.data)*plrmap.high//2
                    bdisp_x, bdisp_y = resolution[0]-9*plrmap.wide, resolution[1]//2-14*plrmap.high//2
                elif e.key == pie.K_F9:       draw_walls = not draw_walls
                elif e.key == pie.K_F10:      draw_text = not draw_text
                elif e.key == pie.K_F11:      draw_matrix = not draw_matrix
                elif e.key == pie.K_F12:      draw_char = not draw_char
                elif e.key == pie.K_KP1:
                    rng_pallette[0] = block_select
                    for i, key in enumerate(block_keys):
                        if key == plrmap.data[e_y][e_x]:
                            block_select = block_keys[i]
                            block_pos = i
                            break
                elif e.key == pie.K_KP2:  rng_pallette[1] = block_select
                elif e.key == pie.K_KP3:  rng_pallette[2] = block_select
                elif e.key == pie.K_KP4:  rng_pallette[3] = block_select
                elif e.key == pie.K_HOME:     e_x = 0
                elif e.key == pie.K_END:      e_x = len(plrmap.data[0])-1
                elif e.key == pie.K_PAGEUP:   e_y = 0
                elif e.key == pie.K_PAGEDOWN: e_y = len(plrmap.data)-1
                elif e.key == pie.K_INSERT:
                    if not scroll:
                        plrmap.data[e_y] = plrmap.data[e_y][-1] + plrmap.data[e_y][:-1]
                    else:
                        column = []
                        for i in range(len(plrmap.data)):
                            column.append(plrmap.data[i][e_x])
                        column = column[-1] + column[:-1]
                        for i in range(len(plrmap.data)):
                            plrmap.data[i][e_x] = column[i]                            
                elif e.key == pie.K_DELETE:
                    if not scroll:
                        plrmap.data[e_y] = plrmap.data[e_y][1:] + plrmap.data[e_y][0]
                    else:
                        column = []
                        for i in range(len(plrmap.data)):
                            column.append(plrmap.data[i][e_x])
                        column = column[1:] + column[0]
                        for i in range(len(plrmap.data)):
                            plrmap.data[i][e_x] = column[i]
        if exit_now:
            pie.mouse.set_visible(True)
            break
        if trails:
            plrmap.SetBlock(block_select, e_x, e_y)
        s.fill((bg_1, bg_2, bg_3))
        bg_1, c_1 = PulseBlue(bg_1, c_1, randint(0, 1))
        bg_2, c_2 = PulseBlue(bg_2, c_2, randint(0, 1))
        bg_3, c_3 = PulseBlue(bg_3, c_3, randint(0, 1))
        mdisp = plrmap.Draw()
        if draw_walls:
            for pos_y in range(0, len(plrmap.data)):
                for pos_x in range(0, len(plrmap.data[0])):
                    x, y = plrmap.wide * pos_x + plrmap.wide // 2 - 1, plrmap.high * pos_y + plrmap.high // 2 - 1
                    if (pos_x, pos_y) in plrmap.walls:
                        pie.draw.rect(mdisp, "red", pie.Rect(x, y, 3, 3))
            mdisp = plrmap.DrawEntity(mdisp)
        mouse = pie.mouse.get_pos()
        block_selected = False
        if mouse[0] > resolution[0] - 9 * plrmap.wide and mouse[0] < resolution[0]:
            if mouse[1] > resolution[1] // 2 - (14 * plrmap.high // 2) and mouse[1] < resolution[1] // 2 + (8 * plrmap.high // 2):
                block_selected = True
                if pie.mouse.get_pressed()[0] and draw_matrix:
                    block_pos = (((mouse[0] - resolution[0] + 9 * plrmap.wide) // plrmap.wide), ((mouse[1] - bdisp_y) // plrmap.high))
                    status_texts["position"].ChangeText(f"Block select: {block_pos[0]}, {block_pos[1]}, {block_pos[1] * 9 + block_pos[0]}")
                    block_select = block_keys[block_pos[1] * 9 + block_pos[0]]
                    block_pos = block_pos[0] + block_pos[1] * 9
        if draw_char and not block_selected:
            pie.draw.rect(mdisp, RandomColor(), pie.Rect((e_x + 1) * plrmap.wide - plrmap.wide // 2 - 3, (e_y + 1) * plrmap.high - plrmap.high // 2 - 1, 6, 2))
            pie.draw.rect(mdisp, RandomColor(), pie.Rect((e_x + 1) * plrmap.wide - plrmap.wide // 2 - 1, (e_y + 1) * plrmap.high - plrmap.high // 2 - 3, 2, 6))
        s.blit(pie.transform.scale(mdisp, scale), (mdisp_x, mdisp_y))
        if draw_matrix:
            s.blit(bdisp, (bdisp_x, bdisp_y))
            s.blit(plrmap.DrawPallette(rng_pallette), (resolution[0] - 4 * plrmap.wide, resolution[1] - plrmap.high))
        if not block_selected:
            if mouse[0] > mdisp_x and mouse[0] < mdisp_x + scale[0]:
                if mouse[1] > mdisp_y and mouse[1] < mdisp_y + scale[1]:
                    pie.mouse.set_visible(not draw_char)
                    e_x = int((mouse[0] - mdisp_x) // rwide)
                    e_y = int((mouse[1] - mdisp_y) // rhigh)
                    status_texts["position"].ChangeText(f"Position: {e_x}x{e_y} (Area: {len(plrmap.data[0])}x{len(plrmap.data)}, Scale:{scale_value}%)")
                    if antibounce == 0:
                        if len(pie.mouse.get_pressed()) > 2 and pie.mouse.get_pressed()[1]:
                            mdisp_x = mouse[0] - scale[0] // 2
                            mdisp_y = mouse[1] - scale[1] // 2
                        if pie.mouse.get_pressed()[0]:
                            plrmap.SetBlock(block_select, e_x, e_y)
                        elif pie.mouse.get_pressed()[-1]:
                            plrmap.SetWall(e_x, e_y)
                else:
                    pie.mouse.set_visible(True)
            else:
                pie.mouse.set_visible(True)
        else:
            pie.mouse.set_visible(True)
        if antibounce > 0:
            antibounce -= 1
        if draw_text:
            status_texts["mapname"].DisplayText(s, (10, 10), True)
            status_texts["author"].DisplayText(s, (10, 40), True)
            status_texts["position"].DisplayText(s, (10, resolution[1]-90), True)
            status_texts["starts"].DisplayText(s, (10, resolution[1]-75), True)
            status_texts["finishes"].DisplayText(s, (10, resolution[1]-60), True)
            status_texts["hint"].DisplayText(s, (10, resolution[1]-45), True)
        pie.display.flip()
        clk.tick(60)
