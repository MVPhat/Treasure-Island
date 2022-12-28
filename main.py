from visualization import Visualization
import numpy as np
from pirate import *

EXAMPLE_FILE = "MAP_0.txt"


def readInputFile(filename):
    with open(filename, "r") as f:
        # - The first line contains 2 numbers to represent the size of the map (𝑾 and 𝑯).
        width, height = f.readline().split(" ")
        # - The second line is the turn number that the pirate reveals the prison (𝒓).
        reveals = f.readline().split(" ")
        # - The third line is the turn number that the pirate is free and start running to the
        # treasure. (𝒇).
        free = f.readline().split(" ")
        # - The fourth line is the number of regions on the map (including the sea) (𝑹).
        regions = f.readline().split(" ")
        # - The fifth line contains 2 numbers to represent the treasure position (𝑻𝒙, 𝑻𝒚)
        Tx, Ty = f.readline().split(" ")
        # - The next H lines are the H rows of a map
        map = []
        for i in range(int(height)):
            map.append(f.readline().split(";"))
        for i in range(int(height)):
            for j in range(int(width)):
                map[i][j] = (int(map[i][j][0]), ' ' if map[i][j][1] ==
                             "\n" or map[i][j][1] == " " else map[i][j][1], False, 1)
    map = np.array(map, dtype=[
                   ('region', np.short), ('type', 'U4'), ('mark', np.bool_), ('ratio', np.short)])
    return (int(width), int(height)), reveals, free, regions, (Tx, Ty), map


(width, height), reveal, free, region, (Tx, Ty), map = readInputFile(EXAMPLE_FILE)


HINTS_NAME = [
    #(1, "A list of random tiles that doesn't contain the treasure (1 to 12)"),
    # (2, "2-5 regions that 1 of them has the treasure"),
    # (3, "1-3 regions that do not contain the treasure"),
    # (4, "A large rectangle area that has the treasure"),
    # (5, "A small rectangle area that doesn't has the treasure"),
    # (6, "He tells you that you are the nearest person to the treasure (between you and the prison he is staying)"),
    # (7, "A column and/or a row that contain the treasure (rare)"),
    # (8, "A column and/or a row that do not contain the treasure"),
    # (9, "2 regions that the treasure is somewhere in their boundary"),
    # (10, 'The treasure is somewhere in a boundary of 2 regions'),
    # (11, 'The treasure is somewhere in an area bounded by 2-3 tiles from sea'),
    # (12, 'A half of the map without treasure (rare)'),
    (13, 'From the center of the map/from the prison that he\'s staying, he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW) (The shape of area when the hints are either W, E, N or S is triangle)'),
    # (14, '2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares (rare)'),
    # (15, 'The treasure is in a region that has mountain'),
]


#random 1 prison
prison_list = list(zip(*np.argwhere(map['type'] == 'P')))
ranidx = random.randint(0, len(prison_list[0]) - 1)
map[prison_list[0][ranidx]][prison_list[1][ranidx]]['type'] += 'p'

#random agent
while True:
    agent = (random.randint(1, width - 2), random.randint(1, height - 2))
    if (map[agent[0]][agent[1]]['type'] != 'P' and map[agent[0]][agent[1]]['type'] != 'M' and
        map[agent[0]][agent[1]]['region'] != 0):
        map[agent[0]][agent[1]]['type'] += 'A'
        break


for i in range(len(HINTS_NAME)):
    num, name = HINTS_NAME[i]
    print(name)
    visual = Visualization(width, height, Tx, Ty, map)

    visual.visualize(f"h{num}")

    visual.verify(f"h{num}")

    visual.clear_mark()

    map = visual.map

