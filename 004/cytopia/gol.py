#!/usr/bin/env python3
"""
The Game of Life.

Python3 implementation of the Game of Life.
"""

# -------------------------------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------------------------------
import copy
import random
import sys
import time


# -------------------------------------------------------------------------------------------------
# GLOBALS
# -------------------------------------------------------------------------------------------------
# WIDTH = 110
# HEIGHT = 29
WIDTH = 15
HEIGHT = 15
DEAD = " "
ALIVE = "*"
# ALIVE = "█"
SHOW_COUNT = False

BASELINE = 2
DELAY = 0.1


# -------------------------------------------------------------------------------------------------
# GAME FUNCTIONS
# -------------------------------------------------------------------------------------------------
def create_field(width, height, baseline=1):
    """Get a random populated field."""
    # 25 % alive
    if baseline == 1:
        return [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
    # 12.5 % alive
    elif baseline == 2:
        return [
            [random.randint(0, random.randint(0, 1)) for _ in range(width)] for _ in range(height)
        ]
    # 6.25 % alive
    elif baseline == 2:
        return [
            [random.randint(0, random.randint(0, random.randint(0, 1))) for _ in range(width)]
            for _ in range(height)
        ]
    # 3.125 % alive
    if baseline == 3:
        return [
            [
                random.randint(0, random.randint(0, random.randint(0, random.randint(0, 1))))
                for _ in range(width)
            ]
            for _ in range(height)
        ]
    # 1.5625 % alive
    else:
        return [
            [
                random.randint(
                    0, random.randint(0, random.randint(0, random.randint(0, random.randint(0, 1))))
                )
                for _ in range(width)
            ]
            for _ in range(height)
        ]


def print_field(field, dead=" ", alive="█", show_count=False):
    """Display the current field."""
    print("+%s+" % ("-" * len(field[0])))
    for x, valx in enumerate(field):
        print("|", end="")
        for y, valy in enumerate(field[x]):
            if show_count:
                print("%s" % (field[x][y] if field[x][y] > 0 else dead), end="")
            else:
                print("%s" % (alive if field[x][y] > 0 else dead), end="")
        print("|")
    print("+%s+" % ("-" * len(field[0])))


def step(field):
    """Run one iteration over the field."""
    count_alives = 0
    for x, valx in enumerate(field):
        for y, valy in enumerate(field[x]):
            # Get number of neighbours
            neighbours = count_neighbours(field, x, y)

            # Cell is currently alive
            if field[x][y] > 0:
                # Allowed to stay alive
                if neighbours in [2, 3]:
                    field[x][y] = 1
                # Over or under population
                else:
                    field[x][y] = 0
            else:
                # Respawn dead cell
                if neighbours == 3:
                    field[x][y] = 1

            # Instead of setting '1' to an alive cell, add the count of neighouring cells,
            # so we can alternatively display the neighbour count of a cell instead of its symbol.
            if field[x][y] == 1:
                field[x][y] = neighbours
                count_alives += 1

    return count_alives


def count_neighbours(field, x, y):
    """Count neighbours of current cell."""
    neighbours = 0

    # Count three cells above
    try:
        if field[x - 1][y - 1] > 0:
            neighbours += 1
    except IndexError:
        pass
    try:
        if field[x][y - 1] > 0:
            neighbours += 1
    except IndexError:
        pass
    try:
        if field[x + 1][y - 1] > 0:
            neighbours += 1
    except IndexError:
        pass

    # Count three cells below
    try:
        if field[x - 1][y + 1] > 0:
            neighbours += 1
    except IndexError:
        pass
    try:
        if field[x][y + 1] > 0:
            neighbours += 1
    except IndexError:
        pass
    try:
        if field[x + 1][y + 1] > 0:
            neighbours += 1
    except IndexError:
        pass

    # Count two cells: left and right
    try:
        if field[x - 1][y] > 0:
            neighbours += 1
    except IndexError:
        pass
    try:
        if field[x + 1][y] > 0:
            neighbours += 1
    except IndexError:
        pass

    return neighbours


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------
def main():
    """Start the program."""
    field = create_field(WIDTH, HEIGHT, BASELINE)
    tmp = list()
    rounds = 0
    stuck = False

    print_field(field, dead=DEAD, alive=ALIVE, show_count=SHOW_COUNT)

    while True:
        time.sleep(DELAY)

        # Iterate: returns num of alives and alters field
        alives = step(field)

        # Show the field
        print_field(field, dead=DEAD, alive=ALIVE, show_count=SHOW_COUNT)
        rounds += 1

        # If the field looks like the previous iteration, end the game
        if tmp == field:
            stuck = True
            break
        # If there are no more alive cells, end the game
        if alives == 0:
            break

        # Create a copy of the last field for comparisson during the next round
        tmp = copy.deepcopy(field)

    if stuck:
        print("Genration lived for %d rounds and got stuck." % (rounds))
    else:
        print("Genration lived for %d rounds and died." % (rounds))


if __name__ == "__main__":
    # Catch Ctrl+c and exit silently without visible exception.
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
