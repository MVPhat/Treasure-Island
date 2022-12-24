import random
import numpy as np

n = 64
array_map = np.chararray([n,n], 3, "utf-8")


def fill_region(array_map, n,  topl, topr, botl, botr):
    #topl
    while topl[0] >= 1 and topl[1] >= 1:
        topl[0] -= 1
        topl[1] -= 1
        for i in range(topl[1], int(n/2-1) + 1):
            array_map[topl[0]][i] = array_map[int(n/2-1)][int(n/2-1)] 
            array_map[i][topl[0]] = array_map[int(n/2-1)][int(n/2-1)]
    #topr       
    while topr[0] >= 1 and topr[1] < n-1:    
        topr[0] -= 1
        topr[1] += 1
        for i in reversed(range(int(n/2), topr[1] + 1)):
            array_map[topr[0]][i] = array_map[int(n/2) - 1][int(n/2)]
        for i in range(topr[0], int(n/2)):
            array_map[i][topr[1]] = array_map[int(n/2) - 1][int(n/2)]

    #botl
    while botl[0] < n-1 and botl[1] >= 1:
        botl[0] += 1
        botl[1] -= 1
        for i in reversed(range(int(n/2), botl[0] + 1)):
            array_map[i][botl[1]] = array_map[int(n/2)][int(n/2) - 1]
        for i in range(botl[1], int(n/2 -1) + 1):
            array_map[botl[0]][i] = array_map[int(n/2)][int(n/2) - 1]

    #botr
    while botr[0] < n-1 and botr[1] < n-1:
        botr[0] += 1
        botr[1] += 1
        for i in reversed(range(int(n/2), botr[0] + 1)):
            array_map[i][botr[1]] = array_map[int(n/2)][int(n/2)]
            array_map[botr[1]][i] = array_map[int(n/2)][int(n/2)]

    return array_map

def gen_r_left(array_map, n, re_left):
    for i in range(4,6):
        index_row = random.randint(4,n-4)
        index_col = random.randint(4, n-4)
        size = random.randint(int(n/4), int(n/2))
        #print(f"number {str(i)} with row: {index_row} and col: {index_col} and size: {size}")
        for j in range(index_row, n - 2):
            cnt = 0
            for k in range(index_col, n - 2):
                if cnt == size: break
                if j < n -1 and k < n - 1:
                    array_map[j][k] = str(re_left[i])
                cnt += 1
    return array_map

def gen_M_and_P_and_T(array_map, n):
    ranPirate = []
    for i in range(1,7):
        if str(i) in array_map:
            prison = list(zip(*np.where(array_map == str(i))))
            ranprison = random.randint(0, len(prison) - 1)
            array_map[prison[ranprison][0]][prison[ranprison][1]] += "P"
            ranPirate.append((prison[ranprison][0], prison[ranprison][1]))

    ranIndexPirate = random.randint(0, len(ranPirate) - 1)

    array_map[ranPirate[ranIndexPirate][0]][ranPirate[ranIndexPirate][1]] += "p"

    for i in range(n):
        for j in range(n):
            mountain = random.randint(0, 5) #0: yes, >=1: no
            if mountain == 0 and "P" not in array_map[i][j] and array_map[i][j] != "0":
                array_map[i][j] = array_map[i][j] + "M"
    while True:
        row = random.randint(1,n-2)
        col = random.randint(1, n-2)
        if array_map[row][col] != '0' and "P" not in array_map[row][col] and "M" not in array_map[row][col]:
            array_map[row][col] += "T"
            break
        
    return array_map

def fix_missing_region(array_map, n, regions):
    arr_tmp = np.array(array_map, dtype=np.int32)
    fix = []
    for i in range(1, regions):
        if str(i) not in array_map:
            fix.append(str(i))
    deleteNum = arr_tmp.argsort()[len(fix):]
    print(fix)
    print("delete:", deleteNum)

def gen_map(array_map, n):
    # 1->6
    regions = 7

    re_left = random.sample(range(1,regions), 6)

    topl = [int((n/2)-1), int((n/2)-1)]
    topr = [int((n/2)-1), int((n/2))]
    botl = [int((n/2)), int((n/2)-1)]
    botr = [int((n/2)), int((n/2))]

    array_map[topl[0]][topl[1]] = str(re_left[0])
    array_map[topr[0]][topr[1]] = str(re_left[1])
    array_map[botl[0]][botl[1]] = str(re_left[2])
    array_map[botr[0]][botr[1]] = str(re_left[3])

    array_map = fill_region(array_map, n, topl, topr, botl, botr)
    array_map = gen_r_left(array_map, n, re_left)

    #random sea
    array_map[0] = "0"
    array_map[n-1] = "0"
    array_map[:,0] = "0"
    array_map[:, n-1] = "0"
    for i in range(1, n-2):
        sea = random.randint(0,3)
        #print(sea)
        
        left_right = random.randint(0,1) #0: left, 1: right
        up_down = random.randint(0, 1) #0: up, 1: down

        if left_right == 0:
            for j in range(sea):
                array_map[i][j] = "0"
        else:
            for j in range(n - 1 - sea, n - 1):
                array_map[i][j] = "0"

        if up_down == 0:
            for k in range(sea):
                array_map[k][i] = "0"
        else:
            for h in range(n - 1 - sea, n- 1):
                array_map[h][i] = "0"
    #fix_missing_region(array_map, n, regions)
    array_map = gen_M_and_P_and_T(array_map,n)
    return array_map

class Cell:
    def __init__(self, row, col, dist, preStep):
        self.row = row
        self.col = col
        self.dist = dist
        self.preStep = list(preStep)

def minDistance(array_map):
    source = Cell(0, 0, 0, [])
 
    # Finding the source to start from
    for row in range(len(array_map)):
        for col in range(len(array_map[row])):
            if 'p' in array_map[row][col]:
                source.row = row
                source.col = col
                source.preStep.append((source.row, source.col))
                break
 
    # To maintain location visit status
    visited = [[False for _ in range(len(array_map[0]))]
               for _ in range(len(array_map))]
     
    # applying BFS on matrix cells starting from source
    queue = []
    queue.append(source)
    visited[source.row][source.col] = True
    while len(queue) != 0:
        source = queue.pop(0)
        # Destination found;
        if ("T" in array_map[source.row][source.col]):
            return source

        # moving up
        if isValid(source.row - 1, source.col, array_map, visited):
            nextStep = Cell(source.row - 1, source.col, source.dist + 1, source.preStep)
            nextStep.preStep.append(((nextStep.row, nextStep.col)))
            queue.append(nextStep)
            #print("up", source.row, source.col)
            visited[source.row - 1][source.col] = True
 
        # moving down
        if isValid(source.row + 1, source.col, array_map, visited):
            nextStep = Cell(source.row + 1, source.col, source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("down", source.row, source.col)
            visited[source.row + 1][source.col] = True
 
        # moving left
        if isValid(source.row, source.col - 1, array_map, visited):
            nextStep = Cell(source.row, source.col - 1, source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("left", source.row, source.col)
            visited[source.row][source.col - 1] = True
 
        # moving right
        if isValid(source.row, source.col + 1, array_map, visited):
            nextStep = Cell(source.row, source.col + 1, source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("right", source.row, source.col)
            visited[source.row][source.col + 1] = True

    return -1

def isValid(x, y, array_map, visited):
    if ((x >= 0 and y >= 0) and
        (x < len(array_map) and y < len(array_map[0])) and
            (array_map[x][y] != '0') and ("M" not in array_map[x][y]) and (visited[x][y] == False)):
        return True
    return False


array_map = gen_map(array_map, n)
print(array_map)
res = minDistance(array_map)
if (res != -1):
    print("Number of steps:", res.dist)
    print("Pirate is in:", res.preStep.pop(0))
    print(res.preStep)
else: print("Can not find")

