import random

def gen_area(map, n):
    isTreasure = False
    area = []
    while isTreasure == False:
        area = random.sample(range(n), 4)
        area.sort()
        if (area[3] - area[1]) <= int(n/3) and (area[2] - area[0]) <= int(n/3):
            for i in range(area[0], area[2] + 1):
                for j in range(area[1], area[3] + 1):
                    if 'T' in map[i][j]['type']:
                        isTreasure = True
    return (int(area[2]/2 + 1), int(area[3]/2 + 1))

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

