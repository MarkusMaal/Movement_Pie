# Movement Pie
Movement Pie is a Python game based on the idea of Movement Batch. You can watch a [demonstration video](https://www.youtube.com/watch?v=wH83EieQVaM) here.

![screenshot](https://user-images.githubusercontent.com/45605071/156929319-d153e520-f229-4e08-b684-4532c29b7ff0.png)

## Prerequisites
You need to have Python 3 installed on your computer. It's also strongly recommended to have Pip installed as well.
This game uses Pygame as its engine, which means you need to install it as well.
Do this with the following command `pip install pygame`

## Menu navigation
The main menu can be navigated using either the arrow keys on your keyboard or the mouse. For keyboard navigation, use the **up** and **down** arrow keys to
change selection and **Enter** to confirm the selection. You can use the **Escape** key to move back to the previous menu. For mouse navigation, hover over
a menu item and **primary click** (by default **left click**) to confirm selection. Use **secondary click** (by default **right click**) to go back to the
previous menu.

## In-game keymap
* Arrow keys - In normal maps - Move currently selected character, in gravity maps - left/right moves the currently selected character, up for jumping (combine with left/right for curved jump), down does nothing
* Space - Shoot right
* Backspace - Shoot left
* 1/2 - Switch between characters (2P mode only)
* Escape - Quit map

## Game modes
* Single player - One player on map. Go to the finish block to win a map.
* 2 player mode - 2 players on a map. Both players need to finish the map.
* Headless mode - No players, useful for screenshotting and demos.

## Editor keymap
The editor keymap is accessible by pressing the F1 key in the editor.

## Scripting ABC
The section covers the basics of custom scripts on your own maps. Scripting allows you to insert your own code into custom maps, which allows you to expand functionality on
your own maps. Here are some examples with functions built into the level and player classes:
* Shootable objects: `if (plr.bx, plr.by) == ([x], [y]): lvl.ChangeData((plr.bx, plr.by), "[block string]")`
* Teleporting player: `if (plr.x, plr.y) == ([x1], [y1]): plr.Teleport([x2], [y2])`
* Teleporting onto another map after shooting an object: `if (plr.bx, plr.by) == ([x], [y]): lvl.SwitchMap("[mapname].json")`
* Teleporting onto another map after going into a specific spot: `if (plr.x, plr.y) == ([x], [y]): lvl.SwitchMap("[mapname].json")`

Other functions accessible through scripting from the level class:
* `LoadTexture()` - reload texture pack
* `LoadCustom(filename)` - load another map, also resets your position, unlike `SwitchMap(mapname)`
* `Shoot(xy, char)` - internal shooting function, not useful in scripting
* `GetData()` - returns the entire level data
* `Draw(screen)` - draws the map, not very useful in scripting
* `DrawEntity(screen)` - draws all entities, not very useful in scripting
* `CheckEntCollide(entity)` - check collision of one entity with another, not useful in scripting
* `MoveEntity(plr, mx, my)` - move entity in a specific direction, args are the player class, destination x position, destination y position
* `CheckEntityWalls(ent_x, ent_y)` - using the position of an entity, check if it's inside a wall

Other functions accessible through scripting from the player class:
* `Draw(screen, plr)` - draws the specified player on a screen, args are screen and plr (not useful in scripting)
* `CheckPlayerCollide(plr2)` - checks if one player is colliding with another, returns a boolean value (True or False)
* `Move(x, y, walls)` - move player to another location, also check if they collide with walls
* `Fire(state)` - fire a bullet to a specific direction, state -1 is for left, state 1 is for right
