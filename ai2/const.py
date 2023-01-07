INFINITY = 1_000_000_000

# ENTITY
NOTHING = 0
MOUNTAIN = 1
PRISON = 2
TREASURE = 3

ENTITIES = ["","M","P","T"]

# REGION
SEA = 0

# HINT
HINTS_NAME = [
    "A list of random tiles that doesn't contain the treasure (1 to 12)",
    "2-5 regions that 1 of them has the treasure",
    "1-3 regions that do not contain the treasure",
    "A large rectangle area that has the treasure",
    "A small rectangle area that doesn't has the treasure",
    "He tells you that you are the nearest person to the treasure (between you and the prison he is staying)",
    "A column and/or a row that contain the treasure (rare)",
    "A column and/or a row that do not contain the treasure",
    "2 regions that the treasure is somewhere in their boundary",
    'The treasure is somewhere in a boundary of 2 regions',
    'The treasure is somewhere in an area bounded by 2-3 tiles from sea',
    'A half of the map without treasure (rare)',
    'From the center of the map/from the prison that he\'s staying, he tells you a direction that has the treasure (W, E, N, S or SE, SW, NE, NW) (The shape of area when the hints are either W, E, N or S is triangle)',
    '2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares (rare)',
    'The treasure is in a region that has mountain',
    'The treausre is in some circular area of the map'
]

NEGATIVE_HINTS = [1, 3, 5, 8]
NUM_OF_HINTS = 16

NORMAL_WEIGHT = 5
RARE_WEIGHT = 2
VERR_RARE_WEIGHT = 1
NOT_IMPLEMENTED = 0

HINT_WEIGHTS = [
    NOT_IMPLEMENTED, # doesnt exist
    NORMAL_WEIGHT, # 1
    NORMAL_WEIGHT, # 2
    NORMAL_WEIGHT, # 3
    NORMAL_WEIGHT, # 4
    NORMAL_WEIGHT, # 5
    NORMAL_WEIGHT, # 6
    RARE_WEIGHT,   # 7
    NORMAL_WEIGHT, # 8
    NORMAL_WEIGHT, # 9
    NORMAL_WEIGHT, # 10
    NORMAL_WEIGHT, # 11
    RARE_WEIGHT,   # 12
    NORMAL_WEIGHT, # 13
    RARE_WEIGHT,   # 14
    NORMAL_WEIGHT, # 15
    VERR_RARE_WEIGHT  # 16
]

# AGENTS
AGENT = 1
PIRATE = 2

