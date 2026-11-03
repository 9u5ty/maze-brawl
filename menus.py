import screen_render as sr
import curses

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    sr.window_create(0, "main menu", "menu", )
    sr.draw_border(stdscr, 0, 0, 78, 22, 0)
    sr.add_menu_button(0, "Character Selection")
    sr.add_menu_button(0, "Help Menu")
    sr.add_menu_button(0, "Quit")
    choice = sr.draw_menu(stdscr, 0, 1, 0, 3, 1)
    stdscr.clear()
    stdscr.addstr(1, 1, f"You picked: {choice}")
    stdscr.refresh()
    stdscr.getch()
