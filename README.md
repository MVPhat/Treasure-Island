# Project 2 AI - TREASURE ISLAND - GUIDE


# IN FILE `gen_input.ipynb` # <-----------------------
# Generate input map
## Set up 'SIZE'
Move to the next last cell which has function `save_map`
Input the size of map (line `n = X`). Recommended for square matrix because i've not splited 2 size becoming to width and height.

## Set up 'REGIONS'
Move to the cell which has function `gen_map` 
Input the number of regions (line `regions = X`). Recommended for less than 10. Bigger than 10 is ok but some cases it will not fill all regions in the map.

## Save file name
Change the file name in `with open("MAP_X.txt", "w")` if you want
THEN,
Click `Run all` to run the file `gen_input.ipynb`.
If function `save_map` occurs error: both agent and pirate can not reach to Treasure on any tiles in the map (map is surrounded by mountain, sea,...).


# Run game # <-----------------------
# IN FILE `init.py`
## Load map
Choose file map and log file want to load and save.
For example:
`EXAMPLE_FILE = "MAP_1.txt"`
`TEST_CASE = "LOG_1.txt"`
PLEASE TURN OFF VISUALIZATION FOR MAP 96x96 or larger (scroll down to see how to turn off).

## Run
Use python 3 to run this project in terminal: `py main.py`

## After finished the game
We save the log game in file `LOG_x.txt` you have inputed above, you can see all process of the game in this file.

## CAN NOT RUN the project
May be your computer does not install the packages we need in the project, so you can use this command line
`pip install -r ./requirements.txt` or find the packages on Google if this command line can not solve the problems.

## Save image
We have saved the image visualization for each turn (give the hint/verify the hint)
You can check it at `./Project2_AI/eps/` or `./Project2_AI/png`


# Visualization # <-----------------------
# IN FILE `visualization.py`
## Visualization console does not fit your screen or can not see whole the map
In function `def __init__(self, width, height, map)` or use `ctrl + F` and type `self.FONT_SIZE`

Move to `self.FONT_SIZE = 14 if width == 16 else 7` (text size)
You can change the number `14` if size is 16 and change the number `7` if the size is larger

and `self.SIZE = 40 if width == 16 else 20` (block size)
You can change the number `40` if size is 16 and change the number `20` if the size is larger

## Speed of the visualization
In function `def __init__(self, width, height, map)` or use `ctrl + F` and type `turtle.speed`

Type of speed:
`fastest`
`fast`
`normal`
`slow`
`slowest`

For example: `turtle.speed('fastest')`

## IF YOU DO NOT VISUALIZE FOR BIG MAP
# IN FILE `main.py`
use `CTRL + F` to and type the keyword: `visualiz` and comment all lines which contain this keyword.
