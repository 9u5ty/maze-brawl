from pathlib import Path
from data import monsters
from fighters import new_monster

#Read maze text file and parse maze data.
#The file_path is the type of the maze: easy, medium, hard

def load_maze(file_path):
   
    maze_map = []
    mandatory_monsters = set()
    optional_monsters = set()
    start_x = None
    start_y = None

    mandatory_chars = {"1", "2", "3"}
    optional_chars = {"a", "b", "c", "d", "e", "f"}

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()


    for y, line in enumerate(lines):
        row = list(line)
        for x, ch in enumerate(row):
            if ch == "@":
                start_x = x
                start_y = y
                row[x] = " "
            elif ch in mandatory_chars:
                mandatory_monsters.add((x, y))
            elif ch in optional_chars:
                optional_monsters.add((x, y))
        maze_map.append(row)

    return maze_map, start_x, start_y, mandatory_monsters, optional_monsters

# What will returns:
#maze_map: list[list[str]]
# start_x, start_y: int, player spawn position (x: horizontal, y: vertical)
# mandatory_monsters: set[tuple[int, int]], coordinates of M monsters (x, y)
#optional_monsters: set[tuple[int, int]], coordinates of m monsters (x, y)


#Player movement and confirm the status

def move_player(maze_map, dead_monsters, mandatory_monsters, optional_monsters, px, py, dx, dy):
    
    height = len(maze_map)
    width = len(maze_map[0])
    tx = px + dx
    ty = py + dy

    # out‑of‑bounds check
    if ty < 0 or ty >= height or tx < 0 or tx >= width:
        return px, py, None

    target_cell = maze_map[ty][tx]

    # wall cannot pass
    if target_cell == "#":
        return px, py, None

    # mandatory monster M
    if (tx, ty) in mandatory_monsters:
        if (tx, ty) not in dead_monsters:
            return px, py, "mandatory_combat"
        else:
            return tx, ty, None

    # optional monster m
    if (tx, ty) in optional_monsters:
        if (tx, ty) not in dead_monsters:
            return px, py, "combat"
        else:
            return tx, ty, None

    # shop S
    if target_cell in "456":
        return tx, ty, "shop"

    # boss B
    if target_cell == "B" and (tx, ty) not in dead_monsters:
        return tx, ty, "boss_combat"

     # exit E
    if target_cell == "E":
        return tx, ty, "exit"

    
    # normal passable floor
    return tx, ty, None

   # Mark one monster as killed. Call this after combat victory.
def mark_monster_dead(dead_monsters, x, y):
    dead_monsters.add((x, y))

def render_maze(maze_map, player_x, player_y, mandatory_monsters,optional_monsters, dead_monsters, mapdef=None):

    output_lines = []
    height = len(maze_map)
    for y in range(height):
        line_buf = []
        row = maze_map[y]
        for x in range(len(row)):
            ch = row[x]
            if x == player_x and y == player_y:
                line_buf.append("@")
            elif (x, y) in dead_monsters:
                line_buf.append(" ")
            elif ch in "456":
                line_buf.append("$")
            elif mapdef is not None and ch in "123abcdefB":
                key = monster_key(mapdef, ch)
                line_buf.append(monsters[key]["glyph"])
            else:
                line_buf.append(ch)
        output_lines.append("".join(line_buf))
    return output_lines

def monster_key(mapdef, ch):
    if ch in "123":
        return mapdef["path_monsters"][int(ch) - 1]
    if ch in "abcdef":
        return mapdef["optional"][ord(ch) - ord("a")]
    if ch == "B":
        return mapdef["boss"]
    raise ValueError(f"Not a monster marker: {ch!r}")

maps_dir = Path(__file__).resolve().parent / "maps"
def load_map(mapdef):
    rows, sx, sy, _, _ = load_maze(maps_dir / mapdef["file"])
    maze = {
        "def": mapdef,
        "start": (sx, sy),
        "wall": [],
        "entities": []
    }
    for y, row in enumerate(rows):
        maze["wall"].append([ch == "#" for ch in row])
        for x, ch in enumerate(row):
            if ch in "123abcdefB":
                maze["entities"].append({
                    "kind": "monster",
                    "x": x,
                    "y": y,
                    "dead": False,
                    "mon": new_monster(monster_key(mapdef, ch))
                })
            elif ch in "456E":
                entity = {
                    "kind": "exit" if ch == "E" else "shop",
                    "x": x,
                    "y": y,
                    "dead": False
                }
                if ch != "E":
                    entity["shop"] = int(ch) - 4
                maze["entities"].append(entity)
    return maze

def entity_at(maze, x, y):
    for e in maze["entities"]:
        if e["x"] == x and e["y"] == y and not e["dead"]:
            return e
    return None

def is_blocked(maze, x, y):
    if not (0 <= x < 79 and 0 <= y < 19):
        return True
    if maze["wall"][y][x]:
        return True
    e = entity_at(maze, x, y)
    if e is not None and e["kind"] == "monster":
        return True
    return False

dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
def nearby(maze, x, y):
    e = entity_at(maze, x, y)
    if e and e["kind"] == "shop":
        return e
    for dx, dy in dirs:
        e = entity_at(maze, x + dx, y + dy)
        if e and e["kind"] == "monster":
            return e
    return None