#Defining constants
hero_order = ["kyle","bryce","george","clara"] #Sets the order of the heroes in character selection
mp_regen_per_turn = 2 #All heroes regenerate 2MP per turn
stun_immune_turns = 3 #If a character gets stunned it cannot get stunned in 3 turns
sell_ratio = 0.5 #Sell price is 0.5x the buy price for all shops

#Hero abilities constants
vigor_heal = 4 #Kyle's ability heals 4HP at the end of every turn
plating = 2 #George's ability makes damage -2
grace_bonus_mp = 1 #Clara's ability regenerates 1 extra MP per turn

#Defining colors
#Gives each hero its respective color in game
hero_colors = {
    "kyle": "yellow", 
    "bryce": "red", 
    "george": "blue", 
    "clara": "green"
} 
#Colors for effects
tag_colors = {
    "STUN": "yellow", 
    "BLEED": "red", 
    "POISON": "green", 
    "CURSE": "magenta", 
    "CHARGE": "white", 
    "REGEN": "cyan", 
    "ATK+": "cyan", 
    "DEF+": "cyan", 
    "ATK-": "blue", 
    "DEF-": "blue"
} 

#Shop items
items = {
    "apple": {"name": "Apple", "price": 8, "hp": 25},
    "beef": {"name": "Roast Beef", "price": 20, "hp": 60},
    "tonic": {"name": "Mana Tonic", "price": 12, "mp": 20},
    "bomb": {"name": "Fire Bomb", "price": 24, "dmg": 40, "combat_only": True},
}

# Gear
gear = {
    #Swords
    "wooden_sword": {"name": "Wooden Sword", "kind": "weapon", "bonus": 3, "price": 20},
    "iron_sword": {"name": "Iron Sword", "kind": "weapon", "bonus": 6, "price": 60},
    "steel_sword": {"name": "Steel Sword", "kind": "weapon", "bonus": 9, "price": 90},
    "diamond_sword": {"name": "Diamond Sword", "kind": "weapon", "bonus": 12, "price": 200},
    "mythic_sword": {"name": "Mythic Sword", "kind": "weapon", "bonus": 15, "price": 320},
    #Armors
    "leather_armor": {"name": "Leather Armor", "kind": "armor", "bonus": 3, "price": 40},
    "chainmail": {"name": "Chainmail", "kind": "armor", "bonus": 6, "price": 100},
    "plate_armor": {"name": "Plate Armor", "kind": "armor", "bonus": 9, "price": 180},
    "mythic_armor": {"name": "Mythic Armor", "kind": "armor", "bonus": 12, "price": 300},
}

#Moves
moves = {
    #Kyle
    "slash": {"name": "Slash", "mp": 0, "power": 100},
    "power_strike": {"name": "Stunning Strike", "mp": 8, "power": 175},
    "stunning_strike": {"name": "Stunning Strike", "mp": 8, "power": 100, "stun": True, "chance": 40},
    "second_wind": {"name": "Second Wind", "mp": 10, "heal": 25},

    #Bryce
    "berserk": {"name": "Berserk", "mp": 0,"power": 100, "dot": (3, 3, "bleeding"), "chance": 40},
    "fury": {"name": "Fury", "mp": 8, "power": 150, "debuff": ("def", 0.8, 2), "chance": 3},
    "battle_cry": {"name": "Battle Cry", "mp": 6, "self_buff": ("atk", 1.4, 3)},
    "rampage": {"name": "rampage", "mp": 12, "power": 200, "recoil": 10},

    #George
    "iron_fist": {"name": "Iron Fist", "mp": 0, "power": 100, "debuff": ("atk", 0.8, 2), "chance": 30},
    "fortify": {"name": "Fortify", "mp": 5, "self_buff": ("def", 1.6, 3)},
    "bulwark_blow": {"name": "Bulwark Blow", "mp": 5, "power": 160, "scale": "def", "stun": True, "chance": 25},
    "provoke": {"name": "Provoke", "mp": 4, "debuff": ("atk", 0.75, 3)},

    #Clara
    "smite": {"name": "Smite", "mp": 0, "power": 100},
    "holy_light": {"name": "Holy Light", "mp": 12, "heal": 40, "cure": True},
    "radiance": {"name": "Radiance", "mp": 10, "power": 120, "drain": 0.6},
    "regenerate": {"name": "Regenerate", "mp": 12, "hot": (0.15, 3, "regen")}
}

#Heroes, shows all stats
heroes = {
    "kyle": {
        "name": "Kyle", "cls": "Knight", "role": "Balanced", #Name, class, and role of hero
        "hp": 100, "mp": 30, "atk": 10, "def_": 3, "spd": 6, #Hero base stats
        "weapon": "wooden_sword", "armor": "leather_armor", "items": {"apple": 2, "tonic": 1}, #Hero starting items
        "moves": ["slash", "power_strike", "stunning_strike", "second_wind"], #Hero moveset
        "passive": "vigor", "passive_desc": "Vigor: +4 HP at the end of the turn", #Hero passive ability
    },

    "bryce": {
        "name": "Bryce", "cls": "Berserker", "role": "Attack",
        "hp": 100, "mp": 30, "atk": 15, "def_": 3, "spd": 8, 
        "weapon": "iron_sword", "armor": None, "items": {"apple": 2, "bomb": 1}, 
        "moves": ["berserk", "fury", "battle_cry", "rampage"], 
        "passive": "bloodlust", "passive_desc": "Vigor: +1 ATK per 10 HP missing", 
    },

    "george": {
        "name": "George", "cls": "Guardian", "role": "Defense", 
        "hp": 120, "mp": 30, "atk": 8, "def_": 5, "spd": 2, 
        "weapon": "wooden_sword", "armor": "chainmail", "items": {"apple": 1, "beef": 1}, 
        "moves": ["iron_fist", "fortify", "bulwark_blow", "provoke"], 
        "passive": "plating", "passive_desc": "Plating: hits taken -2", 
    },

    "clara": {
        "name": "Clara", "cls": "Cleric", "role": "Healer", 
        "hp": 100, "mp": 50, "atk": 10, "def_": 3, "spd": 4, 
        "weapon": None, "armor": None, "items": {"apple": 1, "tonic": 1}, 
        "moves": ["smite", "holy_light", "radiance", "regenerate"], 
        "passive": "grace", "passive_desc": "Grace: +1 MP per turn", 
    },
}

#All monster stats
monsters = {
    "maze_slime": {
        "name": "Maze Slime", "hp": 45, "atk": 8, "def_": 1, "spd": 1, "gold": (15, 22), #Monster base stats
        "art": "slime", "color": "green", "glyph": "1", #Monster art and the character that represents the monster on the map
        "moves": [ #Monster moveset
            {"name": "Splash", "weight": 2, "power": 100}, #Weight decides how often a move gets picked, power is the base power of move
            {"name": "Acid Spit", "weight": 1, "power": 60, "dot": (3, 3, "poisoned"), "chance": 60}, #Some moves have a chance to trigger additional effects
        ],
        "drops": [("gear", "leather_armor", 100), ("item", "apple", 80)], #What the monster drops after being defeated
    },

    "goblin_guard": {
        "name": "Goblin Guard", "hp": 70, "atk": 12, "def_": 4, "spd": 7, "gold": (25, 35),
        "art": "goblin", "color": "yellow", "glyph": "2",
        "moves": [
            {"name": "Stab", "weight": 2, "power": 100},
            {"name": "Rusty Slash", "weight": 1, "power": 120},
        ],
        "drops": [("gear", "iron_sword", 100), ("item", "apple", 80)],
    },

    "skeleton_warden": {
        "name": "Skeleton Warden", "hp": 90, "atk": 12, "def_": 8, "spd": 3, "gold": (40, 65),
        "art": "skeleton", "color": "white", "glyph": "3",
        "moves": [
            {"name": "Bone Slash", "weight": 1, "power": 100},
            {"name": "Bone Guard", "weight": 1, "power": 0, "self_buff": ("def", 1.5, 2)},
            {"name": "Bone Crush", "weight": 1, "power": 125},
        ],
        "drops": [("gear", "chainmail", 100), ("item", "beef", 60)],
    },

    "crystal_spider": {
        "name": "Crystal Spider", "hp": 55, "atk": 8, "def_": 3, "spd": 7, "gold": (25, 40),
        "art": "spider", "color": "cyan", "glyph": "1",
        "moves": [
            {"name": "Bite", "weight": 2, "power": 100},
            {"name": "Venom Fang", "weight": 1, "power": 70, "dot": (4, 3, "poisoned"), "chance": 60},
        ],
        "drops": [("gear", "leather_armor", 100), ("item", "tonic", 70)],
    },

    "alpha_wolf": {
        "name": "Alpha Wolf", "hp": 65, "atk": 12, "def_": 2, "spd": 9, "gold": (27, 45),
        "art": "wolf", "color": "red", "glyph": "2",
        "moves": [
            {"name": "Bite", "weight": 2, "power": 100},
            {"name": "Rending Bite", "weight": 1, "power": 75, "dot": (4, 3, "bleeding"), "chance": 60},
        ],
        "drops": [("gear", "chainmail", 100), ("item", "beef", 60)],
    },

    "orc_warchief": {
        "name": "Orc Warchief", "hp": 110, "atk": 15, "def_": 5, "spd": 1, "gold": (50, 80),
        "art": "orc", "color": "green", "glyph": "3",
        "moves": [
            {"name": "Smash", "weight": 2, "power": 100},
            {"name": "Wild Swing", "weight": 1, "power": 125, "stun": True, "chance": 25},
        ],
        "drops": [("gear", "plate_armor", 100), ("item", "beef", 60)],
    },

    "goblin_captain": {
        "name": "Goblin Captain", "hp": 75, "atk": 12, "def_": 4, "spd": 7, "gold": (25, 40),
        "art": "goblin", "color": "yellow", "glyph": "1",
        "moves": [
            {"name": "Stab", "weight": 2, "power": 100},
            {"name": "Rusty Slash", "weight": 1, "power": 120},
        ],
        "drops": [("gear", "iron_sword", 100), ("item", "apple", 80)],
    },

    "skeleton_lord": {
        "name": "Skeleton Lord", "hp": 95, "atk": 15, "def_": 8, "spd": 3, "gold": (45, 65),
        "art": "skeleton", "color": "white", "glyph": "2",
        "moves": [
            {"name": "Bone Slash", "weight": 1, "power": 100},
            {"name": "Bone Guard", "weight": 1, "power": 0, "self_buff": ("def", 1.5, 2)},
            {"name": "Bone Crush", "weight": 1, "power": 125},
        ],
        "drops": [("gear", "chainmail", 100), ("item", "beef", 60)],
    },

    "dark_priest": {
        "name": "Dark Priest", "hp": 75, "atk": 16, "def_": 4, "spd": 5, "gold": (50, 70),
        "art": "acolyte", "color": "magenta", "glyph": "3",
        "moves": [
            {"name": "Shadow Bolt", "weight": 2, "power": 100},
            {"name": "Curse", "weight": 1, "power": 60, "dot": (5, 3, "cursed"), "chance": 70},
            {"name": "Life Siphon", "weight": 1, "power": 80, "drain": 0.5},
        ],
        "drops": [("gear", "steel_sword", 100), ("item", "tonic", 70)],
    },

    "slime": {
        "name": "Green Slime", "hp": 40, "atk": 8, "def_": 1, "spd": 1, "gold": (12, 20),
        "art": "slime", "color": "green", "glyph": "s", "optional": True,
        "moves": [
            {"name": "Splash", "weight": 2, "power": 100},
            {"name": "Acid Spit", "weight": 1, "power": 60, "dot": (3, 3, "poisoned"), "chance": 60},
        ],
        "drops": [("gear", "leather_armor", 60), ("item", "apple", 80)],
    },

    "goblin": {
        "name": "Goblin Raider", "hp": 65, "atk": 12, "def_": 3, "spd": 7, "gold": (20, 32),
        "art": "goblin", "color": "yellow", "glyph": "g", "optional": True,
        "moves": [
            {"name": "Stab", "weight": 2, "power": 100},
            {"name": "Rusty Slash", "weight": 1, "power": 120},
        ],
        "drops": [("gear", "iron_sword", 60), ("item", "apple", 80)],
    },

    "skeleton": {
        "name": "Skeleton Knight", "hp": 85, "atk": 12, "def_": 7, "spd": 3, "gold": (36, 60),
        "art": "skeleton", "color": "white", "glyph": "S", "optional": True,
        "moves": [
            {"name": "Bone Slash", "weight": 1, "power": 100},
            {"name": "Bone Guard", "weight": 1, "power": 0, "self_buff": ("def", 1.5, 2)},
            {"name": "Bone Crush", "weight": 1, "power": 125},
        ],
        "drops": [("gear", "chainmail", 60), ("item", "beef", 60)],
    },

    "bat": {
        "name": "Cave Bat", "hp": 35, "atk": 10, "def_": 0, "spd": 9, "gold": (15, 22),
        "art": "bat", "color": "magenta", "glyph": "b", "optional": True,
        "moves": [
            {"name": "Bite", "weight": 2, "power": 100},
            {"name": "Wing Slap", "weight": 1, "power": 70, "debuff": ("def", 0.85, 2), "chance": 60},
        ],
        "drops": [("gear", "iron_sword", 60), ("item", "apple", 80)],
    },

    "spider": {
        "name": "Giant Spider", "hp": 50, "atk": 10, "def_": 2, "spd": 7, "gold": (20, 35),
        "art": "spider", "color": "red", "glyph": "x", "optional": True,
        "moves": [
            {"name": "Bite", "weight": 2, "power": 100},
            {"name": "Venom Fang", "weight": 1, "power": 70, "dot": (4, 3, "poisoned"), "chance": 60},
        ],
        "drops": [("gear", "leather_armor", 60), ("item", "tonic", 70)],
    },

    "wolf": {
        "name": "White Wolf", "hp": 60, "atk": 12, "def_": 2, "spd": 9, "gold": (24, 40),
        "art": "wolf", "color": "white", "glyph": "w", "optional": True,
        "moves": [
            {"name": "Bite", "weight": 2, "power": 100},
            {"name": "Rending Bite", "weight": 1, "power": 75, "dot": (4, 3, "bleeding"), "chance": 60},
        ],
        "drops": [("gear", "chainmail", 60), ("item", "beef", 60)],
    },

    "acolyte": {
        "name": "Dark Acolyte", "hp": 70, "atk": 16, "def_": 3, "spd": 5, "gold": (45, 65),
        "art": "acolyte", "color": "magenta", "glyph": "a", "optional": True,
        "moves": [
            {"name": "Shadow Bolt", "weight": 2, "power": 100},
            {"name": "Curse", "weight": 1, "power": 60, "dot": (5, 3, "cursed"), "chance": 70},
            {"name": "Life Siphon", "weight": 1, "power": 80, "drain": 0.5},
        ],
        "drops": [("gear", "steel_sword", 60), ("item", "tonic", 70)],
    },

    "orc": {
        "name": "Orc Brute", "hp": 100, "atk": 15, "def_": 5, "spd": 1, "gold": (45, 75),
        "art": "orc", "color": "green", "glyph": "O", "optional": True,
        "moves": [
            {"name": "Smash", "weight": 2, "power": 100},
            {"name": "Wild Swing", "weight": 1, "power": 125, "stun": True, "chance": 25},
        ],
        "drops": [("gear", "plate_armor", 60), ("item", "beef", 60)],
    },

    "golem": {
        "name": "Stone Golem", "hp": 120, "atk": 16, "def_": 9, "spd": 1, "gold": (60, 100),
        "art": "golem", "color": "white", "glyph": "G", "optional": True,
        "moves": [
            {"name": "Slam", "weight": 2, "power": 100, "stun": True, "chance": 20},
            {"name": "Harden", "weight": 1, "power": 0, "self_buff": ("def", 1.3, 2)},
        ],
        "drops": [("gear", "diamond_sword", 60), ("item", "beef", 60)],
    },

    #Bosses
    "dragon": {
        "name": "Infernus the Dragon", "short": "Infernus", #Includes short form name for the boss which is used in battle
        "hp": 160, "atk": 20, "def_": 8, "spd": 5, "gold": (0, 0), 
        "art": "dragon", "color": "red", "glyph": "I", "boss": True, "enrage_at": 0.5, #enrage_at = 0.5 make it so the boss becomes stronger at half health
        "moves": [
            {"name": "Claw Swipe", "weight": 2, "power": 100},
            {"name": "Wing Buffet", "weight": 1, "power": 75, "debuff": ("def", 0.9, 2), "chance": 60},
            {"name": "Inferno Breath", "weight": 1, "power": 180, "charge": "Infernus inhales deeply... flames gather in its throat!"}, #Includes text for when the boss uses a charge attack
        ],
        "drops": [],
    },

    "titan": {
        "name": "Kronos the Titan", "short": "Kronos",
        "hp": 150, "atk": 22, "def_": 10, "spd": 1, "gold": (0, 0),
        "art": "titan", "color": "cyan", "glyph": "K", "boss": True, "enrage_at": 0.5,
        "moves": [
            {"name": "Crystal Slam", "weight": 2, "power": 100, "stun": True, "chance": 15},
            {"name": "Harden", "weight": 1, "power": 0, "self_buff": ("def", 1.3, 2)},
            {"name": "Shard Storm", "weight": 1, "power": 160, "charge": "Kronos's crystals begin to hum and glow!"},
        ],
        "drops": [],
    },

    "necro": {
        "name": "Morvain the Necromancer", "short": "Morvain",
        "hp": 175, "atk": 22, "def_": 6, "spd": 7, "gold": (0, 0),
        "art": "necro", "color": "magenta", "glyph": "M", "boss": True, "enrage_at": 0.5,
        "moves": [
            {"name": "Shadow Bolt", "weight": 2, "power": 100},
            {"name": "Death Curse", "weight": 1, "power": 65, "dot": (6, 3, "cursed"), "chance": 80},
            {"name": "Soul Drain", "weight": 1, "power": 65, "drain": 0.6},
            {"name": "Doom Blast", "weight": 1, "power": 180, "charge": "Morvain raises his staff... dark energy swirls!"},
        ],
        "drops": [],
    },
}

#Defines the three different maps
maps = [
    {
        "key": "labyrinth", "name": "The Labyrinth", "file": "labyrinth.txt", #txt file stores the actual map
        "difficulty": "Easy", "color": "blue", "blurb": "One long, winding stone maze.", #These information show up on the map selection screen
        "boss": "dragon", #Final boss of the map
        "path_monsters": ["maze_slime", "goblin_guard", "skeleton_warden"], #Monsters that appear on the map that must be fought
        "optional": ["bat", "spider", "wolf", "acolyte", "orc", "golem"], #Optional monsters can be fought on the map
        "shops": [ #Defines the three shops that will appear
            ["apple", "beef", "tonic", "bomb", "leather_armor", "iron_sword"], #Items purchasable in Shop 1 of the map
            ["apple", "beef", "tonic", "bomb", "chainmail", "steel_sword"], #Items purchasable in Shop 2 of the map
            ["apple", "beef", "tonic", "bomb", "plate_armor", "diamond_sword"], #Items purchasable in Shop 3 of the map
        ],
    },

    {
        "key": "caverns", "name": "Crystal Cavern", "file": "caverns.txt",
        "difficulty": "Medium", "color": "cyan", "blurb": "Looping caves with open chambers.",
        "boss": "titan",
        "path_monsters": ["crystal_spider", "alpha_wolf", "orc_warchief"],
        "optional": ["slime", "bat", "goblin", "skeleton", "acolyte", "golem"],
        "shops": [
            ["apple", "beef", "tonic", "bomb", "chainmail", "iron_sword"],
            ["apple", "beef", "tonic", "bomb", "plate_armor", "steel_sword"],
            ["apple", "beef", "tonic", "bomb", "plate_armor", "diamond_sword"],
        ],
    },

    {
        "key": "citadel", "name": "Obsidian Citadel", "file": "citadel.txt",
        "difficulty": "Hard", "color": "red", "blurb": "Rooms joined by long corridors.",
        "boss": "necro",
        "path_monsters": ["goblin_captain", "skeleton_lord", "dark_priest"],
        "optional": ["bat", "spider", "goblin", "wolf", "orc", "skeleton"],
        "shops": [
            ["apple", "beef", "tonic", "bomb", "chainmail", "steel_sword"],
            ["apple", "beef", "tonic", "bomb", "plate_armor", "diamond_sword"],
            ["apple", "beef", "tonic", "bomb", "mythic_armor", "mythic_sword"],
        ],
    },
]
