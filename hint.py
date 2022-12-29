from pirate import verify_hint6
from visualization import Visualization
import random
import numpy as np


class Hint:
    def __init__(self, array_map, n, hint):
        self.map = array_map
        self.n = n
        self.hint = hint
        self.is_center_prison = ''
        self.direction = ''

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
        region_list = list(np.unique(self.map['region']))
        region_list.pop(0)
        region = random.sample(list(region_list), random.randint(2, 5))

        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j]['region'] in region:
                    self.map[i][j] = (self.map[i][j]['region'],
                                      self.map[i][j]['type'], True, 1)

    def hint_3(self):
        # 1-3 regions that do not contain the treasure.
        region_list = list(np.unique(self.map['region']))
        region_list.pop(0)
        region = random.sample(region_list, random.randint(1, 3))

        for i in range(self.n):
            for j in range(self.n):
                if self.map[i][j]['region'] in region:
                    self.map[i][j] = (self.map[i][j]['region'],
                                      self.map[i][j]['type'], True, 1)

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
        return

    def hint_7(self):
        # A column and/or a row that contain the treasure (rare)
        row = random.randint(1, self.n-2)
        col = random.randint(1, self.n-2)
        row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
        if row_col == 0:
            self.map[row, ]['mark'] = True

        elif row_col == 1:
            self.map[:, col]['mark'] = True

        else:
            self.map[row, ]['mark'] = True
            self.map[:, col]['mark'] = True

    def hint_8(self):
        # A column and/or a row that do not contain the treasure.
        row = random.randint(1, self.n-2)
        col = random.randint(1, self.n-2)
        row_col = random.randint(0, 2)  # 0: row, 1: col, 2: both
        if row_col == 0:
            self.map[row, ]['mark'] = True
        elif row_col == 1:
            self.map[:, col]['mark'] = True
        else:
            self.map[row, ]['mark'] = True
            self.map[:, col]['mark'] = True

    def hint_9(self):
        # 2 regions that the treasure is somewhere in their boundary
        region_list = np.unique(self.map['region'])
        region = random.randint(1, np.max(region_list))
        neighbors = []
        for i in range(self.n):
            for j in range(self.n):
                if (self.map['region'][i][j] == region):
                    top = self.map['region'][i+1][j]
                    if (top != region and top not in neighbors and top != 0):
                        neighbors.append(top)
                    bottom = self.map['region'][i-1][j]
                    if (bottom != region and bottom not in neighbors and bottom != 0):
                        neighbors.append(bottom)
                    left = self.map['region'][i][j+1]
                    if (left != region and left not in neighbors and left != 0):
                        neighbors.append(left)
                    right = self.map['region'][i][j-1]
                    if (right != region and right not in neighbors and right != 0):
                        neighbors.append(right)
        neighbor = random.sample(list(neighbors), 1)[0]
        # print(region, neighbor)
        for i in range(self.n):
            for j in range(self.n):
                if (self.map['region'][i][j] == region):
                    top = self.map['region'][i+1][j]
                    if (top == neighbor):
                        self.map[i][j]['mark'] = True
                        self.map[i+1][j]['mark'] = True
                    bottom = self.map['region'][i-1][j]
                    if (bottom == neighbor):
                        self.map[i][j]['mark'] = True
                        self.map[i-1][j]['mark'] = True
                    left = self.map['region'][i][j+1]
                    if (left == neighbor):
                        self.map[i][j]['mark'] = True
                        self.map[i][j+1]['mark'] = True
                    right = self.map['region'][i][j-1]
                    if (right == neighbor):
                        self.map[i][j]['mark'] = True
                        self.map[i][j-1]['mark'] = True

    def hint_10(self):
        # The treasure is somewhere in a boundary of 2 regions
        region_list = np.unique(self.map['region'])
        for region in range(1, np.max(region_list)):
            neighbors = []
            for i in range(self.n):
                for j in range(self.n):
                    if (self.map['region'][i][j] == region):
                        top = self.map['region'][i+1][j]
                        if (top != region and top not in neighbors and top != 0):
                            neighbors.append(top)
                        bottom = self.map['region'][i-1][j]
                        if (bottom != region and bottom not in neighbors and bottom != 0):
                            neighbors.append(bottom)
                        left = self.map['region'][i][j+1]
                        if (left != region and left not in neighbors and left != 0):
                            neighbors.append(left)
                        right = self.map['region'][i][j-1]
                        if (right != region and right not in neighbors and right != 0):
                            neighbors.append(right)
            for neighbor in neighbors:
                for i in range(self.n):
                    for j in range(self.n):
                        if (self.map['region'][i][j] == region):
                            top = self.map['region'][i+1][j]
                            if (top == neighbor):
                                self.map[i][j]['mark'] = True
                                self.map[i+1][j]['mark'] = True
                            bottom = self.map['region'][i-1][j]
                            if (bottom == neighbor):
                                self.map[i][j]['mark'] = True
                                self.map[i-1][j]['mark'] = True
                            left = self.map['region'][i][j+1]
                            if (left == neighbor):
                                self.map[i][j]['mark'] = True
                                self.map[i][j+1]['mark'] = True
                            right = self.map['region'][i][j-1]
                            if (right == neighbor):
                                self.map[i][j]['mark'] = True
                                self.map[i][j-1]['mark'] = True

    def hint_11(self):
        # The treasure is somewhere in an area bounded by 2-3 tiles from sea.
        bounded = random.randint(2, 3)
        for i in range(self.n):
            for j in range(self.n):
                if (self.map['region'][i][j] == 0):
                    for b in range(1, bounded + 1):
                        if (i + b < self.n):
                            top = self.map['region'][i+b][j]
                            if (top != 0):
                                self.map[i+b][j]['mark'] = True
                        if (i-b > 0):
                            bottom = self.map['region'][i-b][j]
                            if (bottom != 0):
                                self.map[i-b][j]['mark'] = True
                        if (j + b < self.n):
                            left = self.map['region'][i][j+b]
                            if (left != 0):
                                self.map[i][j+b]['mark'] = True
                        if (j - b > 0):
                            right = self.map['region'][i][j-b]
                            if (right != 0):
                                self.map[i][j-b]['mark'] = True
        # self.hint_list.append(("h11", random.random(2,3)))

    def hint_12(self):
        # A half of the map without treasure (rare)
        half = random.randint(0, 1)
        if half == 0:  # row half
            half = random.randint(0, 1)
            if half == 0:  # top half
                self.map[0:(int(self.n/2))]['mark'] = True
            else:
                self.map[int(self.n/2):(self.n)]['mark'] = True

        else:  # col half
            half = random.randint(0, 1)
            if half == 0:  # left half
                self.map[:, 0:int(self.n/2)]['mark'] = True
            else:
                self.map[:, int(self.n/2):self.n]['mark'] = True

    def hint_13(self):
        # From the center of the map/from the prison that he's staying, he tells
        # you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW)
        # (The shape of area when the hints are either W, E, N or S is triangle).

        #treasure = list(*np.argwhere(self.map['type'] == 'T'))
        is_center_prison = random.choice(["center", "prison"])
        direction = random.choice(["W", "E", "N", "S", "SE", "SW", "NE", "NW"])
        direction = 'S'
        if is_center_prison == "center":
            if direction == 'SE':
                self.map[0:int(self.n/2), 0:int(self.n/2)]['mark'] = True
            elif direction == 'SW':
                self.map[0:int(self.n/2), int(self.n/2):self.n]['mark'] = True
            elif direction == 'NE':
                self.map[int(self.n/2):self.n, 0:int(self.n/2)]['mark'] = True
            elif direction == 'NW':
                self.map[int(self.n/2):self.n, int(self.n/2)                         :self.n]['mark'] = True
            else:
                start = 0
                end = self.n
                while start != int(self.n/2):
                    if direction == 'S':
                        self.map[start][start:end]['mark'] = True
                    elif direction == 'E':
                        self.map[start:end, start]['mark'] = True
                    elif direction == 'N':
                        self.map[end - 1][start:end]['mark'] = True
                    else:
                        self.map[start:end, end - 1]['mark'] = True
                    start += 1
                    end -= 1
        else:
            prison = self.find_prison_index()
            self.pri_r = prison[0]
            self.pri_c = prison[1]
            if direction == 'SE':
                self.map[0:(prison[0] + 1), 0:(prison[1] + 1)]['mark'] = True
            elif direction == 'SW':
                self.map[0:(prison[0] + 1), prison[1]:self.n]['mark'] = True
            elif direction == 'NE':
                self.map[prison[0]:self.n, 0:(prison[1] + 1)]['mark'] = True
            elif direction == 'NW':
                self.map[prison[0]:self.n, prison[1]:self.n]['mark'] = True
            else:
                row = prison[0]
                col = prison[1]
                self.map[row, col]['mark'] = True
                layer = 1
                while True:
                    if direction == 'N':
                        row += 1
                        if row >= self.n:
                            break
                    elif direction == 'S':
                        row -= 1
                        if row < 0:
                            break
                    elif direction == 'E':
                        col -= 1
                        if col < 0:
                            break
                    else:
                        col += 1
                        if col >= self.n:
                            break

                    if direction == 'N' or direction == 'S':
                        tmp_left = col - layer
                        tmp_right = col + layer + 1
                        if col - layer < 0:
                            tmp_left = 0
                        if col + layer + 1 > self.n:
                            tmp_right = self.n
                        self.map[row, tmp_left:tmp_right]['mark'] = True
                    else:
                        tmp_left = row - layer
                        tmp_right = row + layer + 1
                        if row - layer < 0:
                            tmp_left = 0
                        if row + layer + 1 > self.n:
                            tmp_right = self.n
                        self.map[tmp_left:tmp_right, col]['mark'] = True
                    layer += 1
        self.is_center_prison = is_center_prison
        self.direction = direction

    def hint_14(self):
        # 2 squares that are different in size, the small one is placed inside the
        # bigger one, the treasure is somewhere inside the gap between 2
        # squares. (rare)
        while True:
            while True:
                rectangle = random.sample(range(self.n), 4)
                rectangle.sort()
                if (rectangle[3] - rectangle[1]) >= int(self.n/3) and (rectangle[2] - rectangle[0]) >= int(self.n/3) and (rectangle[2] - rectangle[0]) == (rectangle[3] - rectangle[1]):
                    break
            big = rectangle

            while True:
                rectangle = random.sample(range(self.n), 4)
                rectangle.sort()
                if (rectangle[3] - rectangle[1]) <= int(self.n/3) and (rectangle[2] - rectangle[0]) <= int(self.n/3) and (rectangle[2] - rectangle[0]) == (rectangle[3] - rectangle[1]):
                    break
            small = rectangle

            if big[0] < small[0] and big[1] < small[1] and big[2] > small[2] and big[3] > small[3]:
                for i in range(big[0], big[2] + 1):
                    for j in range(big[1], big[3] + 1):
                        if i >= small[0] and i <= small[2] and j >= small[1] and j <= small[3]:
                            continue
                        self.map[i][j]['mark'] = True
                break

    def hint_15(self):
        # The treasure is in a region that has mountain
        region_list = list(np.unique(self.map['region']))
        region_mountain = []
        for r in range(self.n):
            for c in range(self.n):
                if self.map[r][c]['type'] == 'M' and self.map[r][c]['region'] in region_list and self.map[r][c]['region'] not in region_mountain:
                    region_mountain.append(self.map[r][c]['region'])
        pick_region = random.randint(0, len(region_mountain) - 1)
        for r in range(self.n):
            for c in range(self.n):
                if self.map[r][c]['region'] == region_mountain[pick_region]:
                    self.map[r][c]['mark'] = True

    def verify(self, turn, list_log, line, test=False):
        if self.hint == 'h1' or self.hint == 'h3' or self.hint == 'h5' or self.hint == 'h8':
            hint_isPositive = False
        elif self.hint == 'h6':
            # verify....
            hint_res = True
            agent = verify_hint6(self.map, 'A')
            pirate = verify_hint6(self.map, 'p')
            if pirate[0] < agent[0]:
                hint_res = False
                print(f'\t\tHINT [verify]: {hint_res}')
                list_log.append(f'\t\tHINT [verify]: {hint_res}')
            return hint_res, list_log, (line + 1)
        elif self.hint == 'h13':
            hint_res = self.verify_hint13()
            print(f'\t\tHINT [verify]: {hint_res}')
            list_log.append(f'\t\tHINT [verify]: {hint_res}')
            return hint_res, list_log, (line + 1)
        else:
            hint_isPositive = True

        dump = [str(self.map['type'][i][j]) + str(self.map['mark'][i][j])
                for i in range(self.n) for j in range(self.n)]
        hint_res = not (('TTrue' in dump) ^ hint_isPositive)

        if (test and not hint_res):
            return hint_res, list_log
        if (test):
            visual = Visualization(self.n, self.n, self.map)
            filename = f'TURN[{turn}]_HINT[{self.hint}]_visual'
            visual.visualize(filename)
            print(f'\t\tHINT [visualization]: {filename}.eps')

        print(f'\t\tHINT [verify]: {hint_res}')
        list_log.append(f'\t\tHINT [verify]: {hint_res}')
        for i in range(self.n):
            for j in range(self.n):
                value, dump, visual, ratio = self.map[i][j]
                if (ratio == 0):
                    ratio = 0
                else:
                    if hint_isPositive:
                        ratio = 1 if not (hint_res ^ visual) else 0
                    else:
                        ratio = 1 if (hint_res ^ visual) else 0
                self.map[i][j] = (value, dump, visual, ratio)

        visual = Visualization(self.n, self.n, self.map)
        filename = f'TURN[{turn}]_HINT[{self.hint}]_verify'
        visual.visualize(filename)
        print(f'\t\tHINT [verify_visual]: {filename}.eps')

        return hint_res, list_log, (line + 1)

    def visualize(self, turn, test=False):
        if (self.hint == 'h1'):
            self.hint_1()
        elif (self.hint == 'h2'):
            self.hint_2()
        elif (self.hint == 'h3'):
            self.hint_3()
        elif (self.hint == 'h4'):
            self.hint_4()
        elif (self.hint == 'h5'):
            self.hint_5()
        elif (self.hint == 'h6'):
             self.hint_6()
        elif (self.hint == 'h7'):
            self.hint_7()
        elif (self.hint == 'h8'):
            self.hint_8()
        elif (self.hint == 'h9'):
            self.hint_9()
        elif (self.hint == 'h10'):
            self.hint_10()
        elif (self.hint == 'h11'):
            self.hint_11()
        elif (self.hint == 'h12'):
            self.hint_12()
        elif (self.hint == 'h13'):
            self.hint_13()
        elif (self.hint == 'h14'):
            self.hint_14()
        elif (self.hint == 'h15'):
            self.hint_15()

        if (not test):
            visual = Visualization(self.n, self.n, self.map)
            filename = f'TURN[{turn}]_HINT[{self.hint}]_visual'
            visual.visualize(filename)
            print(f'\t\tHINT [visualization]: {filename}.eps')

    def print_hint_list(self):
        for i in self.hint_list:
            print(f"{i[0]}, {i[1]}", end='\n')

    def find_prison_index(self):
        prison_list = list(zip(*np.argwhere(self.map['type'] == 'P')))
        ranidx = random.randint(0, len(prison_list[0]) - 1)
        return (prison_list[0][ranidx], prison_list[1][ranidx])

    def verify_hint13(self):
        hint_res = False
        if self.is_center_prison == 'center':
            start = int(self.n/4)
            end = self.n - int(self.n/4) - 1
            if self.direction == 'W':
                if 'T' in self.map[start:end, 0:int(self.n/2)]['type']:
                    hint_res = True
            elif self.direction == 'E':
                if 'T' in self.map[start:end, int(self.n/2):self.n]['type']:
                    hint_res = True
            elif self.direction == 'S':
                if 'T' in self.map[int(self.n/2):self.n, start:end + 1]['type']:
                    hint_res = True
            elif self.direction == 'N':
                if 'T' in self.map[0:int(self.n/2), start:end + 1]['type']:
                    hint_res = True
            elif self.direction == 'NE':
                diagonal = list(np.fliplr(self.map['type']).diagonal())
                for i in range(int(self.n/2)):
                    diagonal.pop(len(diagonal) - 1)
                if 'T' in diagonal:
                    hint_res = True
            elif self.direction == 'SW':
                diagonal = list(np.fliplr(self.map['type']).diagonal())
                for i in range(int(self.n/2)):
                    diagonal.pop(0)
                if 'T' in diagonal:
                    hint_res = True
            elif self.direction == 'SE':
                diagonal = list(self.map['type'].diagonal())
                for i in range(int(self.n/2)):
                    diagonal.pop(0)
                if 'T' in diagonal:
                    hint_res = True
            elif self.direction == 'NW':
                diagonal = list(self.map['type'].diagonal())
                for i in range(int(self.n/2)):
                    diagonal.pop(len(diagonal) - 1)
                if 'T' in diagonal:
                    hint_res = True
        else:
            start = self.pri_r - int(self.n/8)
            end = self.pri_r + int(self.n/8)
            if self.direction == 'W':
                if 'T' in self.map[start:end + 1, 0:self.pri_c + 1]['type']:
                    hint_res = True
            elif self.direction == 'E':
                if 'T' in self.map[start:end + 1, self.pri_c:self.n]['type']:
                    hint_res = True
            start = self.pri_c - int(self.n/8)
            end = self.pri_c + int(self.n/8)
            if self.direction == 'N':
                if 'T' in self.map[0:self.pri_r + 1, start:end + 1]['type']:
                    hint_res = True
            elif self.direction == 'S':
                if 'T' in self.map[self.pri_r:self.n, start:end + 1]['type']:
                    hint_res = True
            else:
                i = self.pri_r
                j = self.pri_c
                while i >= 0 and j >= 0 and i < self.n and j < self.n:
                    if self.map[i][j]['type'] == 'T':
                        hint_res = True
                        break
                    if self.direction == 'SE':
                        i += 1
                        j += 1
                    elif self.direction == 'SW':
                        i += 1
                        j -= 1
                    elif self.direction == 'NW':
                        i -= 1
                        j -= 1
                    elif self.direction == 'NE':
                        i -= 1
                        j += 1
        return hint_res
