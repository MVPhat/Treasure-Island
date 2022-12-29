import random

def gen_area(map, n):
    # area = []
    # best_area = []
    # while len(best_area) == 0:
    #     times = 100
    #     cur_cnt = 0
    #     next_cnt = 0
    #     while times != 0:
    #         area = random.sample(range(n), 4)
    #         area.sort()
    #         if (area[3] - area[1]) <= int(n/3) and (area[2] - area[0]) <= int(n/3):
    #             for i in range(area[0], area[2] + 1):
    #                 for j in range(area[1], area[3] + 1):
    #                     if map[i][j]['mark'] == False:
    #                         next_cnt += 1
    #             if next_cnt > cur_cnt:
    #                 best_area = area.copy()
    #                 cur_cnt = next_cnt
    #             times -= 1
    # return (int(best_area[2]/2 + 1), int(best_area[3]/2 + 1)) 
    # if len(best_area) > 0 else 1
    index = []
    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j]['mark'] == True:
              index.append((i,j))
    sumrow = 0
    sumcol = 0
    for i in range(len(index)):
        sumrow += index[i][0]
        sumcol += index[i][1]
    return (int(sumrow/len(index)), int(sumcol/len(index)))

class Cell:
    def __init__(self, row, col, dist, preStep):
        self.row = row
        self.col = col
        self.dist = dist
        self.preStep = list(preStep)


def AgentFind(array_map, agentPos):
    source = Cell(0, 0, 0, [])

    center = gen_area(array_map, len(array_map))
    print(center)

    # Finding the source to start from
    source.row, source.col = agentPos
    source.preStep.append((source.row, source.col))
    
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
        if (source.row == center[0] and source.col == center[1]):
            return source.preStep

        # moving up
        if isValid(source.row - 1, source.col, array_map, visited):
            nextStep = Cell(source.row - 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append(((nextStep.row, nextStep.col)))
            queue.append(nextStep)
            visited[source.row - 1][source.col] = True

        # moving down
        if isValid(source.row + 1, source.col, array_map, visited):
            nextStep = Cell(source.row + 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            visited[source.row + 1][source.col] = True

        # moving left
        if isValid(source.row, source.col - 1, array_map, visited):
            nextStep = Cell(source.row, source.col - 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            visited[source.row][source.col - 1] = True

        # moving right
        if isValid(source.row, source.col + 1, array_map, visited):
            nextStep = Cell(source.row, source.col + 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            visited[source.row][source.col + 1] = True

    return -1


def isValid(x, y, array_map, visited):
    if ((x >= 0 and y >= 0) and
        (x < len(array_map) and y < len(array_map[0])) and
            (array_map[x][y]['region'] != 0) and ("M" not in array_map[x][y]['type']) and (visited[x][y] == False)):
        return True
    return False

