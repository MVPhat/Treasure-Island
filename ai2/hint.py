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
        self.map['contains'] = np.zeros(
            (self.height, self.width), dtype=np.bool_)
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

    """
    It sets the `contains` map to the `mark` map, unless the hint is a negative hint, in which case it
    sets the `contains` map to the opposite of the `mark` map
    """

    def make_contains_map(self):
        negate = self.hint in NEGATIVE_HINTS
        for i in range(self.height):
            for j in range(self.width):
                if negate:
                    self.map['contains'][i][j] = not self.map['mark'][i][j]
                else:
                    self.map['contains'][i][j] = self.map['mark'][i][j]

    def hint_1(self):
        """
        It randomly selects a number of tiles (1 to 12) and marks them as "hinted"
        """
        # A list of random tiles that doesn't contain the treasure (1 to 12).
        num = random.randint(1, 12)
        cnt = 0
        res = []

        while cnt < num:
            row = random.randrange(0, self.height)
            col = random.randrange(0, self.width)
            region = game.MAP['region'][row][col]
            entity = game.MAP['entity'][row][col]
            if region == SEA or entity == MOUNTAIN or entity == PRISON:
                continue
            self.map['mark'][row][col] = 1
            res.append((row, col))
            cnt += 1

        self.log = str(res)

    def hint_2(self):
        """
        The function randomly selects 2-5 regions from the game.REGION_LIST, and then marks all the cells
        in those regions
        """
        # 2-5 regions that 1 of them has the treasure.
        min_num = 2
        max_num = min(5, len(game.REGION_LIST))
        region = set(random.sample(game.REGION_LIST,
                     random.randint(min_num, max_num)))

        self.log = str(list(region))

        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] in region:
                    self.map['mark'][i][j] = 1

    def hint_3(self):
        """
        It randomly selects 1-3 regions that do not contain the treasure, and marks them on the map
        """
        # 1-3 regions that do not contain the treasure.
        min_num = 1
        max_num = min(3, len(game.REGION_LIST))
        region = set(random.sample(game.REGION_LIST,
                     random.randint(min_num, max_num)))

        self.log = str(list(region))

        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] in region:
                    self.map['mark'][i][j] = 1

    def hint_4(self):
        """
        > The function creates a large rectangle area that has the treasure
        """
        # A large rectangle area that has the treasure
        x1 = random.randrange(0, self.height // 2)
        x2 = random.randrange(self.height // 2, self.height)
        y1 = random.randrange(0, self.width // 2)
        y2 = random.randrange(self.width // 2, self.width)

        self.log = f"row1 = {x1}, row2 = {x2}, col1 = {y1}, col2 = {y2}"

        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.map['mark'][i][j] = 1

    def hint_5(self):
        """
        It marks a small rectangle area that doesn't has the treasure.
        """
        # A small rectangle area that doesn't has the treasure.
        while 1:
            x1, x2 = sorted(random.sample(range(self.height), k=2))
            y1, y2 = sorted(random.sample(range(self.width), k=2))
            if (x2 - x1) <= self.height // 2 and (y2 - y1) <= self.width // 2:
                break

        self.log = f"row1 = {x1}, row2 = {x2}, col1 = {y1}, col2 = {y2}"

        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                self.map['mark'][i][j] = 1

    def hint_6(self):
        """
        It finds the shortest path from the agent to the treasure, and marks all the cells that are closer
        to the agent than the treasure
        """
        # He tells you that you are the nearest person to the treasure (between you and the prison he is staying)
        cost = np.zeros((self.height, self.width))
        queue = []
        queue.append(agent.get_position())
        i = 0

        self.log = "ok"

        while i < len(queue):
            x, y = queue[i]
            for move in game.SHORT_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if (u, v) != agent.get_position() and agent.can_move(x, y, dx, dy) and cost[u][v] == 0:
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            for move in game.LONG_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if (u, v) != agent.get_position() and agent.can_move(x, y, dx, dy) and cost[u][v] == 0:
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            i += 1
        for i in range(self.height):
            for j in range(self.width):
                if pirate.map[i][j] > cost[i][j]:
                    self.map['mark'][i][j] = 1

    def hint_7(self):
        """
        > The function randomly chooses a row, column, or both, and marks all the cells in that
        row/column as containing the treasure
        """
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
        """
        It randomly chooses a row, column, or both, and marks them as not containing the treasure
        """
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
        """
        > If the treasure is in region 1, then it must be in the boundary of region 1. If the treasure is
        in region 2, then it must be in the boundary of region 2
        """
        # 2 regions that the treasure is somewhere in their boundary
        region_1, region_2 = random.sample(game.REGION_LIST, k=2)

        self.log = f"{region_1}, {region_2}"

        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] == region_1:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            u, v = i + di, j + dj
                            if game.valid(u, v) and game.MAP['region'][u][v] == region_2:
                                self.map['mark'][i][j] = 1
                                break
                        if self.map['mark'][i][j]:
                            break
                if self.map['mark'][i][j]:
                    continue
                if game.MAP['region'][i][j] == region_2:
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            u, v = i + di, j + dj
                            if game.valid(u, v) and game.MAP['region'][u][v] == region_1:
                                self.map['mark'][i][j] = 1
                                break
                        if self.map['mark'][i][j]:
                            break

    def hint_10(self):
        """
        It marks the boundary of the regions.
        """
        # The treasure is somewhere in a boundary of 2 regions

        self.log = "ok"

        for i in range(self.height):
            for j in range(self.width):
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        u, v = i + di, j + dj
                        if game.valid(u, v) and game.MAP['region'][u][v] != SEA and game.MAP['region'][i][j] != SEA and game.MAP['region'][u][v] != game.MAP['region'][i][j]:
                            self.map['mark'][i][j] = 1
                            break
                    if self.map['mark'][i][j]:
                        break

    def hint_11(self):
        """
        "The treasure is somewhere in an area bounded by 2-3 tiles from sea."

        The function is a bit long, but it's not too complicated. It first picks a random number of
        tiles, between 2 and 3. Then it loops through all the tiles on the map, and if the tile is not
        sea, it checks if there are any sea tiles within the number of tiles picked earlier. If there
        are, it marks the tile
        """
        # The treasure is somewhere in an area bounded by 2-3 tiles from sea.

        self.log = "ok"

        tiles = random.randint(2, 3)
        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] != SEA:
                    for di in range(-tiles, tiles + 1):
                        sus = tiles - abs(di)
                        for dj in range(-sus, sus + 1):
                            u, v = i + di, j + dj
                            if game.valid(u, v) and game.MAP['region'][u][v] == SEA:
                                self.map['mark'][i][j] = 1
                                break
                        if self.map['mark'][i][j]:
                            break

    """
    It randomly chooses a direction and marks the half of the map in that direction as visited
    """

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
        """
        > The pirate tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW) (The shape
        of area when the hints are either W, E, N or S is triangle)
        """
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
                for du in range(-cntx, cntx + 1):
                    for dv in range(-cnty, cnty + 1):
                        p, q = u + du, v + dv
                        if game.valid(p, q):
                            self.map['mark'][p][q] = 1
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
        """
        > The function generates a random map with a treasure hidden in a random location
        """
        # 2 squares that are different in size, the small one is placed inside the
        # bigger one, the treasure is somewhere inside the gap between 2
        # squares. (rare)
        x1 = random.randrange(0, self.height // 2)
        x2 = random.randrange(self.height // 2, self.height)
        y1 = random.randrange(0, self.width // 2)
        y2 = random.randrange(self.width // 2, self.width)
        xx1, xx2 = sorted(random.sample(range(x1 + 1, x2), k=2))
        yy1, yy2 = sorted(random.sample(range(y1 + 1, y2), k=2))

        self.log = f"big rec = ({x1}, {x2}, {y1}, {y2}), small rec = ({xx1}, {xx2}, {yy1}, {yy2})"

        self.map['mark'][x1: x2 + 1, y1: y2 + 1] = 1
        self.map['mark'][xx1: xx2 + 1, yy1: yy2 + 1] = 0

    def hint_15(self):
        """
        > The treasure is in a region that has mountain

        The function is called `hint_15` because it is the 15th hint. 

        The first line of the function is `self.log = "ok"`. This is a log message that will be displayed
        in the game. 

        The next line is `region = random.choice(game.REGION_WITH_MOUNTAIN_LIST)`. This line chooses a
        random region from the list of regions that have mountains. 

        The next line is a `for` loop. This loop goes through every cell in the map. 

        The next line is `if game.MAP['region'][i][j] == region:`. This line checks if the region of the
        current cell is the same as the region that was chosen. 

        The next line is `self.map['mark'][i][j] = 1`. This line
        """
        # The treasure is in a region that has mountain
        self.log = "ok"

        region = random.choice(game.REGION_WITH_MOUNTAIN_LIST)

        for i in range(self.height):
            for j in range(self.width):
                if game.MAP['region'][i][j] == region:
                    self.map['mark'][i][j] = 1

    def hint_16(self):
        """
        It randomly picks half of the tiles on the map and marks them as containing the treasure
        """
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
        """
        If the agent is in the same location as the treasure, then the agent knows that the treasure is
        in that location
        :return: The truthness of the map at the location of the treasure.
        """
        return self.map['contains'][game.TREASURE[0]][game.TREASURE[1]]
