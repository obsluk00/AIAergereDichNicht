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
        playerEntry = 10 * (player.color - 1)
        if self.board[playerEntry] != 0:
            self.board[playerEntry].knocked()
        self.board[playerEntry] = piece
        piece.setSpace(playerEntry)

    # player takes piece out of play
    def leavePiece(self, piece):
        self.board[piece.space] = 0
        piece.setSpace(-1)

    def toString(self):
        rep = "    " + str(self.board[8]) + str(self.board [9]) + str(self.board[10]) + "    \n" \
              "    " + str(self.board[7]) + " " + str(self.board[11]) + "    \n" \
              "    " + str(self.board[6]) + " " + str(self.board[12]) + "    \n" \
              "    " + str(self.board[5]) + " " + str(self.board[13]) + "    \n" \
              + str(self.board[0]) + str(self.board[1]) + str(self.board[2]) + str(self.board[3]) + str(self.board[4]) + " " + str(self.board[14]) + str(self.board[15]) + str(self.board[16]) + str(self.board[17]) + str(self.board[18]) + "\n" \
              + str(self.board[39]) + "         " + str(self.board[19]) + "\n" \
              + str(self.board[38]) + str(self.board[37]) + str(self.board[36]) + str(self.board[35]) + str(self.board[34]) + " " + str(self.board[24]) + str(self.board[23]) + str(self.board[22]) + str(self.board[21]) + str(self.board[20]) + "\n" \
              "    " + str(self.board[33]) + " " + str(self.board[25]) + "    \n" \
              "    " + str(self.board[32]) + " " + str(self.board[26]) + "    \n" \
              "    " + str(self.board[31]) + " " + str(self.board[27]) + "    \n" \
              "    " + str(self.board[30]) + str(self.board[29]) + str(self.board[28]) + "    \n"

        return rep

# pieces keep track on where on the board they are. if they havent entered the board they are on space "base",
# if they have reached the safe spaces they are on -1
class Piece:
    def __init__(self, color):
        self.space = "base"
        self.color = color

    def __str__(self):
        return str(self.color)

    def setSpace(self, space):
        self.space = space

    # piece was knocked out
    def knocked(self):
        self.space = "base"
        print("knocked!")

# color of player is encoded by enumeration from 1 through 4
class Player:
    def __init__(self, color, strategy):
        self.color = color
        self.strategy = strategy
        self.pieces = [Piece(color), Piece(color), Piece(color), Piece(color)]
        self.base = [0, 0, 0, 0]

def rollDice():
    return random.randrange(1, 7)

# checks if player is finished
def finishedCheck(player):
    for piece in player.pieces:
        if piece.space == "base":
            return False
        if piece.space >= 0:
            return False
    return True

# checks if player has a piece in the base
def baseCheck(player):
    for piece in player.pieces:
        if piece.space == "base":
            return True
    return False

# calculates legal moves, moves consist of piece moved
def legalMoves(board, player, roll):
    moves = []
    entry = (player.color - 1) * 10
    baseEntry = (player.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39

    if finishedCheck(player):
        return moves

    # piece needs to enter if possible
    if baseCheck(player) and roll == 6 and (board.board[entry] == 0 or board.board[entry].color != player.color):
        for piece in player.pieces:
            if piece.space == "base":
                moves.append(piece)
                return moves

    # pieces on entry must move if other pieces are still in base
    if baseCheck(player) and board.board[entry] != 0 and board.board[entry].color == player.color:
        for piece in player.pieces:
            if piece.space == entry and canMove(board, piece, player, roll):
                moves.append(piece)
                return moves

    for piece in player.pieces:
        if piece.space == "base":
            continue

        # checks if piece can move out of the board into the goal
        if piece.space + roll > baseEntry and piece.space <= baseEntry:
            if canMove(board, piece, player, roll):
                baseAim = piece.space + roll - baseEntry
                if baseAim < 5:
                    if player.base[baseAim - 1] == 0:
                        moves.append(piece)
        # all other moves
        else:
            if canMove(board, piece, player, roll):
                moves.append(piece)

    return moves

# determines if piece can move to field or if a friendly piece is blocking said space
def canMove(board, piece, player, roll):
    baseEntry = (piece.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39

    target = (piece.space + roll) % 40
    # if its in the base it cant move otherwise this would not be called
    if piece.space == "base":
        return False

    # check if piece tries to enter base
    if piece.space + roll > baseEntry and piece.space <= baseEntry:
        baseTarget = piece.space + roll - baseEntry
        if baseTarget < 5 and player.base[baseTarget - 1] == 0:
            return True
        else:
            return False

    # check if piece is in base
    if piece.space < 0:
        for i in range(4):
            if player.base[i] == piece:
                if i + roll > 4:
                    return False
                elif player.base[i + roll] != 0:
                    return False
                else:
                    return True

    # all other
    if board.board[target] == 0:
        return True
    elif board.board[target].color != piece.color:
        return True
    else:
        return False

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

def playGame(strategies):
    players = [Player(1, strategies[0]), Player(2, strategies[1]), Player(3, strategies[2]), Player(4, strategies[3])]
    rankings = [0, 0, 0, 0]
    position = 0
    first = random.randrange(1, 5)
    current = players[first - 1]
    board = Board()
    while stillPlaying(players):
        roll = rollDice()
        print("Player " + str(current.color) + " rolled a " + str(roll))
        moves = legalMoves(board, current, roll)
        if moves:
            chosenPiece = chooseMove(moves, current.strategy)
            processMove(chosenPiece, board, current, roll)

        # debug stuff
        print(board.toString())
        print("--------------------------------------------")

        if finishedCheck(current):
            rankings[position] = current.strategy
            position += 1
        if roll != 6 and not finishedCheck(current):
            current = players[current.color % 4]

# processes Moving a chosen piece on a specific board
def processMove(chosenPiece, board, player, roll):
    baseEntry = (player.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39

    if chosenPiece.space == "base":
        board.enterPiece(player, chosenPiece)
    elif chosenPiece.space < 0:
        for i in range(4):
            if player.base[i] == chosenPiece:
                player.base[i + roll] == chosenPiece
                player.base[i] = 0
    elif chosenPiece.space + roll > baseEntry and chosenPiece.space <= baseEntry:
        player.base[(chosenPiece.space + roll) - baseEntry - 1] = chosenPiece
        board.leavePiece(chosenPiece)
    else:
        board.moveFromTo(chosenPiece.space, (chosenPiece.space + roll) % 40)

# TODO: determines which move is chosen based on the specified strategy
def chooseMove(moves, strategy):
    return moves[0]

def stillPlaying(players):
    playingCount = 0
    for player in players:
        if not finishedCheck(player):
            playingCount += 1
    if playingCount > 1:
        return True
    else:
        return False

if __name__ == '__main__':
    playGame([0, 0, 0, 0])
