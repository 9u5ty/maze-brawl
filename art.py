#Function to help with creating ASCII art, allowing the code to be outputted exactly as I designed here split over multiple lines
def lines(block):
    lines = block.strip("\n").split("\n") 
    return lines

#Title Block
title = lines(r"""
     __  __    _     __________
    |  \/  |  / \   |__  / ____|
    | |\/| | / _ \    / /|  _|
    | |  | |/ ___ \  / /_| |___
    |_|  |_/_/   \_\/____|_____|
 ____  ____      ___        ___
| __ )|  _ \    / \ \      / / |
|  _ \| |_) |  / _ \ \ /\ / /| |
| |_) |  _ <  / ___ \ V  V / | |___
|____/|_| \_\/_/   \_\_/\_/  |_____|
""")

#Heroes
hero_art = {
    "kyle": lines(r"""
    .--.     |
   | oo |    |
  /|-==-|\  -+-
 / |[##]| \  |
   |    |
   |_  _|
   (_)(_)
"""),
    "bryce": lines(r"""
    \  /
   ,~||~.   ,-.
  ( >_< )  / /
   \\||//  / /
  --[XX]--'/
    |  |
   _/  \_
"""),
    "george": lines(r"""
    .--.
   |[oo]|   |
  /|====|\  |
 |#|    |#| |
 |#| || |#|-+-
  \|_||_|/
   (_)(_)
"""),
    "clara": lines(r"""
           *
    ,--.   |
   ( ^^ )  |
  /|----|\-+-
 / | ++ | \|
   |____|  |
   /_/\_\
"""),
}

#Others
trophy = lines(r"""
   .-----------.
.-.|           |.-.
| ||           || |
'-.|           |.-'
   \           /
    '.       .'
      '--.--'
         |
       __|__
      [_____]
""")

grave = lines(r"""
       _.---._
     .'  RIP  '.
     |   +++    |
     |          |
  ___|__________|___
""")