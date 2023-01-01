import numpy as np
from const import TREASURE
from const import INFINITY
import math
from init import game

class Agent:
    def __init__(self, width=None, height=None, x=None, y=None, copy=None) -> None:
        if copy != None:
            self.width = copy.width
            self.height = copy.height
            self.x = copy.x
            self.y = copy.y
            self.hints = copy.hints.copy()
            self.map = np.copy(copy.map)
            self.can_tele = copy.can_tele
            self.pirate_x = copy.pirate_x
            self.pirate_y = copy.pirate_y
            self.THRESH_HOLD = copy.THRESH_HOLD
        else:
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.hints = set()
            self.map = self.process_map(height, width)
            self.can_tele = 1
            self.pirate_x = -1
            self.pirate_y = -1
            self.THRESH_HOLD = min(64, int(math.sqrt(self.width * self.height)))

    def process_map(self, height, width):
        sus = np.ones((height, width), dtype=np.bool_)
        for i in range(height):
            for j in range(width):
                if not game.good_for_treasure(i, j):
                    sus[i][j] = 0
        return sus

    def get_position(self):
        return (self.x, self.y)

    def can_move(self, x, y, dx, dy):
        u = x + dx
        v = y + dy
        if not game.valid(u, v):
            return False
        if u < x:
            u, x = x, u
        if v < y:
            v, y = y, v
        return not game.BAD_FOR_AGENT[x: u+1, y: v+1].any()

    def move(self, dx, dy):
        if not self.can_move(self.x, self.y, dx, dy):
            return False
        self.x += dx
        self.y += dy
        self.map[self.x][self.y] = 0
        return True

    def tele(self, x, y):
        if not self.can_tele:
            return False
        if not game.good_for_agent(x, y):
            return False
        self.tele = False
        self.x = x
        self.y = y
        self.map[self.x][self.y] = 0

    def small_scan(self):
        Tx, Ty = game.TREASURE
        found = (self.x - 1 <= Tx and Tx <= self.x + 1) and (self.y - 1 <= Ty and Ty <= self.y + 1)
        mX = max(0, self.x - 1)
        MX = min(self.height, self.x + 2)
        mY = max(0, self.y - 1)
        MY = min(self.width, self.y + 2)
        self.map[mX:MX, mY:MY] = 0
        return found

    def big_scan(self):
        Tx, Ty = game.TREASURE
        found = (self.x - 2 <= Tx and Tx <= self.x + 2) and (self.y - 2 <= Ty and Ty <= self.y + 2)
        mX = max(0, self.x - 2)
        MX = min(self.height, self.x + 3)
        mY = max(0, self.y - 2)
        MY = min(self.width, self.y + 3)
        self.map[mX:MX, mY:MY] = 0
        return found

    def agent_bfs(self, Ax, Ay):
        cost = np.zeros((self.height, self.width), dtype=np.int32)
        queue = []
        queue.append((Ax, Ay))
        i = 0
        heuristic = 0
        while i < len(queue):
            x, y = queue[i]
            for move in game.SHORT_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0 and not (u == Ax and v == Ay):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            for move in game.LONG_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0 and not (u == Ax and v == Ay):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            i += 1
        return cost

    def evaluate_position(self):
        if np.sum(self.map) <= self.THRESH_HOLD:
            heuristic = 0
            for x, y in np.argwhere(self.map == True):
                if not (x, y) in game.CACHE.keys():
                    cost = self.agent_bfs(x, y)
                    game.CACHE[(x, y)] = cost
                heuristic += game.CACHE[(x, y)][self.x][self.y]
            return heuristic
        if not self.get_position() in game.CACHE.keys():
            cost = self.agent_bfs(self.x, self.y)
            game.CACHE[self.get_position()] = cost
        return np.sum(np.multiply(self.map, game.CACHE[self.get_position()]))

    def masking(self, mask, inverse):
        if inverse:
            self.map &= (~mask)
        else:
            self.map &= mask
        
    def receive_hint(self, hint):
        self.hints.add(hint)

    def need_verification(self):
        return len(self.hints) != 0

    def evaluate_hint(self, hint, depth):
        MrPositive = Agent(copy=self)
        MrNegative = Agent(copy=self)
        MrPositive.masking(hint.map['contains'], False)
        MrNegative.masking(hint.map['contains'], True)
        sus_1 = np.sum(MrPositive.map)
        sus_2 = np.sum(MrNegative.map)
        if sus_1 == 0 or sus_2 == 0:
            return INFINITY
        MrPositive.hints.discard(hint)
        MrNegative.hints.discard(hint)
        heuristic_1, _ = MrPositive.look_forward(depth + 1)
        heuristic_2, _ = MrNegative.look_forward(depth + 1)
        
        
        return (heuristic_1 * sus_1 + heuristic_2 * sus_2) / (sus_1 + sus_2)

    def find_best_hint(self, depth):
        best_heuristic, best_hint_id = -1, -1
        for hint in self.hints:
            if len(self.hints) == 1:
                return 0, hint.id
            heuristic = self.evaluate_hint(hint, depth)
            if best_heuristic == -1 or best_heuristic > heuristic:
                best_heuristic = heuristic
                best_hint_id = hint.id
        return best_heuristic, best_hint_id
            
    def max_heuristic(self, heuristic, action, best_heuristic, best_action):
        if best_heuristic > heuristic:
            return heuristic, action
        return best_heuristic, best_action

    def look_forward(self, depth):
        best_action = ("do nothing")
        best_heuristic = INFINITY

        if depth < game.ACTIONS_IN_TURN:
            if self.need_verification():
                heuristic, hint_id = self.find_best_hint(depth)
                best_heuristic, best_action = self.max_heuristic(heuristic, ("verify", hint_id), best_heuristic, best_action)
                return best_heuristic, best_action
            
            impostor = Agent(copy=self)
            impostor.big_scan()
            heuristic, _ = impostor.look_forward(depth + 1)
            best_heuristic, best_action = self.max_heuristic(heuristic, ("big scan"), best_heuristic, best_action)
            if best_heuristic == 0:
                return best_heuristic, best_action

            for move in game.SHORT_MOVES:
                impostor = Agent(copy=self)
                dx, dy = move
                if impostor.move(dx, dy):
                    impostor.small_scan()
                    heuristic, _ = impostor.look_forward(depth + 1)
                    best_heuristic, best_action = self.max_heuristic(heuristic, ("short move", (dx, dy)), best_heuristic, best_action)
                    if best_heuristic == 0:
                        return best_heuristic, best_action
            
            for move in game.LONG_MOVES:
                impostor = Agent(copy=self)
                dx, dy = move
                if impostor.move(dx, dy):
                    heuristic, _ = impostor.look_forward(depth + 1)
                    best_heuristic, best_action = self.max_heuristic(heuristic, ("long move", (dx, dy)), best_heuristic, best_action)
                    if best_heuristic == 0:
                        return best_heuristic, best_action
        
        if self.can_tele:
            for row in range(self.height):
                for col in range(self.width):
                    impostor = Agent(copy=self)
                    if impostor.tele(row, col):
                        heuristic, _ = impostor.look_forward(depth)
                        best_heuristic, best_action = self.max_heuristic(heuristic, ("tele", (row, col)), best_heuristic, best_action)
                        if best_heuristic == 0:
                            return best_heuristic, best_action
        
        if best_heuristic == INFINITY:
            best_heuristic = self.evaluate_position()

        return best_heuristic, best_action
    
    def evaluate_pirate_move(self, new_pirate_x, new_pirate_y):
        if self.pirate_x == -1 or self.pirate_y == -1:
            self.pirate_x, self.pirate_y = new_pirate_x, new_pirate_y
            return
        mask = self.pirate_bfs(new_pirate_x, new_pirate_y)
        self.masking(mask, False)
        self.pirate_x, self.pirate_y = new_pirate_x, new_pirate_y

    def pirate_bfs(self, pirate_x, pirate_y):
        cost = np.zeros((self.height, self.width), dtype=np.int32) 
        queue = []
        queue.append((self.pirate_x, self.pirate_y, 2))
        cost[self.pirate_x][self.pirate_y] = 2
        queue.append((pirate_x, pirate_y, 1))
        cost[pirate_x][pirate_y] = 1
        i = 0
        while i < len(queue):
            x, y, z = queue[i]
            for move in game.PIRATE_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0:
                    cost[u][v] = z
                    queue.append((u, v, z))
            i += 1
        mask = (cost == 1)
        return mask

    def bad_hint(self, hint):
        MrPositive = Agent(copy=self)
        MrPositive.masking(hint.map['contains'], False)
        sus = np.sum(MrPositive.map)
        return sus == 0 or sus == np.sum(self.map)

    def discard_bad_hints(self):
        bad_hints = []
        for hint in self.hints:
            if self.bad_hint(hint):
                bad_hints.append(hint)
        for hint in bad_hints:
            self.hints.discard(hint)

    def make_decision(self, depth):
        self.discard_bad_hints()
        heuristic, action = self.look_forward(depth)
        return action
        
    def process_hint(self, hint, inverse):
        self.masking(hint.map['contains'], inverse)
        Tx, Ty = game.TREASURE
        self.hints.discard(hint)