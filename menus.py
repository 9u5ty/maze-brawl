import curses
import sys
import data
import screen_render as sr

from art import title, hero_art
from texts import gear_label

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    stdscr.clear()
    sr.active_windows.clear()
    sr.window_create(0, "Main Menu", "menu", 0, 0, 79, 22)
    sr.add_menu_button(0, "Character Selection")
    sr.add_menu_button(0, "Help Menu")
    sr.add_menu_button(0, "Quit")
    #Center the whole title block while preserving the spacing between lines.
    title_width = max(len(text) for text in title)
    title_left = (80 - title_width) // 2
    for row, text in enumerate(title, 8):
        sr.put(row, title_left, text)
    stdscr.refresh()
    choice = sr.draw_menu(stdscr, 0, 1, 0, 3, 1)
    if choice == "Quit":
        stdscr.clear()
        sys.exit(0)
    if choice == "Help Menu":
        help_screen()
    if choice == "Character Selection":
        stdscr.clear()
        return character_selection(stdscr)
    if choice == "escape":
        stdscr.clear()
        sys.exit(0)

def help_screen():
    from helpbook import build_help_pages
    pages = build_help_pages()
    page = 0
    while True:
        sr.clear_screen()
        sr.put(0, 0, pages[page][0])
        for y, pieces in enumerate(pages[page][1], 2):
            for x, text, color in pieces:
                sr.put(y, x, text, sr.col(color))
        sr.put(23, 0, "LEFT/RIGHT: page ESC: close")
        sr.show()
        key = sr.get_key()
        if key == "ESC":
            return
        if key in ("LEFT", "RIGHT"):
            page = (page + (1 if key == "RIGHT" else -1)) % len(pages)

def choose_map(stdscr):
    stdscr.clear()
    sr.active_windows.clear()
    sr.window_create(0, "Choose Map", "menu", 0, 0, 79, 22)
    for md in data.maps:
        sr.add_menu_button(0, md["name"])
    sr.add_menu_button(0, "Back")
    choice = sr.draw_menu(stdscr, 0, 1, 1, len(data.maps) + 1, 1)
    return next((md for md in data.maps if md["name"] == choice), None)

def character_selection(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    #doing this for every menu so there's no cursor, but player can navigate menu

    sr.active_windows.clear()
    sr.window_create(1, "Character Selection", "menu", 0, 0, 39, 22)
    sr.window_create(2, "Description", "text", 40, 0, 79, 22)
    for hero_key in data.hero_order:
        hero = data.heroes[hero_key]
        sr.add_menu_button(1, hero["name"])
        starting_items = ", ".join(
            f"{data.items[item_id]['name']} x{count}"
            for item_id, count in hero["items"].items()
        )
        description = (
            f"{hero['name']}: {hero['cls']} ({hero['role']})\n"
            f"{hero['passive_desc']}\n\n"
            f"HP: {hero['hp']}  MP: {hero['mp']}\n"
            f"ATK: {hero['atk']}  DEF: {hero['def_']}  SPD: {hero['spd']}\n"
            f"Weapon: {gear_label(hero['weapon'])}\n"
            f"Armor: {gear_label(hero['armor'])}\n"
            f"Items: {starting_items}\n\n"
            + "\n".join(hero_art[hero_key])
        )
        sr.add_menu_button(2, description)
    sr.add_menu_button(1, "Back to Main Menu")
    sr.add_menu_button(2, "Goes back to main menu.")
    choice = sr.draw_menu(stdscr, 1, 1, 1, len(data.hero_order) + 1, 1)
    for hero_key in data.hero_order:
        if choice == data.heroes[hero_key]["name"]:
            return hero_key
    return None
