from art import trophy
from data import monsters
from menus import help_screen
from screen_render import center, clear_screen, col, get_key, put, show
from state import g

#Shows the victory screen when the player wins
def victory_screen():
    p, md = g["player"], g["mapdef"]
    width = 0
    for line in trophy:
        width = max(width, len(line))
    left = (80 - width) // 2 #Centers ASCII art
    while True:
        clear_screen()
        for i, line in enumerate(trophy):
            put(1 + i, left, line, col("yellow", bold=True))
        center(12, f"*** YOU CONQUERED {md['name'].upper()}! ***", col("green", bold=True))
        center(14, f"{p['name']} defeated {monsters[md['boss']]['name']} and escaped.")
        stats = [f"Monsters slain: {g['kills']}", f"Times defeated: {g['deaths']}", f"Gold on hand: {p['gold']}"]
        for i, text in enumerate(stats):
            center(16 + i, text, col("cyan"))
        center(23, "Press ENTER to continue   H: help", col(dim=True))
        show()
        k = get_key()
        if k == "ENTER":
            return
        if k == "h":
            help_screen()
