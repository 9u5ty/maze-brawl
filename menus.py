import screen_render as sr
import curses
import sys


def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    sr.window_create(0, "Main Menu", "menu")
    sr.draw_border(stdscr, 0, 0, 79, 22, 0)
    sr.add_menu_button(0, "Character Selection")
    sr.add_menu_button(0, "Help Menu")
    sr.add_menu_button(0, "Quit")
    choice = sr.draw_menu(stdscr, 0, 1, 0, 3, 1)
    if choice == "Quit":
        stdscr.clear()
        sys.exit(0)
    if choice == "Help Menu":
        stdscr.clear()
        stdscr.addstr(1, 1, "will implement soon.")
        stdscr.refresh()
        stdscr.getch()
    if choice == "Character Selection":
        stdscr.clear()
        character_selection(stdscr)
    


def character_selection(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    sr.window_create(1, "Character Selection", "menu")
    sr.draw_border(stdscr, 0, 0, 39, 22, 1)
    sr.window_create(2, "Description", "text")
    sr.draw_border(stdscr, 40, 0, 79, 22, 2)
    
    pass