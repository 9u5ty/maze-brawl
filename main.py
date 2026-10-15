import curses
import sys
import os
import screen_render
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
    screen_render.setup_colors()
    stdscr.refresh()
    stdscr.addstr(0, 0, "This is a test", screen_render.menu_text)
    stdscr.getch()
curses.wrapper(main)