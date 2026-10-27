"""
4 function in the maze system:
    load_maze(file_path)
    move_player(maze_map, dead_monsters, mandatory_monsters, optional_monsters, px, py, dx, dy)
    mark_monster_dead(dead_monsters, x, y)
    render_maze(maze_map, player_x, player_y, mandatory_monsters, optional_monsters, dead_monsters)
"""


#Read maze text file and parse maze data.
#The file_path is the type of the maze: easy, medium, hard

def load_maze(file_path):
   
    maze_map = []
    mandatory_monsters = set()
    optional_monsters = set()
    start_x = None
    start_y = None

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    for y, line in enumerate(lines):
        row = list(line)
        for x, ch in enumerate(row):
            if ch == "@":
                start_x = x
                start_y = y
                row[x] = " "
            elif ch == "M":
                mandatory_monsters.add((x, y))
            elif ch == "m":
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
    if target_cell == "S":
        return tx, ty, "shop"

    # boss B
    if target_cell == "B":
        return tx, ty, "boss_combat"

    # normal passable floor
    return tx, ty, None


def mark_monster_dead(dead_monsters, x, y):
    """
    Mark one monster as killed. Call this after combat victory.

    Args:
        dead_monsters: set[tuple[int,int]]
        x, y: int, coordinate of dead monster (x, y)
    """
    dead_monsters.add((x, y))


#Generate maze text lines for UI rendering. No print inside this function.
def render_maze(maze_map, player_x, player_y, mandatory_monsters, optional_monsters, dead_monsters):


    output_lines = []
    height = len(maze_map)
    for y in range(height):
        line_buf = []
        row = maze_map[y]
        for x in range(len(row)):
            if x == player_x and y == player_y:
                line_buf.append("@")
            elif (x, y) in mandatory_monsters:
                if (x, y) in dead_monsters:
                    line_buf.append(".")
                else:
                    line_buf.append("M")
            elif (x, y) in optional_monsters:
                if (x, y) in dead_monsters:
                    line_buf.append(".")
                else:
                    line_buf.append("m")
            else:
                line_buf.append(row[x])
        output_lines.append("".join(line_buf))
    return output_lines
