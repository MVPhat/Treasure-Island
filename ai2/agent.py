# The Agent class is a class that represents the agent. It has a bunch of functions that are used to
# make decisions.
import numpy as np
from const import TREASURE
from const import INFINITY

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

    def process_map(self, height, width):
        """
        It takes in a height and width and returns a 2D array of booleans that are True if the
        corresponding location is good for treasure and False otherwise

        :param height: the height of the map
        :param width: width of the map
        :return: A 2D array of booleans.
        """
        sus = np.ones((height, width), dtype=np.bool_)
        for i in range(height):
            for j in range(width):
                if not game.good_for_treasure(i, j):
                    sus[i][j] = 0
        return sus

    def get_position(self):
        return (self.x, self.y)

    def can_move(self, x, y, dx, dy):
        """
        It returns True if the agent can move from (x, y) to (x + dx, y + dy) without hitting a wall

        :param x: the x coordinate of the agent
        :param y: the y coordinate of the agent
        :param dx: the x-distance to move
        :param dy: the vertical distance to move
        :return: A boolean value.
        """
        sx = -1 if dx < 0 else 1
        sy = -1 if dy < 0 else 1
        dx = abs(dx)
        dy = abs(dy)
        for i in range(dx + 1):
            for j in range(dy + 1):
                u, v = x + sx * i, y + sy * j
                if not game.good_for_agent(u, v):
                    return False
        return True

    def move(self, dx, dy):
        """
        If the player can move, then move the player

        :param dx: The x-coordinate of the direction you want to move in
        :param dy: The change in y
        :return: a boolean value.
        """
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
        found = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                u, v = self.x + i, self.y + j
                if not game.valid(u, v):
                    continue
                self.map[u][v] = 0
                if (u, v) == game.TREASURE:
                    found = True
        return found

    def big_scan(self):
        """
        It scans a 5x5 area around the player, and if the treasure is in that area, it sets the map to 0
        :return: a boolean value.
        """
        found = False
        for i in range(-2, 3):
            for j in range(-2, 3):
                u, v = self.x + i, self.y + j
                if not game.valid(u, v):
                    continue
                self.map[u][v] = 0
                if (u, v) == game.TREASURE:
                    found = True
        return found

    def evaluate_position(self):
        """
        It computes the sum of the shortest distances from each cell to the current position of the
        player
        :return: The heuristic value of the current position.
        """
        cost = np.zeros((self.height, self.width))
        queue = []
        queue.append((self.x, self.y))
        i = 0
        heuristic = 0
        while i < len(queue):
            x, y = queue[i]
            if self.map[x][y]:
                heuristic += cost[x][y]
            for move in game.SHORT_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0 and not (u == self.x and v == self.y):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            for move in game.LONG_MOVES:
                dx, dy = move
                u = x + dx
                v = y + dy
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0 and not (u == self.x and v == self.y):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            i += 1
        return heuristic

    def masking(self, mask, inverse):
        """
        If inverse is true, then the masking function will set the value of the map to the value of the map
        AND NOT the mask. 

        If inverse is false, then the masking function will set the value of the map to the value of the
        map AND the mask. 

        :param mask: a 2D array of booleans, where True means that the corresponding cell is a wall
        :param inverse: if true, the mask will be inverted
        """
        for i in range(self.height):
            for j in range(self.width):
                if inverse:
                    self.map[i][j] = self.map[i][j] and not mask[i][j]
                else:
                    self.map[i][j] = self.map[i][j] and mask[i][j]

    def receive_hint(self, hint):
        self.hints.add(hint)

    def need_verification(self):
        return len(self.hints) != 0

    def evaluate_hint(self, hint, depth):
        """
        It takes a hint and a depth, and returns the average heuristic value of the hint, weighted by the
        number of cells that are still suspicious after applying the hint

        :param hint: the hint to be evaluated
        :param depth: the depth of the look-ahead search
        :return: The heuristic value of the hint.
        """
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
        """
        It finds the best hint to give to the opponent

        :param depth: The depth of the search tree
        :return: The best heuristic and the best hint id.
        """
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
        """
        > If the heuristic of the current action is better than the best heuristic, return the current
        heuristic and action. Otherwise, return the best heuristic and action

        :param heuristic: the heuristic value of the current state
        :param action: the action that the agent is considering taking
        :param best_heuristic: the best heuristic value found so far
        :param best_action: the best action found so far
        :return: The best heuristic and the action that corresponds to it.
        """
        if best_heuristic > heuristic:
            return heuristic, action
        return best_heuristic, best_action

    def look_forward(self, depth):
        """
        > The function looks at all possible actions that the agent can take, and returns the action that
        leads to the best heuristic

        :param depth: the number of actions that have been taken so far in the current turn
        :return: The best heuristic and the best action.
        """
        best_action = ("do nothing")
        best_heuristic = self.evaluate_position()
        if best_heuristic == 0:
            return best_heuristic, best_action

        if depth < game.ACTIONS_IN_TURN:

         # Checking if the hint is needed to be verified. If it is, it will find the best hint and
         # then find the best heuristic.
            if self.need_verification():
                heuristic, hint_id = self.find_best_hint(depth)
                best_heuristic, best_action = self.max_heuristic(
                    heuristic, ("verify", hint_id), best_heuristic, best_action)
                if best_heuristic == 0:
                    return best_heuristic, best_action
            else:
                for move in game.SHORT_MOVES:
                    impostor = Agent(copy=self)
                    dx, dy = move
                    if impostor.move(dx, dy):
                        impostor.small_scan()
                        heuristic, _ = impostor.look_forward(depth + 1)
                        best_heuristic, best_action = self.max_heuristic(
                            heuristic, ("short move", (dx, dy)), best_heuristic, best_action)
                        if best_heuristic == 0:
                            return best_heuristic, best_action

                for move in game.LONG_MOVES:
                    impostor = Agent(copy=self)
                    dx, dy = move
                    if impostor.move(dx, dy):
                        heuristic, _ = impostor.look_forward(depth + 1)
                        best_heuristic, best_action = self.max_heuristic(
                            heuristic, ("long move", (dx, dy)), best_heuristic, best_action)
                        if best_heuristic == 0:
                            return best_heuristic, best_action

                impostor = Agent(copy=self)
                impostor.big_scan()
                heuristic, _ = impostor.look_forward(depth + 1)
                best_heuristic, best_action = self.max_heuristic(
                    heuristic, ("big scan"), best_heuristic, best_action)

        if self.can_tele:
            for row in range(self.height):
                for col in range(self.width):
                    impostor = Agent(copy=self)
                    if impostor.tele(row, col):
                        heuristic, _ = impostor.look_forward(depth)
                        best_heuristic, best_action = self.max_heuristic(
                            heuristic, ("tele", (row, col)), best_heuristic, best_action)
                        if best_heuristic == 0:
                            return best_heuristic, best_action

        return best_heuristic, best_action

    def evaluate_pirate_move(self, new_pirate_x, new_pirate_y):
        """
        The function evaluates the pirate's move by comparing the cost of the new move to the cost of the
        old move. If the new move is better, the function updates the pirate's position and masks the old
        move

        :param new_pirate_x: the x coordinate of the pirate's new position
        :param new_pirate_y: The new y coordinate of the pirate
        :return: the cost of the shortest path from the pirate to the treasure.
        """
        if self.pirate_x == -1 or self.pirate_y == -1:
            self.pirate_x, self.pirate_y = new_pirate_x, new_pirate_y
            return
        old_cost = self.pirate_bfs(self.pirate_x, self.pirate_y)
        new_cost = self.pirate_bfs(new_pirate_x, new_pirate_y)
        mask = np.ones((self.height, self.width))
        for i in range(self.height):
            for j in range(self.width):
                if new_cost[i][j] >= old_cost[i][j]:
                    mask[i][j] = 0
        mask[new_pirate_x][new_pirate_y] = 0
        self.masking(mask, False)
        self.pirate_x, self.pirate_y = new_pirate_x, new_pirate_y

    def pirate_bfs(self, pirate_x, pirate_y):
        """
        It takes in the coordinates of a pirate and returns a matrix of the same size as the board, where
        each cell contains the minimum number of moves required to reach that cell from the pirate

        :param pirate_x: the x coordinate of the pirate
        :param pirate_y: The y coordinate of the pirate
        :return: The cost of the shortest path from the pirate to every other cell in the grid.
        """
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
                if self.can_move(x, y, dx, dy) and cost[u][v] == 0 and not (u == pirate_x and v == pirate_y):
                    cost[u][v] = cost[x][y] + 1
                    queue.append((u, v))
            i += 1
        return cost

    def bad_hint(self, hint):
        """
        > If the hint is a bad hint, then the agent will not change his belief

        :param hint: the hint that was given
        :return: The number of suspects that are still possible after the hint is applied.
        """
        MrPositive = Agent(copy=self)
        MrPositive.masking(hint.map['contains'], False)
        sus = np.sum(MrPositive.map)
        return sus == 0 or sus == np.sum(self.map)

    def discard_bad_hints(self):
        """
        If a hint is bad, add it to a list of bad hints. 

        Then, for each hint in the list of bad hints, remove it from the set of hints. 

        The function `bad_hint` is defined in the next cell.
        """
        bad_hints = []
        for hint in self.hints:
            if self.bad_hint(hint):
                bad_hints.append(hint)
        for hint in bad_hints:
            self.hints.discard(hint)

    def make_decision(self, depth):
        """
        > If there are any hints that are impossible to satisfy, discard them. Then, look forward a
        certain number of steps and return the action that maximizes the heuristic

        :param depth: How many turns to look ahead
        :return: The action that the agent should take.
        """
        self.discard_bad_hints()
        heuristic, action = self.look_forward(depth)
        return action

    def process_hint(self, hint, inverse):
        """
        > If the hint is not an inverse, then we mask the hint's map's contains key

        :param hint: the hint object
        :param inverse: True if the hint is negated, False otherwise
        """
        self.masking(hint.map['contains'], inverse)
        self.hints.discard(hint)
