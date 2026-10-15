import curses

# Just acting as a library for colour pairs so we can all call the same colour pairs, and also manage drawing borders.

def setup_colors():
    curses.start_color()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    global menu_text_select; menu_text_select = curses.color_pair(1)
    global menu_text_select_bold; menu_text_select_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_BLINK
    global menu_text; menu_text = curses.color_pair(1) | curses.A_REVERSE
    global menu_text_bold; menutext_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE