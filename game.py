# holds the gamelogic and gameloop
import random

# board is represented by array of 40 fields, index will keep track of loop
class Board:
    def __init__(self):
        self.board = [0] * 40

# color of player is encoded by enumeration from 1 through 4
class Player:
    def __init__(self, color):
        self.color = color
        self.baseCount = 4
        self.entryEmpty = True
        self.home = [0, 0, 0, 0]

def rollDice():
    return random.randrange(1, 7)

# determine who is the first to move. Yes this could just be done by drawing a random number
def determineFirst():
    first = 0
    highestRoll = 0
    # assume that there are always 4 players
    for i in range(1, 5):
        roll = rollDice()
        # tiebreaker where both roll until one has a higher roll than the other
        if roll == highestRoll:
            deff = 0
            atck = 0
            while deff == atck:
                deff = rollDice()
                atck = rollDice()
                if atck > deff:
                    first = i
                    highestRoll = roll
        elif roll > highestRoll:
            highestRoll = roll
            first = i

    return first
