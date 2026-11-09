# AI Use

Generative AI used: Yes

## Entry 01

Member and date: Shum Tin Yu (Eric), Oct 12

Tool and model/version, where available: Claude Sonnet 5.5

Purpose: Naming abilities, moves, monsters for the game

Relevant prompts and outputs used, or retained transcript location:

Prompts (in order):
- I am making a video game. Come up with the name of an ability and a move that regenerates health for a knight
- Come up with the name of an ability that increases damage dealt the more health that is lost
- Come up with the name of an ability that reduces damage taken
- Come up with the name of an ability that increases mana regeneration, for a character that is a healer
- Come up with the name of a move that deals damage based on defense. Keep in mind that this is used by a defensive character
- Come up with the name of a dragon, a titan, and a necromancer

Outputs used:
- Vigor (ability), Second Wind (move)
- Bloodlust
- Plating
- Grace
- Bulwark Blow
- Infernus (dragon), Kronos (titan), Morvain (necromancer)
  
Files/materials affected: N/A, as we are still in a planning phase

What we kept, changed or rejected: We decided to adopt the names

How we checked it; tests and corrections: N/A

## Entry 02

Member and date: Shum Tin Yu (Eric), Oct 27

Tool and model/version, where available: Claude Sonnet 5.5

Purpose: Creating ASCII art for heroes

Relevant prompts and outputs used, or retained transcript location:

Prompts (in order):
- Create ASCII art for the heroes. Keep the hero below 20x7 (width x height).

Outputs used:
- The ASCII sprites for the heroes
  
Files/materials affected: art.py

What we kept, changed or rejected: We used the ASCII sprites, but made minor modifications manually

How we checked it; tests and corrections: We looked through the ASCII sprites and inspected whether it looks good or not

## Entry 03

Member and date: Shum Tin Yu (Eric), Nov 8

Tool and model/version, where available: ChatGPT (GPT-6.1 Sol)

Purpose: Final fixes and adjustments to the game

Relevant prompts and outputs used, or retained transcript location:

Prompts (in order):
- What is still missing for the game to function? Are there still any bugs, inconsistencies, and redundancies?
- The title block still looks weird, can you fix it?
- What other changes can I implement to make the game a little better?

Outputs used:
- Added a few minor parts of code in order for some functions to work properly, fixed many bugs/oversights in the code AI pointed out, removed multiple redundancies and unused parts of code AI pointed out
- Fixed the title block in the title screen
- Implemented a suggestion where battle text output printed the text letter by letter in short intervals
  
Files/materials affected: battle.py, battlescreen.py, data.py, explore.py, fighters.py, main.py, maze_system.py, menus.py, screen_render.py, shop.py, texts.py

What we kept, changed or rejected: There was a large amount of problems. Using the fixes AI suggested, we first inspected the fixes and determined whether the fix was valid. Then we fixed our code to make sure the code does not have any errors. There were a few changes the AI suggested but we did not implement, but we did choose to implement the battle text output suggestions. For the battle text output, we adjusted the text speed between different values and determined that 0.02s was the sweet spot.

How we checked it; tests and corrections: We ran the game and inspected whether the issues still persisted. While most errors were fixed as expected, one that persisted during manual testing was the title block art which still looked weird, so we followed up with a prompt to fix that error. For the battle text output we tested the different values between 0.01-0.05s per letter at intervals of 0.01, and determined that 0.02s was good.

## Entry 04

Member and date: Shum Tin Yu (Eric), Nov 8

Tool and model/version, where available: ChatGPT (GPT-6.1 Sol)

Purpose: Creating README.md instructions for Windows users (I do not own a Windows device)

Relevant prompts and outputs used, or retained transcript location:

Prompts (in order):
- Update README.md to update how to run the game on Windows

Outputs used:
- The method to run the game on a Windows device
- AI also added an additional instruction to install Python, so we kept that too
  
Files/materials affected: README.md

What we kept, changed or rejected: We liked the formatting for the Windows instructions, so we kept it and also modified our formatting for the Mac instructions.

How we checked it; tests and corrections: By reading and checking if the wording and instructions were correct. Made minimal changes to the wording.
