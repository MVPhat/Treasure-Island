import random
import numpy as np
from generate_map import minDistance


class Hint:
    def __init__(self, array_map, n):
        self.map = array_map
        self.n = n

    def hint_1(self):
        # A list of random tiles that doesn't contain the treasure (1 to 12).
        num = random.randint(1, 12)
        cnt = 0
        while cnt != num:
            row = random.randint(1, self.n-2)
            col = random.randint(1, self.n-2)
            value, dump, _, ratio = self.map[row][col]
            if value == 0 or dump == "P" or dump == 'M':
                continue
            self.map[row][col] = (value, dump, True, ratio)
            cnt += 1

    def hint_2(self):
        # 2-5 regions that 1 of them has the treasure.
        region_list = np.unique(self.map['region'])
        region = random.sample(list(region_list), random.randint(2, 5))

        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j]['region'] in region:
                    self.map[i][j] = (self.map[i][j]['region'], self.map[i][j]['type'], True, 1)
        

    def hint_3(self):
        # 1-3 regions that do not contain the treasure.
        region_list = []
        for i in range(1, 7):
            if i in self.map['region']:
                region_list.append(i)

        region = random.sample(region_list, random.randint(1, 3))
        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j]['region'] in region:
                    self.map[i][j] = (self.map[i][j]['region'], self.map[i][j]['type'], True, 1)

    def hint_4(self):
        # A large rectangle area that has the treasure
        while True:
            rectangle = random.sample(range(self.n), 4)
            rectangle.sort()
            if (rectangle[3] - rectangle[1]) >= int(self.n/2) and (rectangle[2] - rectangle[0]) >= int(self.n/2):
                break
        self.map[rectangle[0]:(rectangle[2] + 1), rectangle[1]:(rectangle[3] + 1)]['mark'] = True
        # map_visualize[rectangle[0]:(rectangle[2] + 1),
        #               rectangle[1]:(rectangle[3] + 1)] = True
        # self.hint_list.append(("h4", rectangle, map_visualize))

    def hint_5(self):
        # A small rectangle area that doesn't has the treasure.
        while True:
            rectangle = random.sample(range(self.n), 4)
            rectangle.sort()
            if (rectangle[3] - rectangle[1]) <= int(self.n/3) and (rectangle[2] - rectangle[0]) <= int(self.n/3):
                break
        self.map[rectangle[0]:(rectangle[2] + 1), rectangle[1]:(rectangle[3] + 1)]['mark'] = True

    def hint_6(self):
        # He tells you that you are the nearest person to the treasure (between
        # you and the prison he is staying)
        pirate = minDistance(self.map, 'p')
        agent = minDistance(self.map, 'A')
        return
        # verify hint 6
        # if pirate != -1 and agent != -1:
        #     if len(pirate.preStep) > len(agent.preStep):
        #         self.hint_list.append(("h6", True))  # agent is nearest T
        #     else:
        #         self.hint_list.append(("h6", False))  # otherwise

    def hint_7(self):
        # A column and/or a row that contain the treasure (rare)
        row = random.randint(1, self.n-2)
        col = random.randint(1, self.n-2)
        #map_visualize = np.zeros([self.n, self.n], dtype=bool)
        row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
        if row_col == 0:
            self.map[row, ]['mark'] = True
            #map_visualize[row, ] = True
            #self.hint_list.append(("h7", ("r", row), map_visualize))
        elif row_col == 1:
            self.map[:, col]['mark'] = True
            # map_visualize[:, col] = True
            # self.hint_list.append(("h7", ("c", col), map_visualize))
        else:
            self.map[row, ]['mark'] = True
            self.map[:, col]['mark'] = True
        #     map_visualize[row, ] = True
        #     map_visualize[:, col] = True
        #     self.hint_list.append(("h7", ("r_c", row, col), map_visualize))
        # return map_visualize

    def hint_8(self):
        # A column and/or a row that do not contain the treasure.
        row = random.randint(1, self.n-2)
        col = random.randint(1, self.n-2)
        #map_visualize = np.zeros([self.n, self.n], dtype=bool)
        row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
        if row_col == 0:
            self.map[row, ]['mark'] = True
            #map_visualize[row, ] = True
            #self.hint_list.append(("h7", ("r", row), map_visualize))
        elif row_col == 1:
            self.map[:, col]['mark'] = True
            # map_visualize[:, col] = True
            # self.hint_list.append(("h7", ("c", col), map_visualize))
        else:
            self.map[row, ]['mark'] = True
            self.map[:, col]['mark'] = True
        #     map_visualize[row, ] = True
        #     map_visualize[:, col] = True
        #     self.hint_list.append(("h7", ("r_c", row, col), map_visualize))
        # return map_visualize

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

        # self.hint_list.append(("h11", random.random(2,3)))

    def hint_12(self):
        # A half of the map without treasure (rare)
        half = random.randint(0,1)
        if half == 0: #row half
            col = self.n
            row = int(self.n/2)
        else:
            row = self.n
            col = int(self.n/2)
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
                self.hint_list.append(("h14", (big, small)))
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
        if choose == "h1" or choose == "h2" or choose == "h3":
            dump = [str(self.map['type'][i][j]) + str(self.map['mark'][i][j])
                    for i in range(self.n) for j in range(self.n)]
            hint_res = 'TTrue' in dump

            print(f'Hint {choose} is: {hint_res}')

            for i in range(self.n):
                for j in range(self.n):
                    value, dump, visual, ratio = self.map[i][j]
                    if (ratio == 0):
                        ratio = 0
                    else:
                        if not (visual ^ hint_res):
                            ratio = 1
                        else:
                            ratio = 0
                    self.map[i][j] = (value, dump, visual, ratio)

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
        # return isTrue

    def print_hint_list(self):
        print()
        for i in self.hint_list:
            print(f"{i[0]}, {i[1]}", end='\n')
