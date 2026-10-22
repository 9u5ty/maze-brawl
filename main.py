import curses
import sys
import os
import screen_render as sr
# Just writing some documentation to help planning out the whole game and make things somewhat clearer. #

"""
Needed files/systems:
- Menu system, handles all menus for the game and based on state sends to appropriate window loops.
- Game state system, used as a dependency for most systems.
- Stat system. Handles all player statistics and shared stats such as HP, ATTACK & DEFENSE stats,
gold. Combat system, and Shop system will depend on this.
- Combat system: Handles turn based combat and depends on gamestate, world & stats system.
- Inventory system: Handles items and equipment, depends on menu, stat, gamestate & menu system.
- World system: Handles moving within game world, depends on gamestate & stat system.
- Shop system: Handles buying items


Should finish the most important systems first that have the most impact on the other systems first to ensure
changing stuff will not break everything else.

"""



"""
- Game preloading phase:
    - Load the text display file and cache the different text attribute keys.
    - Create initialised display lists for mazes, and windows if needed
    
- Main menu phase: 
    - Load main menu to initialise game and load the character selection screen.







"""

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    sr.setup_colors()
    sr.window_create(0, "Menu", "menu")
    sr.draw_border(stdscr, 0, 0, 78, 22, 0)
    sr.add_menu_button(0, "Start")
    sr.add_menu_button(0, "Options")
    sr.add_menu_button(0, "Quit")
    choice = sr.draw_menu(stdscr, 0, 1, 0, 3, 1)
    stdscr.clear()
    stdscr.addstr(1, 1, f"You picked: {choice}")
    stdscr.refresh()
    stdscr.getch()
curses.wrapper(main)

import curses