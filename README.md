# Project2_AI

# Generate input map

### Save file name

Move to the cell which has function `save_map()`
Change the name input file in `with open("MAP_2.txt", "w")` if you want
THEN,
Run the file `gen_input.ipynb` to generate the map game.

# How to run this project

### Load the map

In `main.py`, choose your map you want to load and log file want to save in
`EXAMPLE_FILE = "MAP_1.txt"`
`TEST_CASE = "LOG_1.txt"`

### Run

Use python 3 to run this project in terminal: `py main.py`

### After finished the game

We save the log game in `LOG_x.txt`, you can see all process of the game in this file.

# Can not run the project

May be your computer does not install the packages we need in the project, so you can use this command line
`pip install -r ./requirements.txt` or find the packages on Google if this command line can not solve the problems.

# Save image

We have saved the image visualization for each turn (give the hint/verify the hint)
You can check it at `./Project2_AI/eps/` or `./Project2_AI/png`

# About the visualization

### Visualization console does not fit your screen or can not see whole the map

Move to file `visualization.py`

In function `def __init__(self, width, height, map)` or use `ctrl + F` and type `self.FONT_SIZE`

Move to `self.FONT_SIZE = 14 if width == 16 else 7` (text size)
You can change the number `14` if size is 16 and change the number `7` if the size is larger

and `self.SIZE = 40 if width == 16 else 20` (block size)
You can change the number `40` if size is 16 and change the number `20` if the size is larger

### Changing the speed of the visualization

Move to file `visualization.py`

In function `def __init__(self, width, height, map)` or use `ctrl + F` and type `turtle.speed`

type of speed:
`fastest`
`fast`
`normal`
`slow`
`slowest`

For example: `turtle.speed('fastest')`
