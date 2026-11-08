import curses

# Just acting as a library for colour pairs so we can all call the same colour pairs, and also manage drawing borders.
active_windows = {} #Dict for active windows, when creating windows will access dict for window data.
# If there's more windows, will access coordinates, menus, and access them based on that (which is how the inventory can visually update.)
# active_windows = {
#
#   windownumber:[[windowname, windowtype],[item, item2, item3, ...],[x1, y1, x2, y2],[asset_sprite1, asset_sprite2]]
#   #Can directly access window data once the window has been created, can edit items, etc.
# }
#

_screen = None

def init(stdscr):
    #Call once from main() before anything else.
    global _screen
    _screen = stdscr
    curses.set_escdelay(25)

_COLOR_CODES = {
    "black":   curses.COLOR_BLACK,
    "red":     curses.COLOR_RED,
    "green":   curses.COLOR_GREEN,
    "yellow":  curses.COLOR_YELLOW,
    "blue":    curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan":    curses.COLOR_CYAN,
    "white":   curses.COLOR_WHITE,
}

_fg_pairs = {}

def setup_colors():
    curses.start_color()
    curses.use_default_colors() # allow -1 background

    # og menu pairs
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED,   curses.COLOR_BLACK)

    # Register one pair per named foreground colour on the terminal default bg
    pair_id = 4
    for name, code in _COLOR_CODES.items():
        curses.init_pair(pair_id, code, -1)
        _fg_pairs[name] = pair_id
        pair_id += 1

    global menu_text_select_bold, menu_text
    menu_text_select_bold = curses.color_pair(1) | curses.A_BOLD | curses.A_BLINK
    menu_text             = curses.color_pair(1) | curses.A_REVERSE

def blank_rect(stdscr, top, left, height, width, attr=0):
    line = " " * width
    for y in range(top, top + height):
        stdscr.addstr(y, left, line, attr)
    stdscr.refresh()

def col(color=None, bold=False, dim=False, reverse=False, underline=False):
    attr = curses.color_pair(_fg_pairs[color]) if color else 0
    if bold:      attr |= curses.A_BOLD
    if dim:       attr |= curses.A_DIM
    if reverse:   attr |= curses.A_REVERSE
    if underline: attr |= curses.A_UNDERLINE
    return attr

def hp_color(hp, max_hp):
    if max_hp <= 0:
        return "red"
    ratio = hp / max_hp
    if ratio > 0.6:  return "green"
    if ratio > 0.3:  return "yellow"
    return "red"

def put(row, column, text, attr=0):
    try:
        _screen.addstr(row, column, str(text), attr)
    except curses.error:
        pass # off-screen write — ignore

def clear_screen():
    _screen.clear()

def show():
    _screen.refresh()

def flush_keys():
    curses.flushinp()

def get_key():
    k = _screen.getch()
    if k == -1:              return None
    if k == 27:              return "ESC"
    if k in (10, 13):        return "ENTER"
    if k == curses.KEY_UP:   return "UP"
    if k == curses.KEY_DOWN: return "DOWN"
    if k == curses.KEY_LEFT: return "LEFT"
    if k == curses.KEY_RIGHT:return "RIGHT"
    if k == curses.KEY_RESIZE:return "RESIZE"
    try:
        ch = chr(k).lower()
        return {"w": "UP", "a": "LEFT", "s": "DOWN", "d": "RIGHT"}.get(ch, ch)
    except ValueError:
        return None


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

# for a window of border coords x1 = 40, y1 = 0, x2, 79, y2 = 22
# width = display width - 2 because of left and right border, need to start by + 1 to index to avoid editing border
# height = display height - 2 because of left, need to start by + 1 to indext to avoid editing border
# have to wrap inside of that, so x1 = 41, y1 = 1, x2 = 78, y2 = 21

    def render(selected):
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
                    if col > max_col:
                        row += 1
                        col = display_x1 + 1
                    if row > max_row:
                        break
                    stdscr.addstr(row, col, ch)
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

#Functions below are for popup handling
def center(y, text, attr=0):
    put(y, (80 - len(text)) // 2, text, attr)

def hline(y):
    put(y, 0, "-" * 80)

def popup(lines, title="", keys=("ENTER",), border="yellow"):
    top = (24 - len(lines) - 4) // 2
    _, width = _screen.getmaxyx()
    blank_rect(_screen, top, 0, len(lines) + 4, width)
    put(top, 3, title, col(border, bold=True))
    for i, line in enumerate(lines):
        text, color = (line, None) if isinstance(line, str) else line
        put(top + 2 + i, 3, text[:74], col(color))
    show()
    while True:
        key = get_key()
        if key in keys:
            return key

def confirm(lines, title="", border="yellow"):
    return popup(list(lines) + ["", "[Y] Yes [N] No"], title, keys=("y", "n", "ESC"), border=border) == "y"
