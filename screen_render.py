import curses

#Set up text output, so variables for different colours that can be used in windows.

curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) #For when text is selected in menus
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) #PLACEHOLDER, just showcase
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

text_selected = curses.color_pair(1)
text_stats = curses.color_pair(2)
text_new = curses.color_pair(3)
