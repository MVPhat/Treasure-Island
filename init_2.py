import random
from init import *
from agent import Agent
from pirate import Pirate

Ax, Ay = game.random_agent_position(game.MAP)
agent = Agent(width, height, x=Ax, y=Ay)

Px, Py = game.PRISION_LIST[random.randrange(0, game.NUM_OF_PRISON)]
pirate = Pirate(width, height, x=Px, y=Py)
