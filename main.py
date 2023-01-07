import numpy as np
from const import *
from init import *
from init_2 import *
from hint import Hint
from visualization import Visualization
import random
import sys


def agent_win(scan):
    if scan == "small":
        return agent.small_scan()
    elif scan == "big":
        return agent.big_scan()
    else:
        return agent.get_position() == game.TREASURE


def pirate_win():
    return pirate.get_position() == game.TREASURE


def game_loop():
    np.set_printoptions(threshold=sys.maxsize)
    visualization.map['ratio'] &= agent.map
    visualization.visualize()

    log = []

    turn = 1

    hints = []

    while True:
        hint_number = random.choices(
            range(NUM_OF_HINTS+1), weights=game.HINT_WEIGHTS, k=1)[0]
        while hint_number == 6:
            hint_number = random.choices(
                range(NUM_OF_HINTS+1), weights=game.HINT_WEIGHTS, k=1)[0]

        hint = Hint(hint_number, 0)
        if hint.truthness() == True:
            hints.append(hint)
            agent.process_hint(hint, inverse=False)
            if hint_number == 10 or hint_number == 11:
                game.HINT_WEIGHTS[hint_number] = 0
            break

    hint_6 = []

    log.append(f"\nGIVE HINT: {hint.hint}")
    log.append(f"\n{HINTS_NAME[hint.hint-1]}")
    log.append(f"\n{hint.log}")
    print(f"GIVE HINT: {hint.hint}")
    print(f"{HINTS_NAME[hint.hint-1]}")
    print(f"{hint.log}")
    
    visualization.map['ratio'] &= agent.map
    visualization.map['mark'] = hint.map['mark']
    visualization.visualize()

    while True:
        # Agent turn
        Tx, Ty = game.TREASURE
        if agent.map[Tx][Ty] == False:
            print("ERROR")
            input()
        log.append(f"\nTURN {turn}:")
        log.append("\nAGENT TURN:")
        print(f"TURN {turn}:")
        print("AGENT TURN:")
        for i in range(game.ACTIONS_IN_TURN):
            print("Calculating", end=' ')
            start_time = time.time()
            action = agent.make_decision(i)
            print(time.time() - start_time)
            print(turn, action)
            scan = "no"
            if action[0] == "tele":
                x, y = action[1]
                agent.tele(x, y)
                log.append(f"\nTELEPORT: {x}, {y}")
            elif action[0] == "verify":
                hint_id = action[1]
                hint = hints[hint_id]
                agent.process_hint(hint, inverse=not hint.truthness())
                log.append(f"\nVERIFY: HINT {hint_id}")
            elif action[0] == "short move":
                dx, dy = action[1]
                agent.move(dx, dy)
                x, y = agent.get_position()
                scan = "small"
                log.append(
                    f"\nSHORT MOVE AND SMALL SCAN: {dx}, {dy} | NEW POSITION: {x}, {y}")
            elif action[0] == "long move":
                dx, dy = action[1]
                agent.move(dx, dy)
                x, y = agent.get_position()
                log.append(f"\nLONG MOVE: {dx}, {dy} | NEW POSITION: {x}, {y}")
            elif action == "big scan":
                scan = "big"
                log.append(f"\nBIG SCAN")

            visualization.map['ratio'] &= agent.map

            if agent_win(scan):
                log.append("WIN")
                print("WIN")
                visualization.visualize()
                return log

        # Pirate turn
        free = turn >= game.FREE_TURN
        reveal = turn >= game.REVEAL_TURN
        first_reveal = turn == game.REVEAL_TURN
        first_free = turn == game.FREE_TURN

        log.append("\nPIRATE TURN")
        print("PIRATE TURN")

        if first_reveal:
            pirate.reveal = True
            Px, Py = pirate.get_position()
            log.append(f"\nPIRATE REVEALED: {Px}, {Py}")
            agent.evaluate_pirate_move(new_pirate_x=Px, new_pirate_y=Py)
            for hint in hint_6:
                agent.receive_hint(hint)
            hint_6.clear()

        if free:
            print("PREPARE MOVE")
            if first_free:
                pirate.free = True
                log.append(f"\nPIRATE FREED: {Px}, {Py}")

            for i in range(game.ACTIONS_IN_TURN):
                dx, dy = pirate.make_decision()
                pirate.move(dx, dy)
                Px, Py = pirate.get_position()
                log.append(f"\nMOVE: {dx}, {dy} | NEW POSITION {Px}, {Py}")
                print(f"MOVE: {dx}, {dy} | NEW POSITION {Px}, {Py}")
                if pirate_win():
                    visualization.visualize()
                    log.append("LOST")
                    print("LOST")
                    return log
                agent.evaluate_pirate_move(new_pirate_x=Px, new_pirate_y=Py)

        # Pirate gives hint
        print("PREPARE HINT")

        hint_number = random.choices(
            range(NUM_OF_HINTS+1), weights=game.HINT_WEIGHTS, k=1)[0]
        hint = Hint(hint_number, turn)

        if hint_number == 10:
            game.HINT_WEIGHTS[hint_number] = 0

        hints.append(hint)

        if hint.hint == 6 and not reveal:
            hint_6.append(hint)
        else:
            agent.receive_hint(hint)

        print("Visualizing", end=" ")
        start_time = time.time()
        visualization.map['mark'] = hint.map['mark']
        visualization.visualize()
        print(time.time() - start_time)

        log.append(f"\nGIVE HINT: {hint.hint}")
        log.append(f"\n{HINTS_NAME[hint.hint-1]}")
        log.append(f"\n{hint.log}")
        print(f"GIVE HINT: {hint.hint}")
        print(f"{HINTS_NAME[hint.hint-1]}")
        print(f"{hint.log}")
        turn += 1


if __name__ == "__main__":
    visualization = Visualization(width, height)

    log = game_loop()
    save_file_log(log)
