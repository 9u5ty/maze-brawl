from art import hero_art, monster_art
from battle import can_use_move, grant_rewards, log, new_battle, play_round, rows_in_order
from data import hero_colors, items, tag_colors
from fighters import calc_damage, item_ids_in_bag
from menus import help_screen
from screen_render import clear_screen, col, draw_box, get_key, hp_color, put, show, widest
from state import g, bs
from texts import atk_text, battle_summary, def_text, item_summary, move_cost, status_tags

#Runs the battle
def run_battle(mon):
    p = g["player"]
    b = new_battle(p, mon)
    bs.update(b=b, lines=[], notice="") #Prepares new battle screen state
    log(b, f"{mon["name"]} appears!") #Opening message
    show_round(b)
    while not b["over"]: #Keep asking for move choice until fight ends
        choice = battle_menu(b)
        if choice[0] == "move":
            play_round(b, ("move", p["moves"][choice[1]]))
        else:
            play_round(b, ("item", choice[1]))
        show_round(b)
    if b["over"] == "win": #Decide reward value
        rewards = grant_rewards(b)
    else:
        rewards = None
    while True: #Show the last round and wait for new entry, keeping last round visible
        draw_battle(None)
        put(22, 2, "Press ENTER to continue...   H: help", col("cyan", bold=True)) #Prompt for new imput
        show()
        k = get_key()
        if k == "ENTER":
            break
        if k == "h": #Can open help screen during battle
            help_screen()
    return b["over"], rewards

#Pack messages into display lines, starts new lines if message does not fit within the terminal
def pack_messages(messages):
    lines = []
    line = ""
    for message in messages:
        if line == "":
            line = message
        elif len(line) + 1 + len(message) <= 78:
            line = line + " " + message
        else:
            lines.append(line)
            line = message
    if line != "":
        lines.append(line)
    return lines

#Turn the round's messages into lines in battle screen
def show_round(b):
    lines = []
    for row in rows_in_order(b):
        lines = lines + pack_messages(b["rows"][row])
        b["rows"][row] = []
    b["msgs"] = []
    if len(lines) > 0:
        bs["lines"] = lines

#Ask the player what to do
def battle_menu(b):
    p = b["p"]
    mode = "main" 
    cur = 0
    bs["notice"] = ""
    while True:
        items = item_ids_in_bag(p)
        draw_battle({"mode": mode, "cur": cur, "items": items})
        k = get_key()
        if k == "h": #Battle is not affected if help screen is opened
            help_screen()
            continue
        bs["notice"] = "" 
        if mode == "main": #Handles fight/item choice
            mode, cur, bs["notice"] = main_menu_key(k, cur, len(items) > 0)
            continue
        mode, cur, bs["notice"], choice = grid_menu_key(b, mode, cur, k, items) #Handles move/item grid
        if choice is not None:
            return choice

#Draw the battle screen
def draw_battle(menu):
    b = bs["b"]
    clear_screen()
    draw_monster_box(b["m"])
    draw_hero_box(b["p"])
    for i, line in enumerate(bs["lines"]): #What happened in up to six lines
        put(15 + i, 2, line)
    if menu:
        draw_battle_menu(menu)
    show()

#Draw the menu at the bottom of the battle screen
def draw_battle_menu(menu):
    if menu["mode"] == "main":
        draw_main_menu(menu["cur"])
    elif menu["mode"] == "fight":
        draw_fight_menu(menu["cur"])
    else:
        draw_item_menu(menu["items"], menu["cur"])
    if bs["notice"]:
        put(22, 2, " " * 76)
        put(22, 2, bs["notice"], col("red", bold=True))
#Main menu
def draw_main_menu(cur):
    labels = ["1 FIGHT", "2 ITEM"]
    for i, label in enumerate(labels):
        put(21, 6 + i * 22, f" {label} ", highlight(i == cur))
    put(23, 2, "LEFT/RIGHT + ENTER, or press 1-2        H: help", col("cyan", dim=True))
#Fight menu in a 2x2 grid
def draw_fight_menu(cur):
    p, m = bs["b"]["p"], bs["b"]["m"]
    for i, mv in enumerate(p["moves"]):
        effect = move_effect_text(mv, calc_damage(p, m, mv))
        label = f"{i + 1} {mv["name"]:<15}{move_cost(mv):>5} {effect}"
        if p["mp"] >= mv.get("mp", 0):
            attr = highlight(i == cur)
        else:
            attr = col("red", dim=True, rev=(i == cur)) #If the move cannot be chosen it is shown in red color
        put(21 + i // 2, 2 + (i % 2) * 39, with_arrow(label, i == cur), attr)
    put(23, 2, battle_summary(p["moves"][cur], p, m)[:68], col("cyan"))
    put(23, 72, "ESC:back", col(dim=True))
#Item menu in a 2x2 grid
def draw_item_menu(item_ids, cur):
    p = bs["b"]["p"]
    for i, item_id in enumerate(item_ids):
        label = f"{i + 1} {items[item_id]["name"]:<14} x{p["items"][item_id]}"
        put(21 + i // 2, 2 + (i % 2) * 39, with_arrow(label, i == cur), highlight(i == cur))
    put(23, 2, item_summary(items[item_ids[cur]]), col("cyan"))
    put(23, 72, "ESC:back", col(dim=True))
#Color of menu choice
def highlight(selected):
    return col("yellow", bold=True, rev=selected)
#Selection arrows
def with_arrow(label, selected):
    if selected:
        return "> " + label
    return "  " + label
# What the fight menu shows after a move
def move_effect_text(mv, dmg):
    if dmg > 0: #Damage
        return f"dmg {dmg}"
    if "heal" in mv: #Healing
        return f"heal {mv["heal"]}"
    return "buff" #Buff

#Navigating 2x2 grid for choosing move/item
def move_in_grid(k, cur, n):
    if k == "UP" or k == "DOWN": #Vertical navigation
        other = (cur + 2) % 4
    elif k == "LEFT" or k == "RIGHT": #Horizontal navigation
        if cur % 2 == 0:
            other = cur + 1
        else:
            other = cur - 1
    else: 
        return cur
    if other < n:
        return other
    return cur

#Inputs in fight/item menu
def main_menu_key(k, cur, bag_has_items):
    if k == "LEFT" or k == "RIGHT":
        cur = 1 - cur
    elif k == "1" or k == "2":
        cur = int(k) - 1
        k = "ENTER"
    if k == "ENTER":
        if cur == 0:
            return "fight", 0, ""
        if bag_has_items:
            return "item", 0, ""
        return "main", cur, "Your bag is empty!"
    return "main", cur, ""
#Inputs in the battle 2x2 grid
def grid_menu_key(b, mode, cur, k, items):
    n = 4
    if mode == "item":
        n = len(items)
    if k == "ESC" or k == "b":
        if mode == "fight":
            return "main", 0, "", None
        return "main", 1, "", None
    if k is not None and k.isdigit() and 1 <= int(k) <= n:
        cur = int(k) - 1
        k = "ENTER"
    else:
        cur = move_in_grid(k, cur, n)
    if k != "ENTER":
        return mode, cur, "", None
    if mode == "fight":
        if can_use_move(b, cur):
            return mode, cur, "", ("move", cur)
        return mode, cur, "Not enough MP!", None
    notice = item_refusal(b["p"], items[cur])
    if notice == "":
        return mode, cur, "", ("item", items[cur])
    return mode, cur, notice, None
#The warning when an item would be wasted
def item_refusal(p, item_id):
    it = items[item_id]
    if "hp" in it and "mp" not in it and p["hp"] >= p["max_hp"]:
        return "HP is already full!"
    if "mp" in it and "hp" not in it and p["mp"] >= p["max_mp"]:
        return "MP is already full!"
    return ""

#The title of the battle, written into the top line of the monster's box
def draw_battle_title(m):
    if m["boss"]: #For boss
        put(0, 3, " !!! BOSS BATTLE !!! ", col("red", bold=True))
    else: #For regular battle
        put(0, 3, " BATTLE ", col("green", bold=True))

#The monster's picture and its box (title, name, HP, stats, status tags) at the top
def draw_monster_box(m):
    art = monster_art[m["t"]["art"]]
    x = 76 - widest(art)
    for i, line in enumerate(art):
        put(i, x, line, col(m["t"]["color"], bold=True))
    draw_box(0, 1, 5, 42, col(dim=True))
    draw_battle_title(m)
    tag = ""
    if m["boss"]: 
        tag = " [BOSS]"
    elif m["optional"]:
        tag = " [optional]"
    put(1, 3, (m["name"] + tag)[:38], col(m["t"]["color"], bold=True))
    put(2, 3, f"HP {m["hp"]}/{m["max_hp"]}", col(hp_color(m["hp"], m["max_hp"]), bold=True))
    put(3, 3, f"ATK {atk_text(m)}  DEF {def_text(m)}  SPD {m["spd"]}", col(dim=True))
    draw_tags(2, 15, status_tags(m), 26)
#The hero's picture and its box (name, HP, MP, stats, status tags) at the bottom
def draw_hero_box(p):
    for i, line in enumerate(hero_art[p["key"]]):
        put(8 + i, 4, line, col(hero_colors[p["key"]], bold=True))
    draw_box(10, 39, 5, 40, col(dim=True))
    put(11, 41, p["name"], col(hero_colors[p["key"]], bold=True))
    draw_tags(11, 49, status_tags(p), 28)
    put(12, 41, f"HP {p["hp"]}/{p["max_hp"]}", col(hp_color(p["hp"], p["max_hp"]), bold=True))
    put(12, 58, f"MP {p["mp"]}/{p["max_mp"]}", col("cyan", bold=True))
    put(13, 41, f"ATK {atk_text(p)}  DEF {def_text(p)}  SPD {p["spd"]}", col(dim=True))
#Draw status tags in its respective color
def draw_tags(y, x, tags, room):
    used = 0
    for tag in tags:
        text = "<" + tag + ">"
        if used + len(text) > room:
            return
        put(y, x + used, text, col(tag_colors[tag], bold=True))
        used += len(text) + 1