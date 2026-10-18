import curses

# Just acting as a library for colour pairs so we can all call the same colour pairs, and also manage drawing borders.
W_HEIGHT = 22
W_WIDTH = 79
active_windows = {} #Dict for active windows, when creating windows will access dict for window data.
# If there's more windows, will access coordinates, menus, and access them based on that (which is how the inventory can visually update.)
# active_windows = {
#
#   [[windownumber, windowname, windowtype],[item, item2, item3, ...],[x1, y1, x2, y2],[asset_sprite1, asset_sprite2]]
#   #Can directly access window data once the window has been created, can edit items, etc.
# }
#

def setup_colors():
    #creates color and text attribute templates for use in window systems.
    curses.start_color()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    global menu_text_select; menu_text_select = curses.color_pair(1) #base variable
    global menu_text_select_bold; menu_text_select_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_BLINK #when selected with cursor/arrow keys, UI item will blink. Can add more colors later.
    global menu_text; menu_text = curses.color_pair(1) | curses.A_REVERSE  #
    global menu_text_bold; menutext_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE


def window_create(windownumber:int, windowname:str, windowtype:str): #Adds window to memory (dict).
    active_windows[windownumber] = [[windownumber, windowname, windowtype],[],[],[]]

#Drawing window border. Can use for various window purposes. Planning to have this be part of a custom window making function.
def draw_border(stdscr, x1:int, y1:int, x2:int, y2:int, windownumber:int):
    if len(active_windows[windownumber][2]) > 0: #overwrites if there already are coords for window, incase mistake is made.
        x1 = active_windows[windownumber][2][0]
        y2 = active_windows[windownumber][2][1]
        x2 = active_windows[windownumber][2][2]
        y2 = active_windows[windownumber][2][3]
    #draws window border.
    #TREAT X AND Y COORDS AS IF THEY START FROM 0 LIKE ADDSTR FUNCTIONS!!!
    #Need at least 2 coord difference between initial and final coords otherwise an error will occur lol
    if x2 < x1 or y2 < y1:
        raise ValueError("second coordinate parameter cannot be smaller than first coordinate parameter!")
    coords = [x1,y1,x2,y2]
    active_windows[windownumber][2].extend(coords) #adds coordinates to active window memory. Will be important later.
    
    stdscr.addstr(y1 , x1, "╔")
    stdscr.addstr(y1, x2, "╗")
    stdscr.addstr(y2, x1, "╚")
    stdscr.addstr(y2, x2, "╝") 
    step_x = x2 - x1
    step_y = y2 - y1
    range_x = step_x
    range_y = step_y
    for i in range(range_x - 1):
        stdscr.addstr(y1, x1 + i + 1, "═")
    for i in range(range_x - 1):
        stdscr.addstr(y2, x1 + i + 1, "═")
    for i in range(range_y - 1):
        stdscr.addstr(y1 + i + 1, x1, "║")
    for i in range(range_y - 1):
        stdscr.addstr(y1 + i  +1, x2, "║")

#