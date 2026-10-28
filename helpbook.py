import textwrap

from game.data import tag_colors

#Basic game info
help = [ 
    ("EXPLORING", "yellow"),
    ("Move: arrow keys or W A S D      Interact: E", None),
    ("Inventory: I   Help: H   Leave the map: ESC (progress is lost)", None),
    ("Stand NEXT TO a monster and press E to fight it.", None),
    ("Stand ON a $ shop tile and press E to trade.", None),
    ("", None),
    ("BATTLE (turn-based)", "yellow"),
    ("FIGHT: 4 moves. They cost MP (you regain 2 MP every turn).", None),
    ("ITEM : food heals, tonics restore MP, bombs hurt. Uses your turn.", None),
    ("The faster fighter acts first. Armor (DEF) reduces damage taken.", None),
    ("", None),
    ("TIPS", "yellow"),
    ("Gear you find or buy is equipped automatically if it is better.", None),
    ("The old piece goes to your bag and can be sold at a shop.", None),
    ("If you lose a fight you wake at the start with half your gold.", None),
]

# Legend, showing what each icon means on the map, as sprites cannot fit on the map, so they are substituted by letters/symbols
legend = [
    [("@", "white"), (" you   ", None), ("$", "green"), (" shop   ", None),
     ("E", "cyan"), (" exit   ", None), ("#", "blue"), (" wall   ", None),
     ("1 2 3", "red"), (" must-fight, in order", None)], #Each nested list is a separate line
    
    [("s", "green"), (" slime   ", None), ("g", "yellow"), (" goblin   ", None),
     ("S", "white"), (" skeleton   ", None), ("b", "magenta"), (" bat   ", None),
     ("x", "red"), (" spider", None)],
    
    [("w", "white"), (" wolf   ", None), ("a", "magenta"), (" acolyte   ", None),
     ("O", "green"), (" orc   ", None), ("G", "white"), (" golem", None)],
    
    [("Bosses guard the exit:   ", None), ("I", "red"), (" Infernus   ", None),
     ("K", "cyan"), (" Kronos   ", None), ("M", "magenta"), (" Morvain", None)],
]

#This shows what all the statuses mean
status_help = [
    (["<STUN>"],
     "The fighter loses its next turn, then cannot be stunned again for 3 turns."),
    (["<BLEED> <POISON>", "<CURSE>"],
     "Damage at the end of every turn for 3 turns. The same kind of hit starts "
     "it over."),
    (["<ATK+> <DEF+>"],
     "Attack / defense raised for a few turns."),
    (["<ATK-> <DEF->"],
     "Attack / defense lowered for a few turns."),
    (["<REGEN>"],
     "Heals 15% of max HP at the end of each turn for 3 turns."),
    (["<CHARGE>"],
     "A monster is charging a big attack. It fires on its next turn!"),
]

#Setting up rows for the first page (basic help + legend)
def how_to_rows():
    rows = []
    for text, color in help:
        rows.append([(1, text, color)])
    rows.append([])
    rows.append([(1, "LEGEND", "yellow")])
    for pieces in legend:
        x = 1
        row = []
        for text, color in pieces:
            row.append((x, text, color))
            x += len(text)
        rows.append(row)
    return rows


#Setting up rows for the second page (Status effects)
def status_rows():
    rows = [[(1, "These tags appear next to a name in battle.", None)], []]
    for tags, text in status_help:
        lines = textwrap.wrap(text, 56)
        for i in range(max(len(tags), len(lines))):
            row = []
            if i < len(tags):
                row = tag_pieces(tags[i])
            if i < len(lines):
                row.append((23, lines[i], None))
            rows.append(row)
        rows.append([])
    rows.append([(1, "Boss rage: at half HP a boss gains +25% ATK for the rest of the fight.", "yellow")]) #Extra status effects
    rows.append([(1, "Attacks never miss, but their extra effects only happen some of the time.", "yellow")]) #Extra tips
    return rows

#Sets up the two pages of the helpbook, giving it a title as well
def build_help_pages():
    return [("HOW TO PLAY", how_to_rows()),
            ("STATUS EFFECTS", status_rows())]

#This makes it so while that <BLEED> and <POISON> are put in the same line they have different text colors in the helpbook (saves lines)
def tag_pieces(tags_text):
    pieces = []
    x = 1
    for word in tags_text.split(" "):
        pieces.append((x, word, tag_colors[word.strip("<>")]))
        x += len(word) + 1
    return pieces