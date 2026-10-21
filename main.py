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
    sr.setup_colors()
    curses.curs_set(0)
    sr.window_create(1, "test", "menu")
    sr.draw_border(stdscr, 0, 0, sr.W_WIDTH, sr.W_HEIGHT, 1)
    stdscr.refresh()
    stdscr.addstr(1, 2, "This is a test", sr.menu_text_select_bold)
    stdscr.addstr(3, 2, str(sr.active_windows[1][2]))
    stdscr.getch()
curses.wrapper(main)