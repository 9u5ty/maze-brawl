import curses

import menus
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
from explore import explore, start_game
from victory import victory_screen

def main(stdscr):
    sr.init(stdscr)
    sr.setup_colors()
    height, width = stdscr.getmaxyx()
    if height < 24 or width < 80:
        stdscr.addstr(0,0, "Resize screen to 80x24 at least.")
        stdscr.getch()
    else:
        while True:
            hero = menus.main_menu(stdscr)
            if hero is None:
                continue
            mapdef = menus.choose_map(stdscr)
            if mapdef is None:
                continue
            start_game(hero, mapdef)
            if explore() == "exit":
                victory_screen()

if __name__ == "__main__":
    curses.wrapper(main)
