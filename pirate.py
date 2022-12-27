from hint import *

class Cell:
    def __init__(self, row, col, dist, preStep):
        self.row = row
        self.col = col
        self.dist = dist
        self.preStep = list(preStep)


def minDistance(array_map, type):
    source = Cell(0, 0, 0, [])

    # Finding the source to start from
    treasure = list(*np.argwhere(array_map['type'] == 'Pp'))
    source.row = treasure[0]
    source.col = treasure[1]
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
        if (array_map[source.row][source.col]['type'] == 'T'):
            return source.dist, source.preStep

        # moving up
        if isValid(source.row - 1, source.col, array_map, visited):
            nextStep = Cell(source.row - 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append(((nextStep.row, nextStep.col)))
            queue.append(nextStep)
            #print("up", source.row, source.col)
            visited[source.row - 1][source.col] = True

        # moving down
        if isValid(source.row + 1, source.col, array_map, visited):
            nextStep = Cell(source.row + 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("down", source.row, source.col)
            visited[source.row + 1][source.col] = True

        # moving left
        if isValid(source.row, source.col - 1, array_map, visited):
            nextStep = Cell(source.row, source.col - 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("left", source.row, source.col)
            visited[source.row][source.col - 1] = True

        # moving right
        if isValid(source.row, source.col + 1, array_map, visited):
            nextStep = Cell(source.row, source.col + 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("right", source.row, source.col)
            visited[source.row][source.col + 1] = True

    return -1


def isValid(x, y, array_map, visited):
    if ((x >= 0 and y >= 0) and
        (x < len(array_map) and y < len(array_map)) and
            (array_map[x][y]['region'] != 0) and (array_map[x][y]['type'] != 'M') and (visited[x][y] == False)):
        return True
    return False





def verify_hint6(array_map, type):
    source = Cell(0, 0, 0, [])

    # Finding the source to start from
    for i in range(len(array_map)):
        for j in range(len(array_map[0])):
            if type in array_map[i][j]['type']:
                source.row = i
                source.col = j
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
        if (array_map[source.row][source.col]['type'] == 'T'):
            return source.dist, source.preStep

        # moving up
        if isValidHint6(source.row - 1, source.col, array_map, visited):
            nextStep = Cell(source.row - 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append(((nextStep.row, nextStep.col)))
            queue.append(nextStep)
            #print("up", source.row, source.col)
            visited[source.row - 1][source.col] = True

        # moving down
        if isValidHint6(source.row + 1, source.col, array_map, visited):
            nextStep = Cell(source.row + 1, source.col,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("down", source.row, source.col)
            visited[source.row + 1][source.col] = True

        # moving left
        if isValidHint6(source.row, source.col - 1, array_map, visited):
            nextStep = Cell(source.row, source.col - 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("left", source.row, source.col)
            visited[source.row][source.col - 1] = True

        # moving right
        if isValidHint6(source.row, source.col + 1, array_map, visited):
            nextStep = Cell(source.row, source.col + 1,
                            source.dist + 1, source.preStep)
            nextStep.preStep.append((nextStep.row, nextStep.col))
            queue.append(nextStep)
            #print("right", source.row, source.col)
            visited[source.row][source.col + 1] = True

    return -1


def isValidHint6(x, y, array_map, visited):
    if ((x >= 0 and y >= 0) and
        (x < len(array_map) and y < len(array_map)) and
        (visited[x][y] == False)):
        return True
    return False
