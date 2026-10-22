import curses

# Just acting as a library for colour pairs so we can all call the same colour pairs, and also manage drawing borders.
W_HEIGHT = 22
W_WIDTH = 79
active_windows = {} #Dict for active windows, when creating windows will access dict for window data.
# If there's more windows, will access coordinates, menus, and access them based on that (which is how the inventory can visually update.)
# active_windows = {
#
#   windownumber:[[windowname, windowtype],[item, item2, item3, ...],[x1, y1, x2, y2],[asset_sprite1, asset_sprite2]]
#   #Can directly access window data once the window has been created, can edit items, etc.
# }
#
tooltip_string = ""
window_active = False

def setup_colors():
    #creates color and text attribute templates for use in window systems.
    curses.start_color()
    
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED,   curses.COLOR_BLACK)
    
    global menu_text_select; menu_text_select = curses.color_pair(1) #base variable
    global menu_text_select_bold; menu_text_select_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_BLINK #when selected with cursor/arrow keys, UI item will blink. Can add more colors later.
    global menu_text; menu_text = curses.color_pair(1) | curses.A_REVERSE
    global menu_text_bold; menu_text_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_REVERSE
    global text_red_bold; text_red_bold = curses.color_pair(3) | curses.A_BOLD

def blank_rect(stdscr, top, left, height, width, attr=0):
    line = " " * width
    for y in range(top, top + height):
        stdscr.addstr(y, left, line, attr)
    stdscr.refresh()
    

def window_create(windownumber:int, windowname:str, windowtype:str): #Adds window to memory (dict).
    active_windows[windownumber] = [[windownumber, windowname.lower(), windowtype.lower()],[],[],[]]

#Drawing window border. Can use for various window purposes. Planning to have this be part of a custom window making function.
def draw_border(stdscr, x1:int, y1:int, x2:int, y2:int, windownumber:int):
    # If the window already has stored coords, use those instead
    if len(active_windows[windownumber][2]) >= 4:
        x1, y1, x2, y2 = active_windows[windownumber][2][:4]
    else:
        active_windows[windownumber][2][:] = [x1, y1, x2, y2]

    if x2 <= x1 or y2 <= y1:
        raise ValueError("x2/y2 must be greater than x1/y1")

    stdscr.addstr(y1, x1, "╔"); stdscr.addstr(y1, x2, "╗")
    stdscr.addstr(y2, x1, "╚"); stdscr.addstr(y2, x2, "╝")
    for i in range(x2 - x1 - 1):
        stdscr.addstr(y1, x1 + i + 1, "═")
        stdscr.addstr(y2, x1 + i + 1, "═")
    for i in range(y2 - y1 - 1):
        stdscr.addstr(y1 + i + 1, x1, "║")
        stdscr.addstr(y1 + i + 1, x2, "║")

def add_menu_button(windownumber:int, buttonname:str): #adding buttons to an active window.
    active_windows[windownumber][1].append(buttonname)



def draw_menu(stdscr, windownumber:int, button_padding_x:int, button_padding_y:int, rows:int, columns:int):
    #Draws menu buttons within the window.
    #using x1, y1, x2, y2, defines dimensions to arrange grids in. 
    #for rows, column, need to trim button name to fit, display button name on tooltip
    
    if rows < 1 or columns < 1:
        raise ValueError("Cannot have row or column value less than one!")
    if button_padding_x < 0 or button_padding_y < 0:
        raise ValueError("Cannot have padding value below zero!")
    
    x1, y1, x2, y2 = active_windows[windownumber][2][:4]
    buttons        = active_windows[windownumber][1]
    if not buttons:
        return None
    
    inner_left   = x1 + 1
    inner_top    = y1 + 1
    inner_width  = (x2 - x1) - 1      # width between the window sides
    inner_height = (y2 - y1) - 1      # height between the window top and bottom

    cell_width   = max(1, inner_width // columns)   # one column of the grid
    cell_height  = 1 + button_padding_y             # 1 text row + vertical gap
    
    def button_rect(index):
        r = index // columns
        c = index % columns
        bx = inner_left + c * cell_width + button_padding_x
        by = inner_top  + r * cell_height + button_padding_y
        bw = max(1, cell_width - 2 * button_padding_x)
        return bx, by, bw

    visible = buttons[: rows * columns]   #no pages so far I don't want to implement that hellish thing

    def render(selected):
        for i, name in enumerate(visible):
            bx, by, bw = button_rect(i)
            label = name[:bw].ljust(bw)
            attr  = menu_text_select_bold if i == selected else menu_text
            stdscr.addstr(by, bx, label, attr)
            stdscr.addstr(23, 0, f"                                                                    ")
            stdscr.addstr(23, 0, f"{active_windows[windownumber][0][0]}: {active_windows[windownumber][1][selected]}")
        stdscr.refresh()
    #calculate area for buttons, account for padding, rows, columns.
    
    selected = 0
    total = len(visible)

    while True:
        render(selected)
        key = stdscr.getch()

        if key in (curses.KEY_LEFT,  ord('a')): 
            selected = (selected - 1) % total #makes the selected button visible
        elif key in (curses.KEY_RIGHT, ord('d')): 
            selected = (selected + 1) % total
        elif key in (curses.KEY_UP, ord('w')):
            selected = (selected - columns) % total
        elif key in (curses.KEY_DOWN, ord('s')):
            selected = (selected + columns) % total
        elif key in (curses.KEY_ENTER, 10, 13):
            return visible[selected]          # ← the chosen button
        elif key == 27:                       # ESC
            return None
   

   
    