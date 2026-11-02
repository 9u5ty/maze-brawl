from art import hero_art, title
from data import gear, heroes, hero_colors, hero_order, maps, monsters, moves
from fighters import gear_bonus
from helpbook import build_help_pages
from screen_render import (screen_w, center, clear_screen, col, draw_box, flush_keys, get_key, hline, put, show, widest)
from texts import gear_label, items_label, move_cost, move_summary, stat_text
#Builds helpbook
def help_screen():
    pages = build_help_pages()
    page = 0
    while True:
        draw_help_page(pages, page)
        k = get_key()
        if k == "ESC":
            flush_keys()
            return
        if k == "LEFT":
            page = (page - 1) % len(pages)
        elif k == "RIGHT":
            page = (page + 1) % len(pages)
#Shows a page of the helpbook
def draw_help_page(pages, page):
    clear_screen()
    title, rows = pages[page]
    center(0, f"{title}", col("green", bold=True))
    for i, pieces in enumerate(rows):
        for x, text, color in pieces:
            if color:
                put(2 + i, x, text, col(color, bold=True))
            else:
                put(2 + i, x, text)
    center(23, f"Page {page + 1} of {len(pages)}      LEFT/RIGHT: turn page      ESC: close",
           col("cyan"))
    show()

#Title screen menu
def title_screen():
    n = len(title)
    x0 = (screen_w - widest(title)) // 2
    while True:
        clear_screen()
        for i, line in enumerate(title):
            if i < n // 2:
                color = "red"
            else:
                color = "yellow"
            put(1 + i, x0, line, col(color, bold=True))
        y = 2 + n
        center(y, "A maze-crawling monster RPG", col("cyan"))
        center(y + 3, "Press ENTER to begin", col("green", bold=True))
        center(y + 5, "H - Help", col())
        show()
        k = get_key()
        if k == "ENTER":
            return
        if k == "h":
            help_screen()

#Map select menu
def choose_map(start_key=None):
    sel = 0
    for i, md in enumerate(maps):
        if md["key"] == start_key:
            sel = i
    while True:
        clear_screen()
        center(0, "CHOOSE YOUR MAP", col("cyan"))
        for i, md in enumerate(maps):
            draw_map_panel(i, md, i == sel)
        center(23, "UP/DOWN choose   ENTER select   ESC: back to the title   H: help", col("cyan"))
        show()
        k = get_key()
        if k == "UP":
            sel = (sel - 1) % len(maps)
        elif k == "DOWN":
            sel = (sel + 1) % len(maps)
        elif k in ("1", "2", "3"):
            sel = min(int(k) - 1, len(maps) - 1)
        elif k == "h":
            help_screen()
        elif k == "ENTER":
            return maps[sel]
        elif k == "ESC":
            return None
#Shows each map's information in panels
def draw_map_panel(i, map_def, selected):
    diff_colors = {"Easy": "green", "Medium": "yellow", "Hard": "red"}
    y = 3 + i * 5
    if selected:
        draw_box(y, 1, 4, 78, col(map_def["color"], bold=True))
    else:
        draw_box(y, 1, 4, 78, col(dim=True))
    put(y, 4, f" {i + 1}. {map_def['name']} ", col(map_def["color"], bold=True, rev=selected))
    put(y, 62, f" {map_def['difficulty']} ",
        col(diff_colors[map_def["difficulty"]], bold=True, rev=selected))
    put(y + 1, 4, map_def["blurb"], col(bold=selected))
    put(y + 2, 4, "Boss: " + monsters[map_def["boss"]]["name"], col("red", bold=selected))

#Hero selection menu
def choose_hero(mapdef, start_key=None):
    sel = start_selection(start_key)
    while True:
        key = hero_order[sel]
        draw_hero_tabs(mapdef, sel)
        hline(2)
        draw_hero_details(key)
        hline(15)
        draw_hero_table(sel)
        center(22, "LEFT/RIGHT browse   ENTER choose   ESC: back to the maps   H: help", col("cyan"))
        show()
        k = get_key()
        if k == "LEFT":
            sel = (sel - 1) % len(hero_order)
        elif k == "RIGHT":
            sel = (sel + 1) % len(hero_order)
        elif k in ("1", "2", "3", "4"):
            sel = min(int(k) - 1, len(hero_order) - 1)
        elif k == "ENTER":
            return key
        elif k == "h":
            help_screen()
        elif k == "ESC":
            return None
#Shows the picture, name, passive, stats, gear, items and moves
def draw_hero_details(key):
    h = heroes[key]
    color = hero_colors[key]
    for i, line in enumerate(hero_art[key]):
        put(3 + i, 4, line, col(color, bold=True))
    atk, dfn = hero_totals(h)
    atk_s, def_s = stat_text(h["atk"], atk), stat_text(h["def_"], dfn)
    put(3, 24, f"{h['name']} the {h['cls']}", col(color, bold=True))
    put(4, 24, h["passive_desc"], col("cyan"))
    put(6, 24, f"HP {h['hp']}   MP {h['mp']}   ATK {atk_s}   DEF {def_s}   SPD {h['spd']}")
    put(7, 24, f"Starting weapon: {gear_label(h['weapon'])}")
    put(8, 24, f"Starting armor : {gear_label(h['armor'])}")
    put(9, 24, f"Starting items : {items_label(h['items'])}")
    hline(10)
    for i, mk in enumerate(h["moves"]):
        mv = moves[mk]
        put(11 + i, 2, f"{i + 1}. {mv['name']:<15}{move_cost(mv):<8}{move_summary(mv)}"[:77])
# Shows table that compares the four heroes at the bottom of the hero screen
def draw_hero_table(sel):
    put(16, 2, f"{'Hero':<8}{'HP':<5}{'MP':<5}{'ATK':<8}{'DEF':<8}{'SPD':<5}{'Start weapon':<16}Start armor", col(dim=True))
    for i, k in enumerate(hero_order):
        hh = heroes[k]
        a, d = hero_totals(hh)
        weapon = "-"
        if hh["weapon"]:
            weapon = gear[hh["weapon"]]["name"]
        armor = "-"
        if hh["armor"]:
            armor = gear[hh["armor"]]["name"]
        row = f"{hh['name']:<8}{hh['hp']:<5}{hh['mp']:<5}{stat_text(hh['atk'], a):<8}{stat_text(hh['def_'], d):<8}{hh['spd']:<5}{weapon:<16}{armor}"
        put(17 + i, 2, row, col(hero_colors[k], bold=(i == sel), rev=(i == sel)))
#The top of the hero selection screen, which shows the title, the map name and the four hero names.
def draw_hero_tabs(mapdef, sel):
    clear_screen()
    center(0, "CHOOSE YOUR HERO", col("cyan"))
    put(0, 1, mapdef["name"], col(mapdef["color"], bold=True))
    for i, k in enumerate(hero_order):
        label = f"{i + 1} {heroes[k]['name']} - {heroes[k]['role']}"
        put(1, 1 + i * 20, f"{label:<19}", col(hero_colors[k], bold=True, rev=(i == sel)))
#Hero's starting ATK and DEF including starting gear
def hero_totals(h):
    atk = h["atk"] + gear_bonus(h["weapon"])
    dfn = h["def_"] + gear_bonus(h["armor"])
    return atk, dfn
#Hero that is highlighted first (either hero you just went back from or first hero if it is your first instance)
def start_selection(start_key):
    for i, k in enumerate(hero_order):
        if k == start_key:
            return i
    return 0