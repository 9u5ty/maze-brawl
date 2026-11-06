import curses
import sys

import data
import screen_render as sr


def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    stdscr.clear()
    sr.window_create(0, "Main Menu", "menu", 0, 0, 79, 22)
    sr.add_menu_button(0, "Character Selection")
    sr.add_menu_button(0, "Help Menu")
    sr.add_menu_button(0, "Quit")
    stdscr.refresh()
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
    if choice == "escape":
        stdscr.clear()
        sys.exit(0)


def character_selection(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    #doing this for every menu so there's no cursor, but player can navigate menu

    sr.window_create(1, "Character Selection", "menu", 0, 0, 39, 22)
    sr.add_menu_button(1, f"{data.heroes["kyle"]["name"]}")
    sr.add_menu_button(1, f"{data.heroes["bryce"]["name"]}")
    sr.add_menu_button(1, f"{data.heroes["george"]["name"]}")
    sr.add_menu_button(1, f"{data.heroes["clara"]["name"]}")
    sr.add_menu_button(1,"Back to Main Menu")
    sr.window_create(2, "Description", "text", 40, 0, 79, 22)
    sr.add_menu_button(2, "Kyle is an all-rounder hero.\nHe is good at all-round stuff.")
    sr.add_menu_button(2, "Bryce is an attacker.\nHe is good at attacking.")
    sr.add_menu_button(2, "Placeholder, will add full text soon.")
    sr.add_menu_button(2, "Another Placeholder. I will add text soon, this is a test to see if wrapping works or not.")
    choice = sr.draw_menu(stdscr, 1, 1, 1, 5, 1)
    if choice == data.heroes["kyle"]["name"]:
        stdscr.clear()
        stdscr.addstr(1, 1, "Chose Kyle")
        stdscr.refresh()
        stdscr.getch()
    if choice == data.heroes["bryce"]["name"]:
        stdscr.clear()
        stdscr.addstr(1, 1, "Chose Bryce")
        stdscr.refresh()
        stdscr.getch()
    if choice == "Back to Main Menu" or choice == "escape":
        main_menu(stdscr)
