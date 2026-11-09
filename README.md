# maze-brawl
Python maze crawling game

A turn-based maze crawling game for a terminal. Choose one of four heroes and one of three maps, defeat the monsters guarding the maze, and escape past the boss.

## How to run

Install [Python](https://www.python.org/downloads/) 3.9 or newer, then download and unzip the project folder. Keep the `maps` folder alongside `main.py`.

Run the game in a terminal window at least **80 columns wide and 24 rows high**. Enlarge the window before starting the game.

### macOS

1. Open **Terminal**.
2. Type `cd ` (including the space), drag the unzipped project folder into Terminal, and press **Enter**. Choose the folder containing `main.py`.
3. Start the game:

   ```bash
   python3 -B main.py
   ```

### Windows

1. Install Python with the `py` launcher available.
2. Open **Windows Terminal** or **PowerShell**.
3. Change to the unzipped folder containing `main.py`. For example, replace this path with your own:

   ```powershell
   cd "C:\Users\YourName\Downloads\maze-brawl-main"
   ```

4. Check Python and install [windows-curses](https://pypi.org/project/windows-curses/), which provides the `curses` module on Windows. Installation is needed only once per Python environment:

   ```powershell
   py -m pip install windows-curses
   ```

5. Start the game:

   ```powershell
   py -B main.py
   ```

If `py` is not recognised but `python` works, use `python` in place of `py` in all three commands above.

The `-B` option prevents Python from creating `__pycache__` files.

## Controls

- Arrow keys / WASD: move or select
- Enter/Return: confirm a selection
- E: interact with an adjacent monster or a shop beneath you
- I: inventory
- H: opens help menu that offers help during play
- ESC: go back; during exploration, confirm leaving the current run
- Select Quit in the main menu: close the game

Note: Runs are not saved. A defeat restores HP/MP and sends you to the start, costing half your gold. Better gear is equipped automatically, and old gear stays in your bag.

## Contributions
Shum Tin Yu (Eric): art.py, battle.py, data.py, explore.py, helpbook.py, state.py, texts.py, victory.py, maps, additional debugging, README, recording video footage
Pivet Gabriel Jean: main.py, menus.py, screens.py, video editing
Yan Jiayu (Joe): fighters.py, maze_system.py, maps
Guo Fu Ze (Phillip): battlescreen.py, shop.py
