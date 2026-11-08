'''fighters.py
 Responsible for hero/monster creation, stats calculation, damage formula, gear and item logic'''

from data import heroes, monsters, gear, items, moves


def fresh_battle_state():
   # Return brand‑new per‑fight temporary status dict.
    return {
        "status": {},
        "charging": None,
        "stunned": False,
        "stun_immune": 0
    }


#Build a player‑hero dictionary from heroes template in data.py
def new_player(hero_key):

    if hero_key not in heroes:
        return None
    h = heroes[hero_key]
    move_list = []
    for move_key in h["moves"]:
        move_list.append(moves[move_key])

    player_dict = {
        "is_player": True,
        "key": hero_key,
        "name": h["name"],
        "short": h["name"],
        "cls": h["cls"],
        "role": h["role"],
        "max_hp": h["hp"],
        "hp": h["hp"],
        "max_mp": h["mp"],
        "mp": h["mp"],
        "atk": h["atk"],
        "def": h["def_"],
        "spd": h["spd"],
        "moves": move_list,
        "passive": h["passive"],
        "weapon": h["weapon"],
        "armor": h["armor"],
        "items": dict(h["items"]),
        "bag": [],
        "gold": 0
    }
    player_dict.update(fresh_battle_state())
    return player_dict


#Build monster dict, key matches maze text character:

def new_monster(key):

    if key not in monsters:
        return None
    template = monsters[key]
    monster_dict = {
        "is_player": False,
        "key": key,
        "t": template,
        "name": template["name"],
        "short": template.get("short", template["name"]),
        "boss": template.get("boss", False),
        "optional": template.get("optional", False),
        "drops": template["drops"],
        "max_hp": template["hp"],
        "hp": template["hp"],
        "atk": template["atk"],
        "def": template["def_"],
        "spd": template["spd"],
        "gold": template["gold"],
        "enraged": False
    }
    monster_dict.update(fresh_battle_state())
    return monster_dict



#Fully restore monster hp, clear enrage and all battle temporary status.
#Call after player loses combat against this monster.
#m: monster dict
def reset_monster(m):

    m["hp"] = m["max_hp"]
    m["enraged"] = False
    m.update(fresh_battle_state())



#Return numeric bonus of given gear id.
#Return 0 if gear_id is None (empty equipment slot).
def gear_bonus(gear_id):

    if gear_id is None:
        return 0
    return gear[gear_id]["bonus"]


#Return equipment slot name: "weapon" or "armor".
def slot_of(gear_id):
    
    if gear_id is None or gear_id not in gear:
        return None
    if gear[gear_id]["kind"] == "weapon":
        return "weapon"
    else:
        return "armor"



#Base attack value before any buff / debuff multiplier.
#Player adds weapon bonus + bloodlust passive if applicable.
#Monsters return raw atk stat.
#f is the dictionary of player or monster!
def base_atk(f):

    if not f["is_player"]:
        return f["atk"]
    value = f["atk"] + gear_bonus(f["weapon"])
    if f["passive"] == "bloodlust":
        value += (f["max_hp"] - f["hp"]) // 10
    return value


#Base defense value before any buff / debuff multiplier.
#Player adds armor equipment bonus.
def base_def(f):

    if f["is_player"]:
        return f["def"] + gear_bonus(f["armor"])
    return f["def"]



#Get stat buff/debuff multiplier.
#stat: "atk" or "def". Return 1.0 when no status effect present.
#Also accounts for the attack buff for when boss is enraged
def mult(f, stat):

    if stat in f["status"]:
        return f["status"][stat][0]
    if stat == "atk" and f.get("enraged"):
        factor *= 1.25
    return factor


#Total attack = base_atk × buff‑debuff
def atk_total(f):
    
    value = base_atk(f) * mult(f, "atk")
    return value


#Total defense = base_def × buff‑debuff.
def def_total(f):

    return base_def(f) * mult(f, "def")



#Exact move damage calculation.
#Formula: round( stat * power/100 * 20 / (20 + target_def) ), minimum 1 damage.
#Some moves scale from defense instead of attack.
#George passive 'plating' reduces incoming damage.
def calc_damage(user, target, mv):

    if not mv.get("power"):
        return 0

    if mv.get("scale") == "def":
        stat = def_total(user)
    else:
        stat = atk_total(user)

    damage = stat * mv.get("power",0) / 100.0 * 20 / (20 + def_total(target))
    damage = max(1, round(damage))

    if target["is_player"] and target["passive"] == "plating":
        damage = max(1, damage - 2)
    return damage

#Heal fighter, cannot exceed max_hp.
#Return actual hp points gained (0 if already full hp).
def heal(f, amount):

    gained = min(amount, f["max_hp"] - f["hp"])
    f["hp"] += gained
    return gained

#Calculate gold received when selling a piece of gear.
#return int
def sell_value(gear_id):

    if gear_id not in gear:
        return 0
    return int(gear[gear_id]["price"] * 0.5)

#Check whether gear_id is better than player's currently equipped item in that slot.
#Return True / False.
def is_upgrade(p, gear_id):

    if gear_id not in gear:
        return False
    slot = slot_of(gear_id)
    return gear[gear_id]["bonus"] > gear_bonus(p[slot])


#Try to equip gear if it is an upgrade. Old equipment goes to bag.
#p not upgrade: put gear directly into player bag.
#Return tuple (equipped: bool, old_gear_id | None).
def gain_gear(p, gear_id):

    if gear_id not in gear:
        return (False, None)
    slot = slot_of(gear_id)
    if is_upgrade(p, gear_id):
        old_item = p[slot]
        p[slot] = gear_id
        if old_item is not None:
            p["bag"].append(old_item)
        return (True, old_item)
    else:
        p["bag"].append(gear_id)
        return (False, None)


#Take gear from player bag and equip it. Old equipped gear moves into bag.
#return(success: bool, old_item)
def equip_from_bag(p, gear_id):

    if gear_id not in p["bag"]:
        return (False, None)
    p["bag"].remove(gear_id)
    slot = slot_of(gear_id)
    old_item = p[slot]
    p[slot] = gear_id
    if old_item is not None:
        p["bag"].append(old_item)
    return (True, old_item)


#Sell one gear from player bag, add gold to player.
def sell_gear(p, gear_id):

    if gear_id not in p["bag"]:
        return False
    p["bag"].remove(gear_id)
    p["gold"] += sell_value(gear_id)
    return True

#Return sell gold value for consumable item.
def item_sell_value(item_id):
    
    if item_id not in items:
        return 0
    return int(items[item_id]["price"] * 0.5)


#Sell one stack‑count of item, add gold. Item entry removed when count hits zero.
def sell_item(p, item_id):

    if item_id not in p["items"]:
        return False
    remove_item(p, item_id)
    p["gold"] += item_sell_value(item_id)
    return True


 #Increase count of one item in player.items dict.
def add_item(p, item_id):

    if item_id not in {"apple", "beef", "tonic", "bomb"}:
        return
    p["items"][item_id] = p["items"].get(item_id, 0) + 1

#Decrease count for one item
#Delete dictionary key entirely once count <= 0.
def remove_item(p, item_id):

    if item_id not in p["items"]:
        return
    p["items"][item_id] -= 1
    if p["items"][item_id] <= 0:
        del p["items"][item_id]



#Apply food / potion hp & mp restore effect.
#Returns human‑readable result message string.
def use_food(p, item_id):
    """
    
    """
    if item_id not in items:
        return
    it = items[item_id]
    message_parts = []
    if "hp" in it:
        hp_gain = heal(p, it["hp"])
        message_parts.append(f"restored {hp_gain} HP")
    if "mp" in it:
        mp_gain = min(it["mp"], p["max_mp"] - p["mp"])
        p["mp"] += mp_gain
        message_parts.append(f"restored {mp_gain} MP")
    if not message_parts:
        return f"{p['name']} uses {it['name']}, but nothing happened."
    return f"{p['name']} uses {it['name']} and {' and '.join(message_parts)}!"


#Return new list with duplicates removed, preserve first‑seen ordering
def unique(item_list):

    result = []
    for entry in item_list:
        if entry not in result:
            result.append(entry)
    return result

#Get list of item‑ids player currently owns (from items dict keys).
def item_ids_in_bag(p):

    output = []
    for iid in items.keys():
        if p["items"].get(iid, 0) > 0:
            output.append(iid)
    return output
