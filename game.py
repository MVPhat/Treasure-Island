import numpy as np
import random
from const import *


class Game:
    def __init__(self, map, width, height, reveal_turn, free_turn, num_of_regions, Tx, Ty):
        # agents' constants
        self.LONG_MOVES = [(0, 3), (3, 0), (0, -3), (-3, 0),
                           (0, 4), (4, 0), (0, -4), (-4, 0)]
        self.SHORT_MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0),
                            (0, 2), (2, 0), (0, -2), (-2, 0)]
        self.PIRATE_MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
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
        self.REGION_MASK = self.get_region_mask(self.REGION_LIST)
        self.REGION_WITH_MOUNTAIN_LIST = self.get_region_list(
            height, width, with_mountain=True)
        self.REGION_WITH_MOUNTAIN_MASK = self.get_region_mask(
            self.REGION_WITH_MOUNTAIN_LIST)
        self.NEIGHBOUR_REGIONS = self.neighbour_region()
        self.SEA_MASK = self.MAP['region'] == 0
        self.REVEAL_TURN = reveal_turn
        self.FREE_TURN = free_turn
        self.TX = Tx
        self.TY = Ty
        self.TREASURE = (Tx, Ty)
        self.PRISION_LIST = self.get_prison_list(height, width)
        self.NUM_OF_PRISON = len(self.PRISION_LIST)
        self.BAD_FOR_AGENT = self.get_bad_list(height, width)
        self.BAD_FOR_PIRATE = self.BAD_FOR_AGENT
        self.CACHE = {}
        self.HINT_WEIGHTS = [
            NOT_IMPLEMENTED,  # doesnt exist
            NORMAL_WEIGHT,  # 1
            NORMAL_WEIGHT,  # 2
            NORMAL_WEIGHT,  # 3
            NORMAL_WEIGHT,  # 4
            NORMAL_WEIGHT,  # 5
            NORMAL_WEIGHT,  # 6
            RARE_WEIGHT,   # 7
            NORMAL_WEIGHT,  # 8
            NORMAL_WEIGHT,  # 9
            NORMAL_WEIGHT,  # 10
            NORMAL_WEIGHT,  # 11
            RARE_WEIGHT,   # 12
            NORMAL_WEIGHT,  # 13
            RARE_WEIGHT,   # 14
            NORMAL_WEIGHT,  # 15
            VERR_RARE_WEIGHT  # 16
        ]

    def get_region_mask(self, region_list):
        result = {}
        for region in region_list:
            mask = (self.MAP['region'] == region)
            result[region] = mask
        return result

    def get_bad_list(self, height, width):
        result = np.zeros((height, width), dtype=np.bool_)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                result[i][j] = not self.good_for_agent(i, j)
        return result

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
        return self.valid(x, y) and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def good_for_treasure(self, x, y):
        return self.valid(x, y) and self.MAP['entity'][x][y] != PRISON and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def good_for_pirate(self, x, y):
        return self.valid(x, y) and self.MAP['entity'][x][y] != MOUNTAIN and self.MAP['region'][x][y] != SEA

    def random_agent_position(self, map):
        while True:
            Ax = random.randrange(0, self.HEIGHT)
            Ay = random.randrange(0, self.WIDTH)
            if self.good_for_treasure(Ax, Ay) and (not (Ax, Ay) == self.TREASURE):
                return (Ax, Ay)

    def neighbour_region(self):
        result = {}
        for region_1 in self.REGION_LIST:
            for region_2 in self.REGION_LIST:
                if region_1 >= region_2:
                    continue
                tmp_1 = self.REGION_MASK[region_1].copy()
                tmp_1[:-1, :] |= self.REGION_MASK[region_1][1:, :]
                tmp_1[1:, :] |= self.REGION_MASK[region_1][:-1, :]
                tmp_1[:, :-1] |= self.REGION_MASK[region_1][:, 1:]
                tmp_1[:, 1:] |= self.REGION_MASK[region_1][:, :-1]
                tmp_1 ^= self.REGION_MASK[region_1]
                tmp_1 &= self.REGION_MASK[region_2]
                tmp_2 = self.REGION_MASK[region_2].copy()
                tmp_2[:-1, :] |= self.REGION_MASK[region_2][1:, :]
                tmp_2[1:, :] |= self.REGION_MASK[region_2][:-1, :]
                tmp_2[:, :-1] |= self.REGION_MASK[region_2][:, 1:]
                tmp_2[:, 1:] |= self.REGION_MASK[region_2][:, :-1]
                tmp_2 ^= self.REGION_MASK[region_2]
                tmp_2 &= self.REGION_MASK[region_1]
                tmp = tmp_1 | tmp_2
                if tmp.any():
                    result[(region_1, region_2)] = tmp
        return result
