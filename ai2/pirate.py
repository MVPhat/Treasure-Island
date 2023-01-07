import numpy as np
from init import game

class Pirate:
    def __init__(self, width, height, x, y) -> None:
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.prison = (x, y)
        self.hints = {}
        self.map = self.bfs(x, y)
        self.free = False
        self.reveal = False
        self.step = 0
        self.move_seq = self.get_move_sequence()
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j] = (self.map[i][j] + 1) // 2

    def get_position(self):
        return (self.x, self.y)

    def get_move_sequence(self):
        x, y = game.TREASURE
        seq = []
        while (x, y) != (self.x, self.y):
            for move in game.PIRATE_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if game.good_for_pirate(u, v) and self.map[u][v] == self.map[x][y] - 1:
                    x, y = u, v
                    seq.append((-dx, -dy))
                    break
        seq.reverse()
        return seq

    def bfs(self, pirate_x, pirate_y):
        cost = np.zeros((self.height, self.width)) 
        queue = []
        queue.append((pirate_x, pirate_y))
        i = 0
        while i < len(queue):
            x, y = queue[i]
            for move in game.PIRATE_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if game.good_for_pirate(u, v) and cost[u][v] == 0 and not (u == pirate_x and v == pirate_y):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            i += 1
        return cost

    def make_decision(self):
        self.step += 1
        return self.move_seq[self.step - 1]

    def move(self, dx, dy):
        if not game.good_for_pirate(self.x + dx, self.y + dy):
            return False
        self.x += dx
        self.y += dy
        return True