from generate_map import *

def hint_1(array_map, n):
    num = random.randint(1,12)
    cnt = 0
    tiles = []
    while cnt != num:
        row = random.randint(1,n-2)
        col = random.randint(1,n-2)
        if '0' in array_map[row][col] or 'P' in array_map[row][col] or 'M' in array_map[row][col]:
            continue
        tiles.append((row,col))
        cnt += 1
    return ("h1", tiles)

def hint_2(array_map, n):
    region_list = []
    for i in range(1,7):
        if str(i) in array_map:
            region_list.append(i)
    region = random.sample(region_list, random.randint(2,5))
    return ("h2", region)

def hint_3(array_map, n):
    region_list = []
    for i in range(1,7):
        if str(i) in array_map:
            region_list.append(i)
    region = random.sample(region_list, random.randint(1,3))
    return ("h3", region)

def hint_4(array_map, n):
    while True:
        tlbr = random.sample(range(n), 4)
        tlbr.sort()
        if (tlbr[3] - tlbr[1]) >= int(n/2) and (tlbr[2] - tlbr[0]) >= int(n/2):
            break
    return ("h4", tlbr)

def hint_5(array_map, n):
    while True:
        tlbr = random.sample(range(n), 4)
        tlbr.sort()
        if (tlbr[3] - tlbr[1]) <= int(n/3) and (tlbr[2] - tlbr[0]) <= int(n/3):
            break
    return ("h5", tlbr)

def hint_6(array_map, n):
    pirate = minDistance(array_map, 'p')
    agent = minDistance(array_map, 'A')

    #verify hint 6
    if pirate != -1 and agent != -1:
        if len(pirate.preStep) > len(agent.preStep):
            return ("h6", True) #agent is nearest T
        return ("h6", False) #otherwise

def hint_7(array_map, n):
    for i in range(n):
        for j in range(n):
            if "T" in array_map[i][j]:
                row_col = random.randint(0,1) #0: row, 1: col
                if row_col == 0:
                    return ("h7", ("r", i))
                return ("h7", ("c", j))

def hint_8(array_map, n):
    while True:
        row = random.randint(1,n-2)
        col = random.randint(1,n-2)
        if '0' in array_map[row][col] or 'P' in array_map[row][col] or 'M' in array_map[row][col]:
            continue
        row_col = random.randint(0,1) #0: row, 1: col
        if row_col == 0:
            return ("h8", ("r", row))
        return ("h8", ("c", col))


def hint_12(array_map, n):
    print(int(np.flatnonzero(np.core.defchararray.find(array_map, "T") != -1)))
    if float(int(np.flatnonzero(np.core.defchararray.find(array_map, "T") != -1))/n) >= float(n/2):
       return ("h12", False) #half bot has T
    return ("h12", True) #half top has T


hint_list = []
hint_list.append(hint_1(array_map, n))
hint_list.append(hint_2(array_map, n))
hint_list.append(hint_3(array_map, n))
hint_list.append(hint_4(array_map, n))
hint_list.append(hint_5(array_map, n))
array_map[4][3] += 'A'
hint_list.append(hint_6(array_map, n))
hint_list.append(hint_7(array_map, n))
hint_list.append(hint_8(array_map, n))
hint_list.append(hint_12(array_map, n))



print()
for i in hint_list:
    print(i, end='\n')

