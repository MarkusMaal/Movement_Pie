from Player import *
from Editor import *
from Common import *
import pygame as pie
import pygame.locals
import os

pie.init()
pie.font.init()


def GetDirEntries(directory, frmt, fltr = ""):
    entries = []
    for entry in os.listdir(directory):
        if entry.endswith(f".{frmt}") and fltr in entry:
            entries.append(FsEntry(entry, "Lucida Console", 12, "white"))
    return entries


def GetColorTuples(background, foreground, light):
    light = int(str(light).replace("1m", "1"))
    if foreground == "30" and light == 22:
        foreground = (0, 0, 0)
    elif foreground == "31" and light == 22:
        foreground = (128, 0, 0)
    elif foreground == "32" and light == 22:
        foreground = (0, 128, 0)
    elif foreground == "33" and light == 22:
        foreground = (128, 128, 0)
    elif foreground == "34" and light == 22:
        foreground = (0, 0, 128)
    elif foreground == "35" and light == 22:
        foreground = (128, 0, 128)
    elif foreground == "36" and light == 22:
        foreground = (0, 128, 128)
    elif foreground == "37" and light == 22:
        foreground = (192, 192, 192)
    elif foreground == "30" and light == 1:
        foreground = (128, 128, 128)
    elif foreground == "31" and light == 1:
        foreground = (255, 0, 0)
    elif foreground == "32" and light == 1:
        foreground = (0, 255, 0)
    elif foreground == "33" and light == 1:
        foreground = (255, 255, 0)
    elif foreground == "34" and light == 1:
        foreground = (0, 0, 255)
    elif foreground == "35" and light == 1:
        foreground = (255, 0, 255)
    elif foreground == "36" and light == 1:
        foreground = (0, 255, 255)
    else:
        foreground = (255, 255, 255)
    if background == "41":
        background = (128, 0, 0)
    elif background == "42":
        background = (0, 128, 0)
    elif background == "43":
        background = (128, 128, 0)
    elif background == "44":
        background = (0, 0, 128)
    elif background == "45":
        background = (128, 0, 128)
    elif background == "46":
        background = (0, 128, 128)
    elif background == "47":
        background = (192, 192, 192)
    elif background == "100":
        background = (128, 128, 128)
    elif background == "101":
        background = (255, 0, 0)
    elif background == "102":
        background = (0, 255, 0)
    elif background == "103":
        background = (255, 255, 0)
    elif background == "104":
        background = (0, 0, 255)
    elif background == "105":
        background = (255, 0, 255)
    elif background == "106":
        background = (0, 255, 255)
    elif background == "107":
        background = (255, 255, 255)
    else:
        background = (0, 0, 0)
    return background, foreground, light


def Convert(mapname, s):
    mapname = mapname.lower() + ".cmd"
    mapname = mapname.replace(".cmd.cmd", ".cmd")
    valid_txt = "# -?@!.,äõü~|><_:;¤%&/()=£$€{[]}*Ü^\\1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz\""
    texture = pie.Surface((9 * 8, 11 * 12))
    new_batch = PlayerMap(mapname.replace(".cmd", ".json"), s)
    new_batch.LoadBatchTexture()
    raw_blocks = {}
    map_data = []
    raw_start = -1
    raw_start2 = -1
    raw_finish = -1
    raw_finish2 = -1
    raw_ents = []
    raw_bents = []
    new_batch.author = "Unknown"
    texture_coordinate = [0, 0]
    with open(mapname, "r", encoding="windows-1257") as file:
        valid_id = 0
        for line in file:
            rline = line.replace("SET ", "").replace("Set ", "").replace("set ", "").replace("SEt ", "").replace("sET ", "").replace("SeT ", "")
            cmd = rline.split("=")[0]
            value = ""
            try:
                value = rline.split("=")[1].strip()
            except:
                pass
            if value.startswith("\x1b[") and cmd.startswith("bent"):
                value = value.replace("\x1b[", "")
                params = value.split(";")
                background = params[0]
                foreground = params[1]
                light = 22
                background, foreground, light = GetColorTuples(background, foreground, light)
                raw_block = (background, foreground, value.split(";")[-1][-1])
                if not raw_block[-1] in new_batch.batch_chars:
                    raw_block = (background, foreground, " ")
                if not ".".join(map(str, raw_block)) in raw_blocks and len(raw_blocks) < len(valid_txt):
                    raw_blocks[".".join(map(str, raw_block))] = valid_txt[valid_id]
                    texture.blit(ChangeColors(new_batch.ValidTextures[raw_block[-1]], raw_block[0], raw_block[1]), texture_coordinate)
                    texture_coordinate[0] += 8
                    if texture_coordinate[0] == 72:
                        texture_coordinate[1] += 12
                        texture_coordinate[0] = 0
                    valid_id += 1
                raw_bents.append(raw_blocks[".".join(map(str, raw_block))].replace("\"", "\\\"").replace("\\", "\\\\"))
            elif value.startswith("\x1b[") and cmd.startswith("a"):
                value = value.replace("\x1b[", "")
                params = value.split(";")
                background = params[0]
                foreground = params[1]
                light = params[2][:2]
                background, foreground, light = GetColorTuples(background, foreground, light)
                raw_block = (background, foreground, value.split(";")[-1][-1])
                if not value.split(";")[-1][-2] == "m":
                    raw_block = (background, foreground, " ")
                if len(raw_blocks) >= len(valid_txt):
                    print("Pallette full! Too many textures!!!")
                    raw_block = raw_blocks[0]
                backup = raw_block[-1]
                if not ".".join(map(str, raw_block)) in raw_blocks.keys() or not raw_block[-1] in new_batch.batch_chars:
                    if not raw_block[-1] in new_batch.batch_chars:
                        raw_block = (background, foreground, "?")
                    texture.blit(ChangeColors(new_batch.ValidTextures[raw_block[-1]].copy(), raw_block[0], raw_block[1]), texture_coordinate)
                    texture_coordinate[0] += 8
                    if texture_coordinate[0] == 72:
                        texture_coordinate[1] += 12
                        texture_coordinate[0] = 0
                    raw_blocks[".".join(map(str, raw_block))] = valid_txt[valid_id]
                    valid_id += 1
                map_data.append(raw_blocks[".".join(map(str, raw_block))].replace("\"", "\\\"").replace("\\", "\\\\"))
            elif (len(cmd) == 2 or len(cmd) == 3 or len(cmd) == 4) and cmd.startswith("a"):
                if value == "": value = " "
                #if not value in valid_txt: value = "?"
                if not value in raw_blocks:
                    raw_blocks[value] = valid_txt[valid_id]
                    texture.blit(new_batch.ValidTextures[value], texture_coordinate)
                    texture_coordinate[0] += 8
                    if texture_coordinate[0] == 72:
                        texture_coordinate[1] += 12
                        texture_coordinate[0] = 0
                    valid_id += 1
                map_data.append(raw_blocks[value])
            elif cmd.lower() == "/a start" or cmd.lower() == "start":
                if "+" in value:
                    value = value.split("+")[0]
                try:
                    raw_start = int(value) - 1
                except:
                    pass
            elif cmd.lower() == "/a start2" or cmd.lower() == "start2":
                if "+" in value:
                    value = value.split("+")[0]
                try:
                    raw_start2 = int(value) - 1
                except:
                    pass
            elif cmd.lower() == "/a finish" or cmd.lower() == "finish":
                if "+" in value:
                    value = value.split("+")[0]
                try:
                    raw_finish = int(value) - 1
                except:
                    pass
            elif cmd.lower() == "/a finish2" or cmd.lower() == "finish2":
                if "+" in value:
                    value = value.split("+")[0]
                try:
                    raw_finish2 = int(value) - 1
                except:
                    pass
            elif cmd.lower() == "author":
                new_batch.author = value
            elif cmd.lower() == "gravity":
                try:
                    new_batch.gravity = int(value.lower().replace("false", "0").replace("true", "1"))
                except:
                    new_batch.gravity = 0
            elif cmd.lower() == "/a jumpmax" or cmd.lower() == "jumpmax":
                if "+" in value:
                    value = value.split("+")[0]
                new_batch.jump = int(value)
            elif cmd.lower().startswith("ent"):
                if "+" in value:
                    value = value.split("+")[0]
                raw_ents.append(int(value))
            elif cmd.lower().startswith("bent"):
                if not value in raw_blocks:
                    raw_blocks[value] = valid_txt[valid_id]
                    texture.blit(new_batch.ValidTextures[value], texture_coordinate)
                    texture_coordinate[0] += 8
                    if texture_coordinate[0] == 72:
                        texture_coordinate[1] += 12
                        texture_coordinate[0] = 0
                    valid_id += 1
                raw_bents.append(raw_blocks[value])
    
    texture.blit(new_batch.ValidTextures["@"], texture_coordinate)
    texture_coordinate[0] += 8
    if texture_coordinate[0] == 72:
        texture_coordinate[1] += 12
        texture_coordinate[0] = 0
    valid_id += 1
    texture.blit(new_batch.ValidTextures["#"], texture_coordinate)
    texture_coordinate[0] += 8
    if texture_coordinate[0] == 72:
        texture_coordinate[1] += 12
        texture_coordinate[0] = 0
    valid_id += 1
    texture.blit(ChangeColors(new_batch.ValidTextures["®"], (0, 0, 0), (255, 255, 0)), texture_coordinate)
    texture_coordinate[0] += 8
    if texture_coordinate[0] == 72:
        texture_coordinate[1] += 12
        texture_coordinate[0] = 0
    valid_id += 1
    texture.blit(ChangeColors(new_batch.ValidTextures["Æ"], (0, 0, 0), (255, 255, 0)), texture_coordinate)
    new_batch.convert_mode = True
    new_batch.character = list(new_batch.ValidTextures.keys())[valid_id - 3]
    new_batch.character2 = list(new_batch.ValidTextures.keys())[valid_id - 2]
    new_batch.bulletl = list(new_batch.ValidTextures.keys())[valid_id - 1]
    new_batch.bulletr = list(new_batch.ValidTextures.keys())[valid_id]
    new_batch.gravity = 0
    new_batch.jump = 0
    texture_coordinate[0] += 8
    if texture_coordinate[0] == 72:
        texture_coordinate[1] += 12
        texture_coordinate[0] = 0
    valid_id += 1
    chop = 20
    if len(map_data) > 300:
        chop = 40
    line = []
    new_batch.data = []
    if chop == 40:
        map_data = map_data[1:]
    for block in map_data:
        line.append(block)
        if len(line) == chop:
            new_batch.data.append("".join(line))
            line = []
    s.blit(texture, (0, 0))
    pie.display.flip()
    #ifcheck_data = with open(mapname.replace(".cmd", "_ifcheck.cmd"), "r", encoding="windows-1252") as file: file.read()
    justname = mapname.replace(".cmd", "")
    
    raw_walls = []
    raw_teleports = []
    raw_shootables = []
    if os.path.exists(justname + "_ifcheck.cmd"):
        with open(justname + "_ifcheck.cmd", "r", encoding="windows-1257") as ifcheck:
            for line in ifcheck:
                line = line.strip()
                if line.lower().startswith("if %position%==") and "%last%" in line and not line.endswith("("):
                    raw_walls.append(int(line.split(" ")[1].split("=")[-1]) - 1)
                elif line.lower().startswith("if %position%==") and not "%last%" in line and not line.endswith("("):
                    try:
                        raw_teleports.append((int(line.split(" ")[1].split("=")[-1]) - 1, int(line.split(" ")[-1].split("=")[-1]) - 1))
                    except:
                        pass
                elif line.lower().startswith("if \"%shootpos%\"==") and "loadable" in line:
                    raw_x = int(line.lower().split("\"")[3])
                    position = (raw_x % chop, raw_x // chop)
                    loadable = line.lower().split("\"")[4].split("=")[-1]
                    new_batch.script.append(f"if (plr.bx, plr.by) == ({position[0]}, {position[1]}): lvl.SwitchMap(\\\"{loadable}\\\")")
                elif line.lower().startswith("if \"%position") and "loadable" in line:
                    raw_x = int(line.lower().split("\"")[3])
                    position = (raw_x % chop, raw_x // chop)
                    loadable = line.lower().split("\"")[4].split("=")[-1]
                    new_batch.script.append(f"if (plr.x, plr.y) == ({position[0]}, {position[1]}): lvl.SwitchMap(\\\"{loadable}\\\")")

    if os.path.exists(justname + "_shootcheck.cmd"):
        with open(justname + "_shootcheck.cmd", "r", encoding="windows-1257") as shootcheck:
            for line in shootcheck:
                line = line.strip()
                if line.lower().startswith("if %shootpos%==") and "set b%shootpos%=" in line:
                    block = line.split("=")[-1]
                    pos = int(line.split("=")[2].split(" ")[0])
                    block_pic = None
                    if "\x1b[" in block:
                        params = block[2:].split(";")
                        background = params[0]
                        foreground = params[1]
                        light = params[2][:2]
                        background, foreground, light = GetColorTuples(background, foreground, light)
                        raw_block = (background, foreground, block.split(";")[-1][-1])
                        if not raw_block[-1] in new_batch.batch_chars:
                            raw_block = (background, foreground, " ")
                        if not ".".join(map(str, raw_block)) in raw_blocks and len(raw_blocks) < len(valid_txt):
                            raw_blocks[".".join(map(str, raw_block))] = valid_txt[valid_id]
                            texture.blit(ChangeColors(new_batch.ValidTextures[raw_block[-1]], raw_block[0], raw_block[1]), texture_coordinate)
                            texture_coordinate[0] += 8
                            if texture_coordinate[0] == 72:
                                texture_coordinate[1] += 12
                                texture_coordinate[0] = 0
                            valid_id += 1
                        raw_shootables.append((pos - 1, raw_blocks[".".join(map(str, raw_block))].replace("\"", "\\\"").replace("\\", "\\\\")))
                    else:
                        if not block in raw_blocks:
                            raw_blocks[block] = valid_txt[valid_id]
                            if block == "":
                                block = " "
                            if not block in new_batch.batch_chars:
                                block = " "
                            texture.blit(new_batch.ValidTextures[block], texture_coordinate)
                            texture_coordinate[0] += 8
                            if texture_coordinate[0] == 72:
                                texture_coordinate[1] += 12
                                texture_coordinate[0] = 0
                            valid_id += 1
                        try:
                            raw_shootables.append((pos - 1, raw_blocks[block]))
                        except:
                            raw_shootables.append((pos - 1, raw_blocks[list(raw_blocks.keys())[-1]]))
    new_batch.name = justname
    new_batch.texture = f"__CONVERTED_{justname}.png"
    new_batch.wide = 8
    new_batch.high = 12
    new_batch.walls = []
    new_batch.script = []
    new_batch.entities = []
    for shootable in raw_shootables:
        new_batch.script.append(f"if (plr.bx, plr.by) == ({shootable[0] % chop}, {shootable[0] // chop}): lvl.ChangeData((plr.bx, plr.by), \\\"{shootable[1]}\\\")")
    for wall in raw_walls:
        new_batch.walls.append((wall % chop, wall // chop))
    for tp in raw_teleports:
        new_batch.script.append(f"if (plr.x, plr.y) == ({tp[0] % chop}, {tp[0] // chop}): plr.Teleport({tp[1] % chop - 1}, {tp[1] // chop})")
    # convert 1.5D coordinates to 2D coordinates
    new_batch.x = raw_start % chop
    new_batch.y = raw_start // chop
    new_batch.x2 = raw_start2 % chop
    new_batch.y2 = raw_start2 // chop
    new_batch.finish_x = raw_finish % chop
    new_batch.finish_y = raw_finish // chop
    new_batch.finish_x2 = raw_finish2 % chop
    new_batch.finish_y2 = raw_finish2 // chop
    for i in range(len(raw_ents)):
        raw_ent_x = raw_ents[i] % chop
        raw_ent_y = raw_ents[i] // chop
        try:
            new_batch.entities.append((raw_ent_x, raw_ent_y, raw_bents[i]))
        except:
            new_batch.entities.append((raw_ent_x, raw_ent_y, raw_bents[-1]))
    pie.image.save(texture, f"Maps/Textures/__CONVERTED_{justname}.png")
    new_batch.Save()
    SayMessage("Conversion successful. Please note that not everything can be converted using this method.", s, (600, 300))


def Execute(mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, fltr):
    exit_now = False
    if mode == "chooser":
        if not open_editor:
            PlayCustom(category_entries[mode][select].name, character, character2, shoot, gmode, resolution, fullscreen)
        else:
            map1 = PlayerMap(category_entries[mode][select].name, s)
            map1.LoadCustom()
            EditMap(map1, fullscreen, resolution)
        if not fullscreen:
            s = pie.display.set_mode(resolution)
        else:
            s = pie.display.set_mode(resolution, pie.FULLSCREEN)
        try:
            subtext.ChangeText(splash)
        except:
            exit_now = True
        mode = "main"
        select = 0
        pie.mouse.set_visible(True)
    elif mode == "editor":
        if select == 0:
            name = FileName(s, "Set filename for your new map")
            if not name == None:
                map1 = PlayerMap(name, s)
                map1.CreateMap()
                EditMap(map1, fullscreen, resolution)
        elif select == 1:
            open_editor = True
            mode = "chooser"
            last = "editor"
            open_editor = True
            fltr = ""
            category_entries["chooser"] = GetDirEntries("./Maps", "json")
            subtext.ChangeText("Select a map you'd like to edit")
        elif select == 2:
            mode = "main"
            last = "exit"
            subtext.ChangeText(splash)
            select = 0
    elif mode == "extra":
        if select == 0:
            Convert(FileName(s, "Movement Batch map name:"), s)
        elif select == 1:
            mode = "chooser"
            last = "extra"
            fltr = ""
            category_entries["chooser"] = GetDirEntries("./Maps", "json")
            subtext.ChangeText("Select a map you'd like to preview")
        elif select == 3:
            mode = "main"
            last = "exit"
            subtext.ChangeText(splash)
            select = 0
    elif mode == "options":
        if select == 0:
            character =  FileName(s, f"Enter character (current: {character})", False)
        elif select == 1:
            character2 = FileName(s, f"Enter character (current: {character2})", False)
        elif select == 2:
            shoot = int(FileName(s, f"Set bullet distance (current: {shoot})", False))
            category_entries["options"][2].ChangeText(f"Bullet distance: {shoot} blocks")
        elif select == 3:
            if gmode == "single":
                gmode = "multi"
                category_entries["options"][3].ChangeText("Game mode: 2 players")
            elif gmode == "multi":
                gmode = "headless"
                category_entries["options"][3].ChangeText("Game mode: Headless")
            elif gmode == "headless":
                gmode = "single"
                category_entries["options"][3].ChangeText("Game mode: 1 player")
        elif select == 4:
            if fullscreen:
                fullscreen = False
                resolution = (600, 200)
                s = pie.display.set_mode(resolution)
                category_entries["options"][4].ChangeText("Fullscreen: Disabled")
            else:
                fullscreen = True
                resolution = pie.display.get_desktop_sizes()[0]
                s = pie.display.set_mode(resolution, pie.FULLSCREEN)
                category_entries["options"][4].ChangeText("Fullscreen: Enabled")
        elif select == 5:
            mode = "main"
            last = "exit"
            subtext.ChangeText(splash)
            select = 0
            
    elif mode == "main":
        if select == 0:
            mode = "chooser"
            last = "main"
            open_editor = False
            fltr = ""
            category_entries["chooser"] = GetDirEntries("./Maps", "json")
            subtext.ChangeText("Select a map you'd like to play")
        elif select == 1:
            mode = "editor"
            last = "main"
            select = 0
            subtext.ChangeText("Select an action")
        elif select == 2:
            mode = "options"
            last = "main"
            select = 0
            subtext.ChangeText("Edit options here")
        elif select == 3:
            mode = "extra"
            last = "main"
            select = 0
            subtext.ChangeText("Additional features")
        elif select == 4:
            exit_now = True
    return mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, exit_now, fltr
clk = pie.time.Clock()
resolution = (600, 300)
fullscreen = False
s = pie.display.set_mode(resolution)
ui_input = {"w": False, "s": False}
character = "@"
character2 = "#"
shoot = 5
gmode = "single"

splashes = ("Hello!", "Welcome!", "This is the main menu", "Press up and down to choose desired menu item", "Press Enter to confirm selection", "You can use the options menu to configure the game", "Use the editor to make your own maps")
splash = splashes[randint(0, len(splashes)-1)]

title = FsEntry("Movement Pie", "Lucida Console", 20, "white")
subtext = FsEntry(splash, "Lucida Console", 9, "white")
bg_color = list(RandomColor())
cycles = [randint(0, 1), randint(0, 1), randint(0, 1)]
category_entries = {}
category_entries["main"] = []
category_entries["main"].append(FsEntry("Start", "Lucida Console", 12, "white"))
category_entries["main"].append(FsEntry("Editor", "Lucida Console", 12, "white"))
category_entries["main"].append(FsEntry("Options", "Lucida Console", 12, "white"))
category_entries["main"].append(FsEntry("Extra", "Lucida Console", 12, "white"))
category_entries["main"].append(FsEntry("Exit", "Lucida Console", 12, "white"))
category_entries["editor"] = []
category_entries["editor"].append(FsEntry("Create a new map", "Lucida Console", 12, "white"))
category_entries["editor"].append(FsEntry("Load existing map", "Lucida Console", 12, "white"))
category_entries["editor"].append(FsEntry("Go back", "Lucida Console", 12, "white"))
category_entries["options"] = []
category_entries["options"].append(FsEntry("Change character", "Lucida Console", 12, "white"))
category_entries["options"].append(FsEntry("Change second character", "Lucida Console", 12, "white"))
category_entries["options"].append(FsEntry("Bullet distance: 5 block(s)", "Lucida Console", 12, "white"))
category_entries["options"].append(FsEntry("Game mode: 1 player", "Lucida Console", 12, "white"))
category_entries["options"].append(FsEntry("Fullscreen mode: Disabled", "Lucida Console", 12, "white"))
category_entries["options"].append(FsEntry("Go back", "Lucida Console", 12, "white"))
category_entries["chooser"] = GetDirEntries("./Maps", "json")
category_entries["extra"] = []
category_entries["extra"].append(FsEntry("Convert Movement Batch map", "Lucida Console", 12, "white"))
category_entries["extra"].append(FsEntry("Preview map", "Lucida Console", 12, "white"))
category_entries["extra"].append(FsEntry("Random map generator", "Lucida Console", 12, "white"))
category_entries["extra"].append(FsEntry("Go back", "Lucida Console", 12, "white"))
select = 0
antibounce = 10
mode = "main"
last = "exit"
open_editor = False
green_level = 0
blink_cycle = 0
fltr = ""
search_text = FsEntry("Filter map(s) by keyword(s)", "Lucida Console", 12, "white")
while True:
    pie.display.set_caption("Movement Pie 0.5 **** UNDER CONSTRCUTION ****")
    exit_now = False
    for e in pie.event.get():
        if e.type == pie.QUIT:
            exit_now = True
            break
        elif e.type == pie.KEYDOWN:
            if e.key == pie.K_UP: select -= 1
            elif e.key == pie.K_ESCAPE:
                mode = str(last)
                if mode == "main":
                    subtext.ChangeText(splash)
                if mode == "exit":
                    exit_now = True
                    break
            elif e.key == pie.K_DOWN: select += 1
            elif e.key == pie.K_RETURN:
                mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, exit_now, fltr = Execute(mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, fltr)
    if select < 0:
        select = len(category_entries[mode]) - 1
    elif select > len(category_entries[mode]) - 1:
        select = 0
    try:
        s.fill(bg_color)
    except:
        break
    bg_color[0], cycles[0] = PulseBlue(bg_color[0], cycles[0], randint(0, 2))
    bg_color[1], cycles[1] = PulseBlue(bg_color[1], cycles[1], randint(0, 2))
    bg_color[2], cycles[2] = PulseBlue(bg_color[2], cycles[2], randint(0, 2))
    lim = resolution[1]
    lim_sels = (lim - 60) // 20 - 1
    if select - lim_sels < 0:
        idx = 0
    else:
        idx = select - lim_sels
    mouse_location = pie.mouse.get_pos()
    if mouse_location[0] < 205 and mouse_location[1] - 60 < lim:
        select = (mouse_location[1] - 60) // 20
        if pie.mouse.get_pressed()[0] and antibounce < 1:
            mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, exit_now, fltr = Execute(mode, select, open_editor, last, character, character2, shoot, category_entries, gmode, resolution, fullscreen, s, fltr)
            antibounce = 10
        elif pie.mouse.get_pressed()[-1] and antibounce < 1:
            mode = str(last)
            if mode == "main":
                subtext.ChangeText(splash)
            if mode == "exit":
                exit_now = True
            antibounce = 10
    if exit_now:
        pie.quit()
        break
    if antibounce > 0:
        antibounce -= 1
    sel_col = (0, green_level, 255)
    green_level, blink_cycle = PulseBlue(green_level, blink_cycle, 3)
    for y in range(60, len(category_entries[mode]) * 20 + 60, 20):
        if select == idx:
            pie.draw.rect(s, sel_col, pie.Rect(5, y, 200, 10))
            if mode == "chooser":
                s.blit(Preview(category_entries[mode][idx].name), (250, 60))
        try:
            category_entries[mode][idx].DisplayText(s, (10, y))
        except:
            pass
        idx += 1
    high_lighted = False
    if mode == "chooser":
        if mouse_location[0] < resolution[0] - 5 and mouse_location[0] > resolution[0] - 205:
            if mouse_location[1] < 15 and mouse_location[1] > 5:
                DrawButton(s, search_text, resolution[0] - 205, 5, 200, sel_col)
                high_lighted = True
        if not high_lighted:
            DrawButton(s, search_text, resolution[0] - 205, 5, 200, "darkblue")
        elif antibounce < 1 and pie.mouse.get_pressed()[0]:
            if fltr == "":
                fltr = FileName(s, "Enter keyword(s): ")
                category_entries["chooser"] = GetDirEntries("./Maps", "json", fltr)
            else:
                fltr = ""
                category_entries["chooser"] = GetDirEntries("./Maps", "json", "")
    title.DisplayText(s, (10, 10))
    subtext.DisplayText(s, (10, 40))
    pie.display.flip()
    clk.tick(30)