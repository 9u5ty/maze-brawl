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

def get_keys(stdscr):
    key = stdscr.getch()
    return key


def window_create(windownumber:int, windowname:str, windowtype:str, x1:int, y1:int, x2:int, y2:int): #Adds window to memory (dict).
    active_windows[windownumber] = [[windowname, windowtype.lower()],[],[x1, y1, x2, y2],[]]

#Drawing window border for selected window (maybe should put this in ).
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

def clear_window(stdscr, windownumber:int, attr=0):
    x1, y1, x2, y2 = active_windows[windownumber][2][:4]
    width = x2 - x1 - 1
    blank = " " * width
    for y in range(y1 + 1, y2):
        stdscr.addstr(y, x1 + 1, blank, attr)

def wrap_text(text):
    pass

def draw_menu(stdscr, windownumber:int, button_padding_x:int, button_padding_y:int, rows:int, columns:int):
    #Draws menu buttons within the window.
    #using x1, y1, x2, y2, defines dimensions to arrange grids in.
    #for rows, column, need to trim button name to fit, display button name on tooltip

    if rows < 1 or columns < 1:
        raise ValueError("Cannot have row or column value less than one!")
    if button_padding_x < 0 or button_padding_y < 0:
        raise ValueError("Cannot have padding value below zero!")

    x1, y1, x2, y2 = active_windows[windownumber][2][:4]
    buttons = active_windows[windownumber][1]
    if not buttons:
        return None

    inner_left = x1 + 1
    inner_top = y1 + 1
    inner_width = (x2 - x1) - 1      # width between the window sides

    cell_width  = max(1, inner_width // columns)   # one column of the grid
    cell_height  = 1 + button_padding_y             # 1 text row + vertical gap

    next_window_name = active_windows[windownumber + 1][0][0] if len(active_windows) > 1 else None
    next_window_type = active_windows[windownumber + 1][0][1] if len(active_windows) > 1 else None

    has_description = (
        windownumber + 1 in active_windows
        and active_windows[windownumber + 1][0] == ["Description", "text"]
    )

    if has_description:
        display_text = list(active_windows[windownumber + 1][1])
        display_x1, display_y1, display_x2, display_y2 = active_windows[windownumber + 1][2][:4]

    def button_rect(index):
        r = index // columns
        c = index % columns
        bx = inner_left + c * cell_width + button_padding_x
        by = inner_top  + r * cell_height + button_padding_y
        bw = max(1, cell_width - 2 * button_padding_x)
        return bx, by, bw

    visible = buttons[: rows * columns]   #no pages so far I don't want to implement that hellish thing

    if next_window_name == "Description" and next_window_type == "text":
        display_text = []
        for i in range(len(active_windows[windownumber + 1][1])):
            display_text.append(active_windows[windownumber + 1][1][i])

        display_x1, display_y1, display_x2, display_y2 = active_windows[windownumber + 1][2][:4]
        display_width = active_windows[windownumber + 1][2][2] - active_windows[windownumber + 1][2][0]
        display_height = active_windows[windownumber + 1][2][3] - active_windows[windownumber + 1][2][1]

# for a window of border coords x1 = 40, y1 = 0, x2, 79, y2 = 22
# width = display width - 2 because of left and right border, need to start by + 1 to index to avoid editing border
# height = display height - 2 because of left, need to start by + 1 to indext to avoid editing border
# have to wrap inside of that, so x1 = 41, y1 = 1, x2 = 78, y2 = 21

    def render(selected):
        #tooltip draws once, depends on button.
        tip_y = min(23, curses.LINES - 1)
        blank_rect(stdscr, tip_y, 0, 1, min(79, curses.COLS))
        tip = f"{active_windows[windownumber][0][0]}: {buttons[selected]}"
        stdscr.addstr(tip_y, 0, tip[:curses.COLS - 1])

        #buttons
        for i, name in enumerate(visible):
            bx, by, bw = button_rect(i)
            label = name[:bw].ljust(bw)
            attr = menu_text_select_bold if i == selected else menu_text
            stdscr.addstr(by, bx, label, attr)

        #menu item description, with text wrapping
        if has_description:
            clear_window(stdscr, windownumber + 1)
            if selected < len(display_text):
                text = display_text[selected]
                row = display_y1 + 1
                col = display_x1 + 1
                max_col = display_x2 - 1
                max_row = display_y2 - 1
                for ch in text:
                    if ch == "\n":
                        row += 1
                        col = display_x1 + 1
                        continue
                    if col >= max_col:
                        row += 1
                        col = display_x1 + 1
                    if row >= max_row:
                        break
                    stdscr.addstr(row, col, ch, menu_text)
                    col += 1

        stdscr.refresh()
    #calculate area for buttons, account for padding, rows, columns.

    selected = 0
    total = len(visible)

    while True:
        render(selected)
        draw_border(stdscr, x1, y1, x2, y2, windownumber)
        if has_description:
            draw_border(stdscr, display_x1, display_y1, display_x2, display_y2, windownumber + 1)
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
        elif key == 27:
            return "escape"
