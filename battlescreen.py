import time
from battle import can_use_move, grant_rewards, log, new_battle, play_round, rows_in_order
from data import items
from fighters import fresh_battle_state, item_ids_in_bag
from menus import help_screen
from screen_render import clear_screen, get_key, put, show
from state import bs, g
from texts import atk_text, battle_summary, def_text, item_summary, move_cost, status_tags
from textwrap import wrap


#if hp/mp full send notice when trying to using corresponding items
def refuse(data,ident):
    inf = items[ident]
    if "hp" in inf  and data["hp"] >= data["max_hp"]:
        return "hp is already full"
    if "mp" in inf and data["mp"] >= data["max_mp"]:
        return "mp is already full"
    return ""
#battle selection for choosing to use power or using item
def confirm_choice(b, mode, cur, item_ids):
    if mode == "main":
        if cur == 0:
            return "fight", 0, "", None
        if item_ids:
            return "item", 0, "", None
        return mode, cur, "Your bag is empty!", None
    if mode == "fight":
        if can_use_move(b, cur):
            return mode, cur, "", ("move", cur)
        return mode, cur, "Not enough MP!", None
    ident = item_ids[cur]
    notice = refuse(b["p"], ident)
    if notice:
        return mode, cur, notice, None
    return mode, cur, "", ("item", ident)

# Make the readable text for the battle
def battle_entries(b, mode, item_ids):
    p = b["p"]
    if mode == "main":
        return ["FIGHT", "ITEM"]
    entries = []
    if mode == "fight":
        for move in p["moves"]:
            description = battle_summary(move, p, b["m"])
            entries.append(f"{move['name']}  {move_cost(move)}  - {description}")
    else:
        for ident in item_ids:
            name = items[ident]["name"]
            count = p["items"][ident]
            entries.append(f"{name} x{count}  - {item_summary(items[ident])}")
    return entries

#putting the action by player into the corresponding position
def battle_menu(b):
    mode, cur, notice = "main", 0, ""
    while True:
        item_ids = item_ids_in_bag(b["p"])
        entries = battle_entries(b, mode, item_ids)
        cur = min(cur, max(0, len(entries) - 1))
        draw_battle(b, entries, cur, notice)
        k = get_key()
        if k == "h":
            help_screen()
            continue
        if k == "RESIZE":
            continue
        notice = ""
        if k in ("ESC", "b"):
            mode, cur = "main", 0
            continue
        if k in ("UP", "LEFT") and entries:
            cur = (cur - 1) % len(entries)
        elif k in ("DOWN", "RIGHT") and entries:
            cur = (cur + 1) % len(entries)
        elif k in ("1", "2", "3", "4") and int(k) <= len(entries):
            cur = int(k) - 1
            k = "ENTER"
        if k == "ENTER" and entries:
            mode, cur, notice, choice = confirm_choice(b, mode, cur, item_ids)
            if choice is not None:
                return choice



#Show battle messages, six lines per page.
def show_round(b):
    lines = []
    for row in rows_in_order(b):
        lines += b["rows"][row]
        b["rows"][row] = []
    if not lines:
        return
    bs["lines"] = lines
    bs["log_top"] = 0
    while True:
        more = bs["log_top"] + 6 < len(lines)
        notice = "More battle messages" if more else ""
        draw_battle(
            b, [], 0, notice,
            more=more, animate=True
        )
        if not more:
            return
        #Wait for Enter before revealing the next page.
        while True:
            k = get_key()
            if k == "ENTER":
                bs["log_top"] += 6
                break
            elif k == "h":
                help_screen()
                #Restore the page without replaying its animation.
                draw_battle(b, [], 0, notice, more=True)
# call the infor and determine the battle finished screen include the reward( link data for display and data)
def finish_battle(b):
    rewards = None
    if b["over"] == "win":
        rewards = grant_rewards(b)
    while True:
        draw_battle(b, [], 0, f"Battle result: {b['over']}")
        k = get_key()
        if k == "ENTER":
            b["p"].update(fresh_battle_state())
            return b["over"], rewards
        if k == "h":
            help_screen()


# build the structure for the whole battle connect all the battle relevant function together
#give a complete run
# firstly read infor for the battle. Then start each round
#including showing battle message and let player to use item or move
#finally finish the battle
def run_battle(mon):
    data = g["player"]
    b = new_battle(data, mon)
    bs["lines"] = []
    log(b, f"{mon['name']} appears!")
    show_round(b)
    while not b["over"]:
        kind, value = battle_menu(b)
        if kind == "move":
            play_round(b, ("move", data["moves"][value]))
        else:
            play_round(b, ("item", value))
        show_round(b)
    return finish_battle(b)
#display player and enemy current status information
#Display the hero on the left and the enemy on the right.
def draw_fighters(b):
    p, m = b["p"], b["m"]
    title = "BOSS BATTLE" if m["boss"] else "BATTLE"
    put(0, 2, title)
    for fighter, column in ((p, 2), (m, 42)):
        put(2, column, fighter["name"][:36])
        put(3, column, f"HP {fighter['hp']}/{fighter['max_hp']}")
        if fighter["is_player"]:
            put(4, column, f"MP {fighter['mp']}/{fighter['max_mp']}")
        stats = (
            f"ATK {atk_text(fighter)}  "
            f"DEF {def_text(fighter)}  "
            f"SPD {fighter['spd']}"
        )
        put(5, column, stats[:36])
        status = "Status: " + (
            ", ".join(status_tags(fighter)) or "None"
        )
        for offset, text in enumerate(wrap(status, width=36)[:2]):
            put(6 + offset, column, text)
    for row in range(2, 8):
        put(row, 40, "|")

#draw the battle screen, display the battle to player
def draw_battle(b, entries, cur, notice, more=False, animate=False):
    clear_screen()
    draw_fighters(b)
    top = bs.get("log_top", 0)
    if not animate:
        for i, line in enumerate(bs["lines"][top:top + 6]):
            put(8 + i, 2, line[:78])
    for i, label in enumerate(entries):
        marker = "  "
        if i == cur:
            marker = "> "
        put(15 + i, 2, f"{marker}{i + 1}. {label}"[:76])
    put(20, 2, notice[:76])
    if more:
        put(23, 2, "ENTER next messages   H help")
    elif not b["over"]:
        put(22, 2, "UP/DOWN select   ENTER confirm   1-4 choose")
        put(23, 2, "ESC/B back   H help")
    else:
        put(23, 2, "ENTER continue   H help")
    show()
    #Print battle message one character at a time at 0.02s intervals
    if animate:
        for i, line in enumerate(bs["lines"][top:top + 6]):
            for column, character in enumerate(line[:78], 2):
                put(8 + i, column, character)
                show()
                time.sleep(0.02)
