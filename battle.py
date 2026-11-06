import random
from data import items
from fighters import add_item, calc_damage, fresh_battle_state, gain_gear, heal, remove_item, use_food

#Messages are shown in a maximum of 6 rows: The move and effect of both the hero and the enemy, status effect text, and ability activation text.
battle_rows = ["enemy", "enemy effect", "hero", "hero effect", "status", "ability"]
#Determines the order of the effect text, as hero and enemies move first/second based on their speed.
def rows_in_order(b):
    first = b["first"]
    if first == "hero":
        second = "enemy"
    else:
        second = "hero"
    return [first, first + " effect", second, second + " effect", "status", "ability"]

#Start a battle between hero and monster and returns the battle dictionary.
def new_battle(p, m):
    p.update(fresh_battle_state())
    m.update(fresh_battle_state())
    rows = {}
    for row in battle_rows:
        rows[row] = []
    return {"p": p, "m": m, "msgs": [], "rows": rows, "actor": "enemy", "first": "enemy",
            "over": None}

#Remembers the messages that is to be outputted in battle rows in order
def add_message(b, row, text):
    b["msgs"].append(text)
    b["rows"][row].append(text)
#Logs what the fighter did
def log(b, text):
    add_message(b, b["actor"], text)
#Logs the secondary effect of the fighter's moves
def log_effect(b, text):
    add_message(b, b["actor"] + " effect", text)
#Logs the damage of poison, bleeding and curses.
def log_status(b, text):
    add_message(b, "status", text)
#Logs the effects of abilities that occur at the end of a turn
def log_ability(b, text):
    add_message(b, "ability", text)

#Checks if hero has enough MP to use a move
def can_use_move(b, index):
    return b["p"]["mp"] >= b["p"]["moves"][index].get("mp", 0)

#Take HP away from the target, log it, and returns the damage.
def hurt(b, target, dmg):
    dmg = min(dmg, target["hp"])
    target["hp"] -= dmg
    log(b, f"{target["short"]} takes {dmg} damage!")
    return dmg

#Do one move: pay MP, help the user, deal damage, then apply the extra effects.
def use_move(b, user, target, mv, charged=False):
    if mv.get("charge") and not charged: #Charge turn for boss charge moves
        user["charging"] = mv
        log(b, mv["charge"])
        return
    if user["is_player"]:
        user["mp"] -= mv.get("mp", 0) #Subtract MP
    log(b, f"{user["short"]} uses {mv["name"]}!")
    apply_self_effects(b, user, mv)
    dealt = 0
    if mv.get("power"): #Direct attack damage
        dealt = hurt(b, target, calc_damage(user, target, mv))
    if "drain" in mv and dealt: #HP drain
        got = heal(user, int(dealt * mv["drain"]))
        if got:
            log(b, f"{user["short"]} drains {got} HP!")
    apply_target_effects(b, target, mv) #
    if "recoil" in mv: #Recoil
        user["hp"] = max(0, user["hp"] - mv["recoil"])
        log(b, f"{user["short"]} is hurt by recoil! (-{mv["recoil"]})")
    #Final checks
    check_enrage(b) #Checks if boss is enraged
    check_over(b) #Checks if battle is over
#Bosses are enraged (get the rage status) once they are at half HP or less, gaining 25% ATK
def check_enrage(b):
    m = b["m"]
    enrage_at = m["t"].get("enrage_at")
    if not enrage_at or m["enraged"] or m["hp"] <= 0:
        return
    if m["hp"] > enrage_at * m["max_hp"]:
        return
    m["enraged"] = True
    m["status"]["atk"] = [1.25, float("inf")]
    log_ability(b, f"{m["short"]} is enraged!")
#Check if battle is over
def check_over(b):
    if b["over"]:
        return
    if b["m"]["hp"] <= 0: #If enemy dies
        b["over"] = "win"
        log_ability(b, f"{b["m"]["short"]} is defeated!")
    elif b["p"]["hp"] <= 0: #If hero dies
        b["over"] = "lose"
        log_ability(b, f"{b["p"]["name"]} collapses...")

# The hero's turn: skip it if stunned, otherwise use an item or a move.
def player_acts(b, action):
    b["actor"] = "hero"
    p = b["p"]
    if p["stunned"]: #Checks for stun (and stun immunity)
        p["stunned"] = False
        p["stun_immune"] = 3
        log(b, f"{p["name"]} is stunned and can't move!")
    elif action[0] == "item": #Checks if hero used item
        item = items[action[1]]
        remove_item(p, action[1])
        if "dmg" in item: #If fire bomb is being used
            log(b, f"{p["name"]} hurls a {item["name"]}!")
            hurt(b, b["m"], item["dmg"])
            check_enrage(b)
            check_over(b)
        else: #If food is used
            log(b, use_food(p, action[1]))
    else: #Otherwise just use a move, if the hero is not stunned and chose not to use an item
        use_move(b, p, b["m"], action[1])

#Pick monster's moves at random, taking into account weighting
def pick_enemy_move(m):
    moves = m["t"]["moves"]
    weights = []
    for mv in moves:
        weights.append(mv.get("weight", 1))
    return random.choices(moves, weights=weights)[0]

#The monster's turn: it is stunned, or it finishes a charge, or it picks a move at random.
def monster_acts(b):
    b["actor"] = "enemy"
    m = b["m"]
    if m["stunned"]: #Checks for stun (and stun immunity)
        m["stunned"] = False
        m["stun_immune"] = 3
        log(b, f"{m["short"]} is stunned and can't move!")
    elif m["charging"]: #Checks for charging for bosses
        mv = m["charging"]
        m["charging"] = None
        use_move(b, m, b["p"], mv, charged=True)
    else: #Otherwise just use a move
        use_move(b, m, b["p"], pick_enemy_move(m))

#End of a round: heal / poison ticks, buffs wear off, MP and passives.
def end_of_round(b):
    for f in (b["p"], b["m"]):
        if f["stun_immune"]: #Reduce stun immune turns by 1 if stunned before
            f["stun_immune"] -= 1
        if f["hp"] > 0: #Checks for heal over time
            heal_over_time(b, f)
        if "dot" in f["status"] and f["hp"] > 0: #Checks for damage over time
            damage_over_time(b, f)
            check_over(b)
            if b["over"]:
                return
        wear_off_buffs(f) #Buff countdown for ATK/DEF buffs
    passives_and_mp(b)
#Heal over time function
def heal_over_time(b, f):
    if "hot" not in f["status"]:
        return
    hot = f["status"]["hot"]
    got = heal(f, hot[0]) #Heals HP
    hot[1] -= 1 #Ticks down
    if got:
        log_ability(b, f"{f["short"]} regains {got} HP.")
    if hot[1] <= 0:
        del f["status"]["hot"]
#Damage over time function
def damage_over_time(b, f):
    dot = f["status"]["dot"]
    dmg = min(dot[0], f["hp"])
    f["hp"] -= dmg #Reduces HP
    dot[1] -= 1 #Ticks down
    log_status(b, f"{f["short"]} is {dot[2]}! (-{dmg})")
    if dot[1] <= 0:
        del f["status"]["dot"]
#Function accounting for attack/defense buffs wearing off over time
def wear_off_buffs(f):
    for stat in ("atk", "def"):
        if stat in f["status"]:
            f["status"][stat][1] -= 1
            if f["status"][stat][1] <= 0:
                del f["status"][stat]

#What happens each round in a battle
def play_round(b, action):
    p, m = b["p"], b["m"]
    #Checks who is faster. Faster one goes first
    if action[0] == "item" or p["spd"] >= m["spd"]: 
        b["first"] = "hero"
        player_acts(b, action)
        if not b["over"]:
            monster_acts(b)
    else:
        b["first"] = "enemy"
        monster_acts(b)
        if not b["over"]:
            player_acts(b, action)
    if not b["over"]:
        end_of_round(b) #If the battle is not over, perform end of round effects

#After defeating an enemy, drop (random amount of) gold and (possibly) gear
def grant_rewards(b): #Determines gold reward of battle
    p, m = b["p"], b["m"]
    low, high = m["gold"]
    gold = low
    if high > low:
        gold = random.randint(low, high)
    p["gold"] += gold
    drops = [] #Drop list for enemies
    for kind, ident, chance in m["drops"]: #Random roll for drop
        if random.random() * 100 >= chance:
            continue
        #Item drop
        if kind == "item":
            add_item(p, ident)
            drops.append((kind, ident, ""))
            continue
        #Gear drop
        equipped = gain_gear(p, ident)[0]
        if equipped:
            note = "equipped!"
        else:
            note = "kept in bag"
        drops.append((kind, ident, note))
    p["mp"] = p["max_mp"] #MP regeneration
    return gold, drops

#Function for text, ATK becomes attack, DEF becomes defense
def stat_word(stat):
    if stat == "atk":
        return "attack"
    return "defense"

#Self effects that buff user
def apply_self_effects(b, user, mv):
    if "heal" in mv: #Heal effect
        log(b, f"{user["short"]} recovers {heal(user, mv["heal"])} HP!")
    if mv.get("cure"): #Cure effect
        cure_negative_effects(b, user)
    if "self_buff" in mv: #Self buff ATK/DEF
        stat, amount, turns = mv["self_buff"]
        user["status"][stat] = [amount, turns]
        log_effect(b, f"{user["short"]}'s {stat_word(stat)} rose!")
    if "hot" in mv: #Healing over time
        fraction, turns, label = mv["hot"]
        user["status"]["hot"] = [round(user["max_hp"] * fraction), turns, label]
        log_effect(b, f"{user["short"]} is surrounded by healing light!")
#Function accounting for "cure" status which removes negative status effects
def cure_negative_effects(b, user):
    cured = False
    if "dot" in user["status"]:
        del user["status"]["dot"]
        cured = True
    for stat in ("atk", "def"):
        if stat in user["status"] and user["status"][stat][0] < 1:
            del user["status"][stat]
            cured = True
    if cured:
        log_effect(b, f"{user["short"]} is cleansed of all negative effects!")

#Extra target effects on moves
def apply_target_effects(b, target, mv):
    lands = True
    if mv.get("power") and mv.get("chance", 100) < 100: #Chance roll for certain events that are not guaranteed
        lands = random.random() * 100 < mv["chance"]
    if not lands or target["hp"] <= 0:
        return
    if mv.get("stun") and not target["stunned"] and target["stun_immune"] <= 0: #Stun effect, checks if target is not stun immune
        target["stunned"] = True
        log_effect(b, f"{target["short"]} is stunned!")
    if "debuff" in mv: #Debuff effect that lowers ATK/DEF
        stat, amount, turns = mv["debuff"]
        target["status"][stat] = [amount, turns]
        log_effect(b, f"{target["short"]}'s {stat_word(stat)} fell!")
    if "dot" in mv: #DOT effect
        target["status"]["dot"] = list(mv["dot"])
        log_effect(b, f"{target["short"]} is {mv["dot"][2]}!")

#Passive abilities for some heroes
def passives_and_mp(b):
    p = b["p"]
    if p["passive"] == "vigor" and p["hp"] > 0: #Kyle's passive Vigor, which does healing
        got = heal(p, 4)
        if got:
            log_ability(b, f"{p["name"]}'s vigor heals {got} HP.")
    regen = 2
    if p["passive"] == "grace": #Clara's passive Grace, which increases MP regeneration rate
        regen += 1
    p["mp"] = min(p["max_mp"], p["mp"] + regen)