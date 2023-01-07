from game import Game
from const import *
import numpy as np


def readInputFile(filename):
    with open(filename, "r") as f:
        # - The first line contains 2 numbers to represent the size of the map (𝑾 and 𝑯).
        width, height = f.readline().split(" ")
        width, height = int(width), int(height)
        # - The second line is the turn number that the pirate reveals the prison (𝒓).
        reveal_turn = int(f.readline())
        # - The third line is the turn number that the pirate is free and start running to the treasure. (𝒇).
        free_turn = int(f.readline())
        # - The fourth line is the number of regions on the map (including the sea) (𝑹).
        num_of_regions = int(f.readline())
        # - The fifth line contains 2 numbers to represent the treasure position (𝑻𝒙, 𝑻𝒚)
        Tx, Ty = f.readline().split(" ")
        Tx, Ty = int(Tx), int(Ty)
        # - The next H lines are the H rows of a map
        map = []
        output = {}
        output['region'] = np.zeros((height, width), dtype=int)
        output['entity'] = np.zeros((height, width), dtype=int)
        for i in range(height):
            map.append(f.readline().split(";"))
        for i in range(height):
            for j in range(width):
                map[i][j] = map[i][j].strip()
                output['region'][i][j] = int(map[i][j][0])
                if len(map[i][j]) == 1:
                    continue
                if map[i][j][1] == 'M':
                    output['entity'][i][j] = MOUNTAIN
                elif map[i][j][1] == 'P':
                    output['entity'][i][j] = PRISON
                elif map[i][j][1] == 'T':
                    output['entity'][i][j] = TREASURE
    return (output, width, height, reveal_turn, free_turn, num_of_regions, Tx, Ty)


def save_file_log(log):
    f = open(TEST_CASE, 'w')
    for line in log:
        f.write(line)
    f.close()


EXAMPLE_FILE = "MAP_0.txt"
TEST_CASE = "LOG_0.txt"

map, width, height, reveal_turn, free_turn, num_of_regions, Tx, Ty = readInputFile(
    EXAMPLE_FILE)

game = Game(map=map, width=width, height=height, reveal_turn=reveal_turn,
            free_turn=free_turn, num_of_regions=num_of_regions, Tx=Tx, Ty=Ty)
