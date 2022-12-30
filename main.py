from visualization import Visualization
from hint import Hint
import numpy as np
import random
import time
from pirate import minDistance
from agent import AgentFind
from agent import Agent

EXAMPLE_FILE = "MAP_0.txt"
TEST_CASE = "LOG_0.txt"


def readInputFile(filename):
    with open(filename, "r") as f:
        # - The first line contains 2 numbers to represent the size of the map (𝑾 and 𝑯).
        width, height = f.readline().split(" ")
        # - The second line is the turn number that the pirate reveals the prison (𝒓).
        reveals = f.readline().split(" ")
        # - The third line is the turn number that the pirate is free and start running to the
        # treasure. (𝒇).
        free = f.readline().split(" ")
        # - The fourth line is the number of regions on the map (including the sea) (𝑹).
        regions = f.readline().split(" ")
        # - The fifth line contains 2 numbers to represent the treasure position (𝑻𝒙, 𝑻𝒚)
        Tx, Ty = f.readline().split(" ")
        # - The next H lines are the H rows of a map
        map = []
        for i in range(int(height)):
            map.append(f.readline().split(";"))
        for i in range(int(height)):
            for j in range(int(width)):
                map[i][j] = (int(map[i][j][0]), '' if map[i][j][1] ==
                             "\n" or map[i][j][1] == "" else map[i][j][1], False, 1)
    map = np.array(map, dtype=[
                   ('region', np.short), ('type', 'U4'), ('mark', np.bool_), ('ratio', np.short)])
    return (int(width), int(height)), int(reveals[0]), int(free[0]), regions, (int(Tx), int(Ty)), map


HINTS_NAME = [
    (1, "A list of random tiles that doesn't contain the treasure (1 to 12)"),
    (2, "2-5 regions that 1 of them has the treasure"),
    (3, "1-3 regions that do not contain the treasure"),
    (4, "A large rectangle area that has the treasure"),
    (5, "A small rectangle area that doesn't has the treasure"),
    (6, "He tells you that you are the nearest person to the treasure (between you and the prison he is staying)"),
    (7, "A column and/or a row that contain the treasure (rare)"),
    (8, "A column and/or a row that do not contain the treasure"),
    (9, "2 regions that the treasure is somewhere in their boundary"),
    (10, 'The treasure is somewhere in a boundary of 2 regions'),
    (11, 'The treasure is somewhere in an area bounded by 2-3 tiles from sea'),
    (12, 'A half of the map without treasure (rare)'),
    (13, 'From the center of the map/from the prison that he\'s staying, he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW) (The shape of area when the hints are either W, E, N or S is triangle)'),
    (14, '2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares (rare)'),
    (15, 'The treasure is in a region that has mountain'),
]

# print(minDistance(map, 'p'))

# The agent has 2 action each turn, the available action:
# o Verification, verify a hint is a truth or a liar.
# o Move straight 1-2 steps in a direction then perform a
# small scan.
# o Move straight 3-4 steps in a direction.
# o Stay and perform a large scan.


turn = 0

(width, height), reveal, free, region, (Tx, Ty), map = readInputFile(EXAMPLE_FILE)

# random 1 prison
prison_list = list(zip(*np.argwhere(map['type'] == 'P')))
ranIdx = random.randint(0, len(prison_list[0]) - 1)
map[prison_list[0][ranIdx]][prison_list[1][ranIdx]]['type'] += 'p'

piratePos = (prison_list[0][ranIdx], prison_list[1][ranIdx])

isWin = False
line = 0
list_log = []

while True:
    Ax = random.randint(0, width-1)
    Ay = random.randint(0, height-1)
    if not (map[Ax][Ay]['type'] == 'P' or map[Ax][Ay]['type'] == 'M' or map[Ax][Ay]['region'] == 0):
        break

agent = Agent(Ax, Ay, map)

while True:
    turn += 1

    print(f'TURN [{turn}]')
    list_log.append(f'TURN [{turn}]')
    line += 1

    visual = Visualization(width=width, height=height, map=map)

    visual.clear_mark()

    if (len(HINTS_NAME) == 0):
        print(f'\t\tHINT [empty]')
        break

    if turn == reveal:
        print(f"\tPIRATE [reveal]: {reveal == turn}")
        list_log.append(f"\tPIRATE [reveal]: {reveal == turn}")
        line += 1

    if turn >= free:
        if turn == free:
            print(f"\tPIRATE [free]: {free == turn}")
            list_log.append(f"\tPIRATE [free]: {free == turn}")
            line += 1
            _, pirateMoves = minDistance(map, 'p')

        Px, Py = piratePos
        map[Px][Py]['type'] = map[Px][Py]['type'][:-1]
        map[Px][Py]['ratio'] = 0

        # pirate move
        PIRATE_STEP = 2 if len(pirateMoves) > 1 else 1
        if PIRATE_STEP == 2:
            Px, Py = pirateMoves[1]
            map[Px][Py]['ratio'] = 0
        pirateMoves = pirateMoves[PIRATE_STEP:]

        if (np.all((Tx, Ty) == piratePos) or len(pirateMoves) == 0):
            map[Tx][Ty]['type'] += 'p'
            print("\tPIRATE [win]")
            list_log.append("\tPIRATE [win]")
            line += 1
            break

        piratePos = pirateMoves[0]

        Px, Py = piratePos
        map[Px][Py]['ratio'] = 0
        map[Px][Py]['type'] += 'p'

    print(
        f"\tPIRATE [pos]: {piratePos} ")
    list_log.append(f"\tPIRATE [pos]: {piratePos} ")
    line += 1

    hint = random.randint(1, len(HINTS_NAME))
    num, name = HINTS_NAME[hint - 1]

    if (turn == 1):

        while True:
            hint = Hint(map, width, hint=f'h{num}')
            hint.visualize(test=True, turn=turn)
            res, list_log, line = hint.verify(
                test=True, turn=turn, list_log=list_log, line=line)
            # print('==> Test hint', num, res)

            if (res):
                break
            else:
                hint = random.randint(1, len(HINTS_NAME))
                num, name = HINTS_NAME[hint - 1]
    else:
        hint = Hint(map, width, hint=f'h{num}')
        hint.visualize(turn=turn)

        # time.sleep(15)
        # if (hint_verify):

    print(f'\t\tHINT [{num}][name]: {name}')
    list_log.append(f'\t\tHINT [{num}][name]: {name}')
    # print(visual.map[visual.map['mark']])

    print(f'\tAGENT [pos]: ({agent.Ax}, {agent.Ay})')
    list_log.append(f'\tAGENT [pos]: ({agent.Ax}, {agent.Ay})')
    line += 2

    agent.updateMap(map)

    map = agent.updateAgentPos(agent.Ax, agent.Ay)

    for i in range(2):
        print(f"\tAGENT [action][{i+1}]")
        list_log.append(f"\tAGENT [action][{i+1}]")
        action = agent.get_best_action(hint=hint, turn=turn)

        direction = agent.get_best_direction(map=hint.map)

        if action == 'move':
            agent.agentMove(direction)
        elif action == 'big_scan':
            agent.agentScan('big')
        elif action == 'teleport':
            (teleX, teleY) = agent.get_best_Teleport()
            map = agent.updateAgentPos(teleX, teleY)
        elif action == 'verify':
            line += 1
            _, list_log, line = hint.verify(
                turn=turn, list_log=list_log, line=line)
        # if (turn == reveal):
        #     map[x][y]['type'] = map[x][y]['type'][:-1]
        #     x = prison_list[0][ranIdx]
        #     y = prison_list[1][ranIdx]
        #     print(f'\tAGENT [action]: TELEPORT to ({x}, {y})')
        #     print(f'\tAGENT [pos]: ({x}, {y})')

    map = hint.map
    # HINTS_NAME.remove((num, name))

    # print(AgentFind(map, (Ax, Ay)))


def save_file_log():
    f = open(TEST_CASE, 'w')
    f.write(str(line) + '\n')
    if isWin:
        f.write("WIN\n")
    else:
        f.write("LOSE\n")
    for i in list_log:
        f.write(i + '\n')

    f.close()


save_file_log()
