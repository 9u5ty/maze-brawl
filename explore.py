from art import grave
from battlescreen import run_battle
from data import hero_colors, items
from fighters import new_player, reset_monster
from menus import help_screen
from screen_render import clear_screen, col, confirm, flush_keys, get_key, hp_color, popup, put, show
from shop import inventory_screen, shop_screen
from state import g
from texts import atk_text, def_text, gear_label
from maze_system import map_h, map_w, entity_at, is_blocked, load_map, nearby

#Load the map, create the hero and reset gold for a fresh run
def start_game(hero_key, mapdef):
    maze = load_map(mapdef)
    g.clear() #Clears gold in a new run
    g.update(player=new_player(hero_key), maze=maze, mapdef=mapdef, px=maze["start"][0], py=maze["start"][1], kills=0, deaths=0, message="")

#Message to show at the bottom of the map screen
def say(text):
    g["message"] = text

#Draw two status lines at the top of the map screen.
def draw_status():
    p = g["player"]
    put(0, 0, p["name"], col(hero_colors[p["key"]], bold=True))
    put(0, 14, f"HP {p['hp']}/{p['max_hp']}", col(hp_color(p["hp"], p["max_hp"]), bold=True))
    put(0, 30, f"MP {p['mp']}/{p['max_mp']}", col("cyan", bold=True))
    put(0, 46, f"Gold:{p['gold']}", col("yellow", bold=True))
    line = (f"ATK {atk_text(p)}   DEF {def_text(p)}   Items:{sum(p['items'].values())}"
            f"   [{g['mapdef']['name']}]")
    put(1, 0, line, col(dim=True))

# Draw walls, shops, the exit, monsters and the hero (a white @)
def draw_map():
    maze = g["maze"]
    for y in range(map_h):
        for x in range(map_w):
            if maze["wall"][y][x]:
                put(2 + y, x, "#", col(g["mapdef"]["color"], bold=True))
                continue
            e = entity_at(maze, x, y)
            if e is None:
                continue
            if e["kind"] == "shop":
                put(2 + y, x, "$", col("green", bold=True))
            elif e["kind"] == "exit":
                put(2 + y, x, "E", col("cyan", bold=True))
            else:
                mon = e["mon"]
                put(2 + y, x, mon["t"]["glyph"], col(mon["t"]["color"], bold=True))
    put(2 + g["py"], g["px"], "@", col("white", bold=True))

# Draw the whole map screen
def draw_explore():
    clear_screen()
    draw_status() #Status
    draw_map() #Map
    if g["message"]: #Message
        put(22, 0, g["message"])
    e = nearby(g["maze"], g["px"], g["py"])
    if e is None: #Hints
        hint = "Move: arrows/WASD   E: interact   I: inventory   H: help   ESC: leave map"
    elif e["kind"] == "shop":
        hint = "[E] Press E to enter the shop"
    else:
        hint = f"[E] Press E to challenge {e['mon']['name']}!"
    put(23, 0, hint, col("cyan", bold=True))

#Main loop that allows moving around and interactions
def explore():
    moves = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    while True:
        draw_explore()
        show()
        k = get_key()
        if k in moves:
            dx, dy = moves[k]
            if try_move(dx, dy) == "exit":
                return "exit"
        elif k == "e":
            interact()
        elif k == "i":
            inventory_screen()
        elif k == "h":
            help_screen()
        elif k == "ESC":
            if confirm(["Leave this map?", "Your progress will be lost."], "LEAVE MAP"):
                return "left"
#Trying a step forward
def try_move(dx, dy):
    maze = g["maze"]
    nx, ny = g["px"] + dx, g["py"] + dy 
    if is_blocked(maze, nx, ny):
        return None
    g["px"], g["py"] = nx, ny #If tile in front is free the try is committed
    g["message"] = ""
    e = entity_at(maze, nx, ny)
    if e and e["kind"] == "exit": #If tile tried is exit, it exits the maze
        return "exit"
    return None

#E key (interaction key), which performs interaction tasks
def interact():
    maze = g["maze"]
    e = nearby(maze, g["px"], g["py"])
    if e is None: #If nothing to interact with
        say("There is nothing to interact with here.")
        return
    if e["kind"] == "shop": #If trying to interact with shop
        shop_screen(e["shop"])
        return
    mon = e["mon"] #If interacting with monster
    lines, border = monster_popup(mon)
    if not confirm(lines, "A MONSTER BLOCKS THE WAY", border=border):
        return
    result, rewards = run_battle(mon)
    flush_keys()
    if result == "win":
        g["kills"] += 1
        e["dead"] = True
        show_spoils(mon, rewards)
    else:
        reset_monster(mon)
        blackout()

#Losing a fight makes you black out. You also lose half your gold
def blackout():
    p = g["player"]
    g["deaths"] += 1
    lost = p["gold"] // 2
    p["gold"] -= lost
    p["hp"], p["mp"] = p["max_hp"], p["max_mp"]
    g["px"], g["py"] = g["maze"]["start"]
    draw_explore()
    popup(list(grave) + ["", f"{p['name']} was defeated...", f"You wake at the start of the maze. Lost {lost} gold.", "", ("Press ENTER to try again", "green")], "DEFEATED", border="red")
    say(f"You blacked out and lost {lost} gold. Try again!")

#Popup after winning a battle
def show_spoils(mon, rewards):
    gold, drops = rewards 
    draw_explore()
    if mon["boss"]:
        popup([(f"{mon['name'].upper()} IS DEFEATED!", "green"), "", "Walk onto the exit  E  to escape!", "", ("Press ENTER to continue", "green")], "VICTORY", border="green")
        say("The boss is down! Reach the exit E!")
        return
    gear_line = "Gear: none" #Separate row for gear and item
    item_line = "Item: none"
    for kind, ident, note in drops:
        if kind == "gear":
            gear_line = f"Gear: {gear_label(ident)} - {note}"
        else:
            item_line = f"Item: {items[ident]['name']}"
    popup([(f"{mon['name']} is defeated!", "green"), "", f"Gold +{gold}",
           (gear_line, "cyan"), (item_line, "cyan"), "",
           ("Press ENTER to continue", "green")], "SPOILS", border="green")
    say(f"Defeated {mon['name']}! +{gold} gold.")

#"A monster blocks the way" popup
def monster_popup(mon):
    p = g["player"]
    stats = f"HP {mon['max_hp']}  ATK {mon['atk']}  DEF {mon['def']}  SPD {mon['spd']}"
    you = f"You: HP {p['hp']}/{p['max_hp']}   MP {p['mp']}/{p['max_mp']}"
    if mon["boss"]:
        return [(mon["name"].upper(), "red"), stats, you, "", "Are you ready?"], "red"
    tag = ""
    if mon["optional"]:
        tag = "  (optional)"
    return [f"{mon['name']}{tag}", stats, you, "", "Fight it?"], "yellow"