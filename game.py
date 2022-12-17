# holds the gamelogic and gameloop
import copy
import random
import time
import trueskill as trueskill


# board is represented by array of 40 fields, index will keep track of loop
class Board:
    def __init__(self, players):
        self.players = players
        self.board = [0] * 40

    # returns player corresponding to color
    def getPlayer(self, color):
        for player in self.players:
            if player.color == color:
                return player

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
        if checkBaseEntry(piece, roll):
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

# checks if a piece passes its base entry
def checkBaseEntry(piece, roll):
    if piece.space == "base":
        return False
    baseEntry = (piece.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39
    for i in range(1, roll):
        if piece.space + i == baseEntry:
            return True
    return False



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
    if checkBaseEntry(piece, roll):
        baseTarget = piece.space + roll - baseEntry
        if baseTarget < 5 and player.base[baseTarget - 1] == 0:
            return True
        else:
            return False

    # check if piece is in base
    if piece.space < 0:
        pieceIndex = -1
        for i in range(4):
            if player.base[i] == piece:
                pieceIndex = i
        aim = pieceIndex + roll
        if aim > 3:
            return False
        elif player.base[aim] != 0:
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
    playing = 4
    turns = 0
    first = random.randrange(1, 5)
    current = players[first - 1]
    board = Board(players)
    while playing > 1:
        turns += 1
        roll = rollDice()
        #print("Player " + str(current.color) + " rolled a " + str(roll))
        moves = legalMoves(board, current, roll)
        if moves:
            chosenPiece = chooseMove(board, moves, roll, current)
            processMove(chosenPiece, board, roll)

        # debug stuff
        #print(board.toString())
        #print("--------------------------------------------")

        if roll != 6 and not finishedCheck(current):
            current = players[current.color % playing]

        if finishedCheck(current):
            rankings[position] = current.strategy
            position += 1
            playing -= 1
            players.remove(current)
            current = players[current.color % playing]

    rankings[position] = players[0].strategy
    #print("Game took " + str(turns) + " turns.")
    return rankings

# processes Moving a chosen piece on a specific board
def processMove(chosenPiece, board, roll):
    player = board.getPlayer(chosenPiece.color)
    baseEntry = (player.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39

    if chosenPiece.space == "base":
        board.enterPiece(player, chosenPiece)
    elif chosenPiece.space < 0:
        for i in range(4):
            if player.base[i] == chosenPiece:
                player.base[i + roll] = chosenPiece
                player.base[i] = 0
                return
    elif checkBaseEntry(chosenPiece, roll):
        leftOnEntry = chosenPiece.space + roll - baseEntry
        player.base[leftOnEntry - 1] = chosenPiece
        board.leavePiece(chosenPiece)
    else:
        board.moveFromTo(chosenPiece.space, (chosenPiece.space + roll) % 40)

# determines which move is chosen based on the specified strategy
def chooseMove(board, moves, roll, player):
    if player.strategy == "Random":
        return random.choice(moves)
    elif player.strategy == "TryToKnock":
        closest = random.choice(moves)
        closestDistance = disToOpponent(board, closest, roll)
        for piece in moves:
            if doesItKnock(board, piece, roll):
                return piece
            else:
                distance = disToOpponent(board, piece, roll)
                if distance > closestDistance:
                    closest = piece
                    closestDistance = distance
        return closest
    elif player.strategy == "RushOnePiece":
        ordered = piecesOrdered(moves)
        if ordered:
            return ordered[0]
        else:
            return random.choice(moves)
    elif player.strategy == "StickTogether":
        ordered = piecesOrdered(moves)
        if ordered:
            return ordered[-1]
        else:
            return random.choice(moves)
    elif player.strategy == "LookOneAhead":
        return lookahead(board, moves, roll, player)
    else:
        return moves[0]

# TODO: increase depth
# heuristic based minimax tree of fixed depth to return best move
def lookahead(board, originalMoves, roll, player):
    copied = copy.deepcopy(board)
    moves = legalMoves(copied, copied.getPlayer(player.color), roll)
    bestMove = None
    bestH = -99999
    for move in moves:
        unmovedMove = copy.deepcopy(move)
        copied = copy.deepcopy(board)
        processMove(move, copied, roll)
        h = heuristic(copied, copied.getPlayer(player.color))
        if h > bestH:
            bestH = h
            bestMove = unmovedMove
    for piece in originalMoves:
        if piece.color == bestMove.color and piece.space == bestMove.space:
            return piece

# heuristic to determine boards value for a player
def heuristic(board, player):
    playerSum = 0
    opponentsSum = 0

    for i in player.pieces:
        playerSum += disToBase(i)

    for i in board.board:
        if i != 0:
            if i.color != player.color:
                opponentsSum += disToBase(i)

    # the larger the opponents sum the better for us, the lower our dist to base sum the better for us
    return opponentsSum - playerSum

# checks if a move would knock an opponents piece
def doesItKnock(board, piece, roll):
    if piece.space == "base" or piece.space < 0:
        return False
    target = (piece.space + roll) % 40
    if checkBaseEntry(piece, roll):
        return False
    elif board.board[target] != 0:
        return True
    else:
        return False

# calculates distance to nearest knockable opponent after move
def disToOpponent(board, piece, roll):
    # if pieces enters the safe base after the roll it will not be able to knock anyone
    if checkBaseEntry(piece, roll):
        return 99

    if piece.space == "base":
        spaceAfterRoll = (piece.color - 1) * 10
    else:
        spaceAfterRoll = (piece.space + roll) % 40

    for i in range(1, 40):
        checkedIdx = (spaceAfterRoll + i) % 40
        checking = board.board[checkedIdx]
        if checking != 0 and checking.color != piece.color:
            return i
    return 99

# calculates distance to base entry
def disToBase(piece):
    if piece.space == "base":
        return 40
    if piece.space < 0:
        return -1

    entry = (piece.color - 1) * 10
    baseEntry = (piece.color - 1) * 10 - 1
    if baseEntry < 0:
        baseEntry = 39

    progress = 39 - piece.space - entry
    if progress < 0:
        return baseEntry - piece.space
    else:
        return progress

# returns ordered array of a players pieces (which they have on the board) with their positions from first to last
def piecesOrdered(moves):
    ordered = []
    for piece in moves:
        if piece.space != "base" and piece.space >= 0:
            ordered.append(piece)
    ordered.sort(key=disToBase)
    return ordered


if __name__ == '__main__':

    strategies = ["Random", "TryToKnock", "RushOnePiece", "StickTogether", "LookOneAhead"]
    ratings = {"Random" : trueskill.Rating(), "TryToKnock" : trueskill.Rating(), "RushOnePiece" : trueskill.Rating(), "StickTogether" : trueskill.Rating(), "LookOneAhead" : trueskill.Rating()}
    stats = {"Random" : [0, 0, 0, 0], "TryToKnock" : [0, 0, 0, 0], "RushOnePiece" : [0, 0, 0, 0], "StickTogether" : [0, 0, 0, 0], "LookOneAhead" : [0, 0, 0, 0]}

    for i in range(200):
        players = random.sample(strategies, 4)
        results = playGame(players)
        #print("Results of game: " + str(results))
        for i in range(4):
            stats[results[i]][i] += 1
        r1 = ratings[results[0]]
        r2 = ratings[results[1]]
        r3 = ratings[results[2]]
        r4 = ratings[results[3]]
        r1, r2, r3, r4 = trueskill.rate([(r1,), (r2,), (r3,), (r4,)])
        ratings[results[0]] = r1[0]
        ratings[results[1]] = r2[0]
        ratings[results[2]] = r3[0]
        ratings[results[3]] = r4[0]

        #print("Updated Ratings: ")
        #for i in ratings:
        #    print(i + ": " + str(ratings[i]))
    print("Stats: ")
    for i in stats:
        print(i + ": " + str(stats[i]))

    print("Updated Ratings: ")
    for i in ratings:
        print(i + ": " + str(ratings[i]))
