import numpy as np
import random
from const import *


class Game:
    def __init__(self, map, width, height, reveal_turn, free_turn, num_of_regions, Tx, Ty):
        # agents' constants
        self.LONG_MOVES = [[0, 3], [3, 0], [0, -3],
                           [-3, 0], [0, 4], [4, 0], [0, -4], [-4, 0]]
        self.SHORT_MOVES = [[0, 1], [1, 0], [0, -1],
                            [-1, 0], [0, 2], [2, 0], [0, -2], [-2, 0]]
        self.PIRATE_MOVES = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        self.ACTIONS_IN_TURN = 2

        # game's constants
        self.HEIGHT = height
        self.WIDTH = width
        self.MAP = {}
        self.MAP['region'] = np.copy(map['region'])
        self.MAP['entity'] = np.copy(map['entity'])
        self.NUM_OF_REGION = num_of_regions
        self.REGION_LIST = self.get_region_list(
            height, width, with_mountain=False)
        self.REGION_WITH_MOUNTAIN_LIST = self.get_region_list(
            height, width, with_mountain=True)
        self.REVEAL_TURN = reveal_turn
        self.FREE_TURN = free_turn
        self.TX = Tx
        self.TY = Ty
        self.TREASURE = (Tx, Ty)
        self.PRISION_LIST = self.get_prison_list(height, width)
        self.NUM_OF_PRISON = len(self.PRISION_LIST)

    def get_region_list(self, height, width, with_mountain):
        regions = set()
        for i in range(height):
            for j in range(width):
                if self.MAP['region'][i][j] != SEA and (not with_mountain or self.MAP['entity'][i][j] == MOUNTAIN):
                    regions.add(self.MAP['region'][i][j])
        return list(regions)

    def get_prison_list(self, height, width):
        prisons = []
        for i in range(height):
            for j in range(width):
                if self.MAP['entity'][i][j] == PRISON:
                    prisons.append((i, j))
        return prisons

    def valid(self, x, y):
        return x >= 0 and x < self.HEIGHT and y >= 0 and y < self.WIDTH

    def good_for_agent(self, x, y):
        """
        If the position is valid, and it's not a mountain or sea, then it's good for the agent.

        :param x: the x coordinate of the cell
        :param y: the y coordinate of the cell
        :return: A list of all the possible actions that can be taken from the current state.
        """
        return self.valid(x, y) and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def good_for_treasure(self, x, y):
        return self.valid(x, y) and self.MAP['entity'][x][y] != PRISON and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def good_for_pirate(self, x, y):
        return self.valid(x, y) and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def random_agent_position(self, map):
        while True:
            Ax = random.randrange(0, self.HEIGHT)
            Ay = random.randrange(0, self.WIDTH)
            if self.good_for_treasure(Ax, Ay):
                return (Ax, Ay)
