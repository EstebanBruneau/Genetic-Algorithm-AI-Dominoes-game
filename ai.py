import random

from ui import *
from prints import *


def aiMoveChoice(game, player, AIstrat, genAI=None, prints = False):
    
    # if AIstrat == "gen":
    #     knownPieces = player + game.board
    #     placeablePieces = game.getPlaceablePieces(player)
    #     firstBoardPiece = game.board[0]
    #     lastBoardPiece = game.board[-1]
    #     chosenPiece, side = genAI.choose_move(placeablePieces, knownPieces, firstBoardPiece, lastBoardPiece)
    
    if AIstrat == "random":
        chosenPiece, side = Titouan3ansEtDemiJoueAuHasard(game, player)
        
    elif AIstrat == "highestFirst":
        chosenPiece, side = Enzo12ansJoueLesPlusGrosDominosIlSeCroitMalinCeFDP(game, player)
        
    else:
        print_colored("Invalid AI strategy. Reverting to default (random).", "red")
        chosenPiece, side = Titouan3ansEtDemiJoueAuHasard(game, player)
    
    return chosenPiece, side

def Titouan3ansEtDemiJoueAuHasard(game, player):
    placeablePieces = game.getPlaceablePieces(player)
    if not placeablePieces:
        return None, None
    listIndex = []
    for i in placeablePieces:
        if game.canPlace(i):
            listIndex.append(i)
    return random.choice(listIndex), "R"

def Enzo12ansJoueLesPlusGrosDominosIlSeCroitMalinCeFDP(game, player):
    placeablePieces = game.getPlaceablePieces(player)
    if not placeablePieces:
        return None, None
    bestPiece = None
    bestScore = -1
    for piece in placeablePieces:
        score = game.getPieceScore(piece)
        if score > bestScore:
            bestScore = score
            bestPiece = piece
    return bestPiece, "R"

