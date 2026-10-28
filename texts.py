#Purpose of this is to translate data into texts shown on screen

from game.data import gear, items, item_order
from game.fighters import atk_total, calc_damage, def_total

#Verb forms for each DOT (damage over time) effect
dot_verbs = {"bleeding": "bleed", "poisoned": "poison", "cursed": "curse"}

#Battle text for status effects
def effect_texts(mv):
    out = [] #Output
    pre = chance_prefix(mv)  
    if mv.get("stun"): #Output for the stun effect
        out.append(f"{pre}stun")   
    if "dot" in mv: #Output for DOT effects
        label = mv["dot"][2]
        out.append(f"{pre}{dot_verbs.get(label, label)}")
    if "self_buff" in mv: #Output for attack/defense buffs
            stat, amount, turns = mv["self_buff"]
            out.append(f"Your {stat.upper()} {round((amount - 1) * 100)}% for {turns} turns")
    if "debuff" in mv: #Output for attack/defense debuffs
        stat, amount, turns = mv["debuff"]
        if mv.get("power"): #If the move is a damaging move and debuff is a secondary effect
            out.append(f"{pre}lower enemy {stat.upper()} for {turns} turns") 
        else: #If the debuff is a primary effect of the move
            out.append(f"Enemy {stat.upper()} -{round((1 - amount) * 100)}% for {turns} turns")    
    if mv.get("charge"): #Output for charge
        out.append("charges for a turn first")
    if mv.get("cure"): #Output for Clara's skill Holy Light, where negative effects are cured
            out.append("cures all negative status effects")
    return out
#Prefix for a move with secondary effects if it is not guaranteed
def chance_prefix(mv):
    chance = 100 
    if mv.get("power"):
        chance = mv.get("chance", 100)
    if chance < 100:
        return f"{chance}% to "
    return ""

#Summary of move
def move_summary(mv, atk=None, dfn=None):
    parts = [] #Output, in different parts as a move can have 2 effects
    if mv.get("power"): #Output for power of the move in percentage
        if mv.get("scale") == "def": #Damaging moves can scale with either attack or defense
            stat = "DEF"
        else:
            stat = "ATK"
        text = f"Damage {mv['power']}% {stat}"
        parts.append(text)
    if "heal" in mv: #Output for a healing effect
        parts.append(f"Heals {mv['heal']} HP")
    if "hot" in mv: #Output for a heal over time effect
        parts.append(f"Heals {round(mv['hot'][0] * 100)}% HP/turn for {mv['hot'][1]} turns")
    if "drain" in mv: #Output for a health draining effect
        parts.append(f"Heals {int(mv['drain'] * 100)}% of damage")
    parts += effect_texts(mv)
    if "recoil" in mv: #Output for a recoil effect
        parts.append(f"Recoil {mv['recoil']}")
    return ", ".join(parts) #Joins the different parts into one output

#Summary of item
def item_summary(it):
    if "dmg" in it: #If the item does damage
        return f"Deals {it['dmg']} damage"
    parts = []
    if "hp" in it: #If the item restores HP
        parts.append(f"Heals {it['hp']} HP")
    if "mp" in it: #If the item restores MP
        parts.append(f"Restores {it['mp']} MP")
    return ", ".join(parts)

#In battle status tag shown next to hero
dot_tags = {"bleeding": "BLEED", "poisoned": "POISON", "cursed": "CURSE"} #Status tag that will show for DOT effects
def status_tags(f):
    tags = []
    for stat in ("atk", "def"): #Tag for attack buff/debuff
        if stat in f["status"]:
            tag = stat.upper()
            if f["status"][stat][0] > 1:
                tag += "+"
            else:
                tag += "-"
            tags.append(tag)
    if "dot" in f["status"]: #Status tag for DOT effects
        label = f["status"]["dot"][2]
        tags.append(dot_tags.get(label, label.upper()))
    if "hot" in f["status"]: #Status tag for heal over time effects
        tags.append(f["status"]["hot"][2].upper())
    if f["stunned"]: #Status tag for stun effect
        tags.append("STUN")
    if f["charging"]: #Status tag for charge effect
        tags.append("CHARGE")
    return tags

#Gear description (in character selection screen and shop)
def gear_label(gear_id):
    if not gear_id: 
        return "none" #This is here because some characters may not have starting gear
    g = gear[gear_id]
    return f"{g['name']} (+{g['bonus']} {gear_stat_name(g)})" #Outputs the name of gear and bonus in brackets
#This just outputs ATK for weapons and DEF for armor
def gear_stat_name(gear):
    if gear["kind"] == "weapon":
        return "ATK"
    else:
        return "DEF"

#Character stat being shown
def stat_text(base, total):
    add = round(total - base)
    if add == 0:
        return f"{base}" #Outputs the base stat only if there are no added stats
    return f"{base} ({add:+d})" #Outputs the stat as the base stat plus added stats in brackets
#Amount of attack
def atk_text(f):
    return stat_text(f["atk"], atk_total(f))
#Amount of defense
def def_text(f):
    return stat_text(f["def"], def_total(f))

#Cost of moves in MP
def move_cost(mv):
    return f"{mv.get('mp', 0)}MP"

#What the move will do exactly (not in percentage)
def battle_summary(mv, user, target):
    parts = [] 
    dmg = calc_damage(user, target, mv) #Calculates the exact damage that will be dealt
    if dmg: #Output for exact power of move
        parts.append(f"Damage {dmg}")
    if "heal" in mv: #Output for a healing effect
        parts.append(f"Heals {mv['heal']} HP")
    if "hot" in mv: #Output for a heal over time effect
        parts.append(f"Heals {round(user['max_hp'] * mv['hot'][0])} HP/turn for {mv['hot'][1]} turns")
    if "drain" in mv and dmg: #Output for a health draining effect
        parts.append(f"Heals {int(dmg * mv['drain'])} HP")
    parts += effect_texts(mv)
    if "recoil" in mv: #Output for a recoil effect
        parts.append(f"Recoil {mv['recoil']}")
    return ", ".join(parts) #Joins the different parts into one output

#Shows the starting items (with their number) each character starts with in starting screen
def items_label(item_counts):
    parts = [] 
    for item_id in item_order:
        if item_counts.get(item_id):
            parts.append(f"{item_counts[item_id]} {items[item_id]['name']}")
    return ", ".join(parts)