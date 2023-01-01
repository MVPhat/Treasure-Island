import numpy as np
import random
from const import *

from init_2 import *

class Hint:
    def __init__(self, hint_number, id):
        self.height = game.HEIGHT
        self.width = game.WIDTH
        self.map = {}
        self.map['mark'] = np.zeros((self.height, self.width), dtype=np.bool_)
        self.map['contains'] = np.zeros((self.height, self.width), dtype=np.bool_)
        self.hint = hint_number
        self.id = id
        self.log = ""
        if self.hint == 1:
            self.hint_1()
        elif self.hint == 2:
            self.hint_2()
        elif self.hint == 3:
            self.hint_3()
        elif self.hint == 4:
            self.hint_4()
        elif self.hint == 5:
            self.hint_5()
        elif self.hint == 6:
            self.hint_6()
        elif self.hint == 7:
            self.hint_7()
        elif self.hint == 8:
            self.hint_8()
        elif self.hint == 9:
            self.hint_9()
        elif self.hint == 10:
            self.hint_10()
        elif self.hint == 11:
            self.hint_11()
        elif self.hint == 12:
            self.hint_12()
        elif self.hint == 13:
            self.hint_13()
        elif self.hint == 14:
            self.hint_14()
        elif self.hint == 15:
            self.hint_15()
        elif self.hint == 16:
            self.hint_16()
        self.make_contains_map()

    def make_contains_map(self):
        if self.hint in NEGATIVE_HINTS:
            self.map['contains'] = ~self.map['mark']
        else:
            self.map['contains'] = self.map['mark']
        
    def hint_1(self):
        # A list of random tiles that doesn't contain the treasure (1 to 12).
        max_num = min(12, np.sum(agent.map))
        num = random.randint(1, max_num)
        res = []
        
        for coord in np.argwhere(agent.map == True):
            res.append(coord)
        
        random.shuffle(res)

        res = res[:num]

        self.log = str(res)

    def hint_2(self):
        # 2-5 regions that 1 of them has the treasure.
        min_num = 2
        max_num = min(5, len(game.REGION_LIST))
        regions = random.sample(game.REGION_LIST, random.randint(min_num, max_num))
        self.log = str(regions)

        for region in regions:
            self.map['mark'] |= game.REGION_MASK[region]
    
    def hint_3(self):
        # 1-3 regions that do not contain the treasure.
        min_num = 1
        max_num = min(3, len(game.REGION_LIST))
        regions = random.sample(game.REGION_LIST, random.randint(min_num, max_num))
        self.log = str(regions)

        for region in regions:
            self.map['mark'] |= game.REGION_MASK[region]
    
    def hint_4(self):
        # A large rectangle area that has the treasure
        x1 = random.randrange(0, self.height // 2)
        x2 = random.randrange(x1 + self.height // 2, self.height)
        y1 = random.randrange(0, self.width // 2)
        y2 = random.randrange(y1 + self.width // 2, self.width)
        
        self.log = f"row1 = {x1}, row2 = {x2}, col1 = {y1}, col2 = {y2}"

        self.map['mark'][x1: x2, y1: y2] = 1

    def hint_5(self):
        # A small rectangle area that doesn't has the treasure.
        while 1:
            x1, x2 = sorted(random.sample(range(self.height), k=2))
            y1, y2 = sorted(random.sample(range(self.width), k=2))
            if (x2 - x1) * 2 <= self.height and (y2 - y1) * 2 <= self.width:
                break
        
        self.log = f"row1 = {x1}, row2 = {x2}, col1 = {y1}, col2 = {y2}"

        self.map['mark'][x1: x2, y1: y2] = 1

    def hint_6(self):
        # He tells you that you are the nearest person to the treasure (between you and the prison he is staying)
        cost = agent.agent_bfs(agent.x, agent.y)

        cost = (cost + 1) // 2

        self.map['mark'] = (cost - pirate.map) < 0
    
    def hint_7(self):
        # A column and/or a row that contain the treasure (rare)
        # 0: row 
        # 1: col
        # 2: both
        row_col = random.randint(0, 2)  
        row = random.randrange(0, self.height)
        col = random.randrange(0, self.width)
        if row_col == 0:
            self.log = f"row: {row}"
            self.map['mark'][row, :] = 1
        elif row_col == 1:
            self.log = f"column: {col}"
            self.map['mark'][:, col] = 1
        else:
            self.log = f"row: {row}, column: {col}"
            self.map['mark'][row, :] = 1
            self.map['mark'][:, col] = 1
    
    def hint_8(self):
        # A column and/or a row that do not contain the treasure.
        row_col = random.randint(0, 2)
        row = random.randrange(0, self.height)
        col = random.randrange(0, self.width)
        if row_col == 0:
            self.log = f"row: {row}"
            self.map['mark'][row, :] = 1
        elif row_col == 1:
            self.log = f"column: {col}"
            self.map['mark'][:, col] = 1
        else:
            self.log = f"row: {row}, column: {col}"
            self.map['mark'][row, :] = 1
            self.map['mark'][:, col] = 1

    def hint_9(self):
        # 2 regions that the treasure is somewhere in their boundary
        region_1, region_2 = random.choice(list(game.NEIGHBOUR_REGIONS.keys()))
        
        self.log = f"{region_1}, {region_2}"

        self.map['mark'] |= game.NEIGHBOUR_REGIONS[(region_1, region_2)]

    def hint_10(self):
        # The treasure is somewhere in a boundary of 2 regions

        self.log = "ok"

        for mask in game.NEIGHBOUR_REGIONS.values():
            self.map['mark'] |= mask

    def hint_11(self):
        # The treasure is somewhere in an area bounded by 2-3 tiles from sea.

        self.log = "ok"

        tiles = random.randint(2, 3)
        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] != SEA:
                    u = max(0, i - tiles)
                    d = min(self.height, i + tiles + 1)
                    l = max(0, j - tiles)
                    r = min(self.width, j + tiles + 1)
                    self.map['mark'][i][j] = game.SEA_MASK[u:d, j].any() or game.SEA_MASK[i, l:r].any()

        
    def hint_12(self):
        # A half of the map without treasure (rare)
        choices = random.randint(1, 4)
        if choices == 1:
            self.log = "north"
            half = self.height // 2
            self.map['mark'][0: half, :] = 1
        if choices == 2:
            self.log = "south"
            half = self.height // 2
            self.map['mark'][half: self.height, :] = 1
        if choices == 3:
            self.log = "west"
            half = self.width // 2
            self.map['mark'][:, 0: half] = 1
        if choices == 4:
            self.log = "east"
            half = self.width // 2
            self.map['mark'][:, half: self.width] = 1
    
    def hint_13(self):
        # From the center of the map/from the prison that he's staying, he tells
        # you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW)
        # (The shape of area when the hints are either W, E, N or S is triangle).
        if not pirate.reveal:
            source = "center"
        else:
            source = random.choice(["center", "prison"])

        if source == "center":
            x, y = self.height // 2, self.width // 2
        else:
            x, y = pirate.prison

        direction = random.choice(["W", "E", "N", "S", "SE", "SW", "NE", "NW"])
        self.log = f"{source}, {direction}"
        # W E N S
        if len(direction) == 1:
            if direction == "N":
                dx, dy, dcntx, dcnty = -1, 0, 0, 1
            elif direction == "S":
                dx, dy, dcntx, dcnty = 1, 0, 0, 1
            elif direction == "W":
                dx, dy, dcntx, dcnty = 0, -1, 1, 0
            elif direction == "E":
                dx, dy, dcntx, dcnty = 0, 1, 1, 0
            cntx = 0
            cnty = 0
            while game.valid(x, y):
                u, v = x, y
                lmao_u = max(0, x - cntx)
                lmao_d = min(self.height, x + cntx + 1)
                lmao_l = max(0, y - cnty)
                lmao_r = min(self.width, y + cnty + 1)
                self.map['mark'][lmao_u:lmao_d, lmao_l:lmao_r] = 1
                x += dx
                y += dy
                cntx += dcntx
                cnty += dcnty
        # SE SW NE NW
        else:
            if direction == "SE":
                self.map['mark'][x: self.height, y: self.width] = 1
            elif direction == "SW":
                self.map['mark'][x: self.height, 0: y] = 1
            elif direction == "NE":
                self.map['mark'][0: x, y: self.width] = 1
            elif direction == "NW":
                self.map['mark'][0: x, 0: y] = 1
    
    def hint_14(self):
        # 2 squares that are different in size, the small one is placed inside the
        # bigger one, the treasure is somewhere inside the gap between 2
        # squares. (rare)
        x1 = random.randrange(0, self.height // 2)
        x2 = random.randrange(x1 + self.height // 2, self.height)
        y1 = random.randrange(0, self.width // 2)
        y2 = random.randrange(y1 + self.width // 2, self.width)
        xx1, xx2 = sorted(random.sample(range(x1, x2), k=2))
        yy1, yy2 = sorted(random.sample(range(y1, y2), k=2))

        self.log = f"big rec = ({x1}, {x2}, {y1}, {y2}), small rec = ({xx1}, {xx2}, {yy1}, {yy2})"

        self.map['mark'][x1: x2, y1: y2] = 1
        self.map['mark'][xx1: xx2, yy1: yy2] = 0


    def hint_15(self):
        # The treasure is in a region that has mountain
        self.log = "ok"

        region = random.choice(game.REGION_WITH_MOUNTAIN_LIST)

        self.map['mark'] |= game.REGION_WITH_MOUNTAIN_MASK[region]

    def hint_16(self):
        # A list of random tiles that contains the treasure (half of the map size) (very rare).
        res = []

        for i in range(self.height):
            for j in range(self.width):
                res.append((i, j))
        
        random.shuffle(res)

        res = res[:self.height * self.width // 2]

        self.log = str(res)

        for i, j in res:
            self.map['mark'][i][j] = 1

    def truthness(self):
        return self.map['contains'][game.TREASURE[0]][game.TREASURE[1]]

