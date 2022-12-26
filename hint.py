import random
import numpy as np
from generate_map import minDistance


class Hint:
    def __init__(self, array_map, n):
        self.map = array_map
        self.n = n
        self.mask_map = np.ones([n, n], dtype=bool)
        self.hint_list = []

    def hint_1(self):
        # A list of random tiles that doesn't contain the treasure (1 to 12).
        num = random.randint(1, 12)
        cnt = 0
        while cnt != num:
            row = random.randint(1, self.n-2)
            col = random.randint(1, self.n-2)
            value, dump, _ = self.map[row][col]
            if value == 0 or dump == "P" or dump == 'M':
                continue
            self.map[row][col] = (value, dump, True)
            cnt += 1

    def hint_2(self):
        # 2-5 regions that 1 of them has the treasure.
        region_list = []
        for i in range(1, 7):
            if str(i) in self.map:
                region_list.append(i)
        region = random.sample(region_list, random.randint(2, 5))
        self.hint_list.append(("h2", region))

    def hint_3(self):
        # 1-3 regions that do not contain the treasure.
        region_list = []
        for i in range(1, 7):
            if str(i) in self.map:
                region_list.append(i)
        region = random.sample(region_list, random.randint(1, 3))
        self.hint_list.append(("h3", region))

    def hint_4(self):
        # A large rectangle area that has the treasure
        while True:
            rectangle = random.sample(range(self.n), 4)
            rectangle.sort()
            if (rectangle[3] - rectangle[1]) >= int(self.n/2) and (rectangle[2] - rectangle[0]) >= int(self.n/2):
                break
        self.hint_list.append(("h4", rectangle))

    def hint_5(self):
        # A small rectangle area that doesn't has the treasure.
        while True:
            rectangle = random.sample(range(self.n), 4)
            rectangle.sort()
            if (rectangle[3] - rectangle[1]) <= int(self.n/3) and (rectangle[2] - rectangle[0]) <= int(self.n/3):
                break
        self.hint_list.append(("h5", rectangle))

    def hint_6(self):
        # He tells you that you are the nearest person to the treasure (between
        # you and the prison he is staying)
        pirate = minDistance(self.map, 'p')
        agent = minDistance(self.map, 'A')

        # verify hint 6
        if pirate != -1 and agent != -1:
            if len(pirate.preStep) > len(agent.preStep):
                self.hint_list.append(("h6", True))  # agent is nearest T
            else:
                self.hint_list.append(("h6", False))  # otherwise

    def hint_7(self):
        # A column and/or a row that contain the treasure (rare)
        for i in range(self.n):
            for j in range(self.n):
                if "T" in self.map[i][j]:
                    row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
                    if row_col == 0:
                        self.hint_list.append(("h7", ("r", i)))
                    elif row_col == 1:
                        self.hint_list.append(("h7", ("c", j)))
                    else:
                        self.hint_list.append(("h7", ("r_c", i, j)))

    def hint_8(self):
        # A column and/or a row that do not contain the treasure.
        while True:
            row = random.randint(1, self.n-2)
            col = random.randint(1, self.n-2)
            if '0' in self.map[row][col] or 'P' in self.map[row][col] or 'M' in self.map[row][col]:
                continue
            row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
            if row_col == 0:
                self.hint_list.append(("h8", ("r", row)))
                return
            elif row_col == 1:
                self.hint_list.append(("h8", ("c", col)))
                return
            else: 
                self.hint_list.append(("h8", ("r_c", row, col)))
            return

    def hint_9(self):
        # 2 regions that the treasure is somewhere in their boundary
        return

    def hint_10(self):
        # The treasure is somewhere in a boundary of 2 regions
        return

    def hint_11(self):
        # The treasure is somewhere in an area bounded by 2-3 tiles from sea.
        tiles = random.randint(2, 3)
        cnt = [i for i in range(self.n)]
        index = []

        for i in range(tiles):
            index_top = 1
            index_bot = self.n - 2
            index_left = 1
            index_right = self.n - 2

        #self.hint_list.append(("h11", random.random(2,3)))

    def hint_12(self):
        # A half of the map without treasure (rare)
        if float(int(np.flatnonzero(np.core.defchararray.find(self.map, "T") != -1))/self.n) >= float(self.n/2):
            self.hint_list.append(("h12", False))  # half bot has T
        else:
            self.hint_list.append(("h12", True))  # half top has T

    def hint_13(self):
        # From the center of the map/from the prison that he's staying, he tells
        # you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW)
        # (The shape of area when the hints are either W, E, N or S is triangle).
        return

    def hint_14(self):
        # 2 squares that are different in size, the small one is placed inside the
        # bigger one, the treasure is somewhere inside the gap between 2
        # squares. (rare)
        while True:
            while True:
                rectangle = random.sample(range(self.n), 4)
                rectangle.sort()
                if (rectangle[3] - rectangle[1]) >= int(self.n/3) and (rectangle[2] - rectangle[0]) >= int(self.n/3):
                    break
            big = rectangle

            while True:
                rectangle = random.sample(range(self.n), 4)
                rectangle.sort()
                if (rectangle[3] - rectangle[1]) <= int(self.n/5) and (rectangle[2] - rectangle[0]) <= int(self.n/5):
                    break
            small = rectangle

            if big[0] < small[0] and big[1] < small[1] and big[2] > small[2] and big[3] > small[3]:
                self.hint_list.append(("h14", big, small))
                break

    def hint_15(self):
        # The treasure is in a region that has mountain
        mountain_region = []
        for i in range(self.n):
            for j in range(self.n):
                if 'M' in self.map[i][j] and self.map[i][j][0] not in mountain_region:
                    mountain_region.append(self.map[i][j][0])
        self.hint_list.append(
            ("h15", mountain_region[random.randint(0, len(mountain_region) - 1)]))

    def verify(self, choose):
        isTrue = False
        if choose[0] == "h1":
            #contain or not contain
            for i in choose[1]:
                if "T" in self.map[i[0]][i[1]]:
                    isTrue = True  # 1-> 12 tiles contain T
            for i in range(self.n):
                for j in range(self.n):
                    if isTrue == True and (i, j) not in choose[1]:
                        self.mask_map[i][j] = False
                    elif isTrue == False and (i, j) in choose[1]:
                        self.mask_map[i][j] = False

        elif choose[0] == "h2" or choose[0] == "h3":
            r = ""
            for i in choose[1]:
                if str(i) + "T" in self.map:
                    isTrue = True
                    r = str(i)
            for i in range(self.n):
                for j in range(self.n):
                    if isTrue == True and r != "" and r != self.map[i][j][0]:
                        self.mask_map[i][j] = False
                    elif isTrue == False and r == "" and int(self.map[i][j][0]) in choose[1]:
                        self.mask_map[i][j] = False

        elif choose[0] == "h4" or choose[0] == "h5":
            row = choose[1][0]
            col = choose[1][1]
            index = []
            while True:
                if col == choose[1][3]:
                    col = choose[1][1]
                    row += 1
                    if row > choose[1][2]:
                        break
                index.append((row, col))
                if "T" in self.map[row][col]:
                    isTrue = True
                col += 1

            if isTrue == False:
                for i in index:
                    self.mask_map[i[0]][i[1]] = False
            else:
                for i in range(self.n):
                    for j in range(self.n):
                        if (i, j) not in index:
                            self.mask_map[i][j] = False

        elif choose[0] == "h6":
            isTrue = choose[1]

        elif choose[0] == "h7" or choose[0] == "h8":
            if choose[1][0] == "r":
                for i in range(self.n):
                    if "T" in self.map[choose[1][1]][i]:
                        isTrue = True
            elif choose[1][0] == "c":
                for i in range(self.n):
                    if "T" in self.map[i][choose[1][1]]:
                        isTrue = True
            else:
                for i in range(self.n):
                    if "T" in self.map[choose[1][1]][i] or "T" in self.map[i][choose[1][1]]:
                        isTrue = True
            if choose[1][0] == "r" and isTrue == False:
                self.mask_map[choose[1][1]][:] = False
            elif choose[1][0] == "c" and isTrue == False:
                self.mask_map[:][choose[1][1]] = False
            elif choose[1][0] == "r_c" and isTrue == False:
                self.map[choose[1][1]][:] = False
                self.map[:][choose[1][1]] = False
            # mask another if row/col has T
            return

        elif choose[0] == "h9":
            return
        elif choose[0] == "h10":
            return
        elif choose[0] == "h11":
            return
        elif choose[0] == "h12":
            return
        elif choose[0] == "h13":
            return
        elif choose[0] == "h14":
            return
        elif choose[0] == "h15":
            return
        return isTrue

    def print_hint_list(self):
        print()
        for i in self.hint_list:
            print(i, end='\n')
