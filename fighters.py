from data import heroes, moves

#Return brand‑new clean battle‑only state for hero / monster.
#twhen you use this funtion you can just name the dictionary as you want. 
#example: dictionary_name = fresh_battle_state()
def  fresh_battle_state():
    return {"status": {}, "charging": None, "stunned": False, "stun_immune": 0}

# Build new player hero instance from hero template in data.py
# This function will out put a dictionary and you just need to input the name of hero
#example: dictionary_name = new_player(hero_key), here hero_key is the name of the hero
def new_player(hero_key):
    h= heroes[hero_key]
    p={}
    p["is_player"] = True
    p["key"] = hero_key
    p["name"] = h["name"]
    p["hp"] = h["hp"]
    p["max_hp"] = h["hp"]
    p["mp"] = h["mp"]
    p["max_mp"] = h["mp"]
    p["atk"] = h["atk"]
    p["def"] = h["def_"] 实例def
    p["spd"] = h["spd"]
    p["passive"] = h["passive"]
#create the move list
    moves=[]
    for move_key in h["moves"]:
        moves.append(moves[move_key])
    p["moves"]=moves
#other values
    p["weapon"] = h["weapon"]
    p["armour"] = h["armour"]
    p["items"] = dict(h["items"]) 
    p["bag"] = []
    p["gold"] = 0
#before the battle's state
    p.update(fresh_battle_state())
    return p
    

