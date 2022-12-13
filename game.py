# holds the gamelogic and gameloop
import random

# board is represented by array of 40 fields, index will keep track of loop
class Board:
    def __init__(self):
        self.board = [0] * 40

    # piece moved from to
    def moveFromTo(self, start, end):
        if end >= 40:
            end -= 40
        if self.board[end] != 0:
            self.board[end].knocked()
        self.board[end] = self.board[start]
        self.board[start].setSpace(end)
        self.board[start] = 0

    # player enters piece into play
    def enterPiece(self, player, piece):
        playerEntry = 10 * (player.color - 1) + 1
        if self.board[playerEntry] != 0:
            self.board[playerEntry].knocked()
        self.board[playerEntry] = piece
        piece.setSpace(playerEntry)

    # player takes piece out of play
    def leavePiece(self, piece, target):
        self.board[piece.space] = 0
        piece.setSpace(target)


# pieces keep track on where on the board they are. if they havent entered the board they are on space 0,
# if they have reached the safe spaces they are on -1, -2, -3 or -4
class Piece:
    def __init__(self):
        self.space = 0
    def setSpace(self, space):
        self.space = space

    # piece was knocked out
    def knocked(self):
        self.space = 0

# color of player is encoded by enumeration from 1 through 4
class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = [Piece(), Piece(), Piece(), Piece()]
        self.entryEmpty = True

def rollDice():
    return random.randrange(1, 7)

# checks if player is finished
def finishedCheck(player):
    finished = True
    for piece in player.pieces:
        if piece.space >= 0:
            finished = False
    return finished

# checks if player has a piece in the base
def baseCheck(player):
    for piece in player.pieces:
        if piece.space == 0:
            return True
    return False

# TODO: calculates legal moves, moves consist of piece moved and resulting board state
def legalMoves(board, player, roll):
    moves = []
    for piece in player.pieces:
        pass

    return moves

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

def playGame():
    players = [Player(1), Player(2), Player(3), Player(4)]
    current = players[determineFirst() - 1]
    board = Board()
    while stillPlaying(players):
        roll = rollDice()
        moves = legalMoves(board, current, roll)
        # TODO: chose which move to perform based on agents
        chosenMove = None
        board = chosenMove[1]
        current = players[current.color % 4]

def stillPlaying(players):
    playingCount = 0
    for player in players:
        if not finishedCheck(player):
            playingCount += 1
    if playingCount > 1:
        return True
    else:
        return False

