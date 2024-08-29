import random
from prints import *

from ai import aiMoveChoice

class DominoGame1v1:
    def __init__(self):
        self.dominoes = self.generateDominoSet()
        self.player1 = []
        self.player2 = []
        self.player1_score = 0
        self.player2_score = 0
        self.player1_turn = True
        self.game_over = False
        self.board = []
        self.boneyard = []
        
    def generateDominoSet(self):
        return [(i, j) for i in range(7) for j in range(i, 7)]

    def dealHands(self):
        random.shuffle(self.dominoes)
        self.player1 = self.dominoes[:7]
        self.player2 = self.dominoes[7:14]

    def initializeGame(self):
        self.dealHands()
        self.board = []
        self.boneyard = self.dominoes[14:]
    
    def isRoundOver(self):
        return (not self.player1 or not self.player2 or 
                (not self.canPlacePiece(self.player1) and not self.canPlacePiece(self.player2) and not self.boneyard))
    
    def canPlace(self, piece):
        if not self.board:
            return True
        else:
            left_end = self.board[0][0]
            right_end = self.board[-1][1]
            return piece[0] in [left_end, right_end] or piece[1] in [left_end, right_end]
        
    def getUserChoice(self):
        while True:
            choice = input("Choose placement (L/R): ").strip().upper()
            if choice in ['L', 'R']:
                return choice
            else:
                print_colored("Invalid choice. Please type 'L' for left or 'R' for right.", "red")
    
    def canPlacePiece(self, hand):
        return any(self.canPlace(piece) for piece in hand)

    def flipPieceIfNeeded(self, piece, target, side):
        if side == 'R':
            return piece if piece[0] == target else (piece[1], piece[0])
        else:
            return piece if piece[1] == target else (piece[1], piece[0])
        
    def placePieceOnBoard(self, piece):
        if not self.board:
            self.board.append(piece)
            return

        can_place_left, can_place_right = self.canPlacePieceLR(piece)

        if can_place_left and can_place_right:
            choice = self.getUserChoice()
            if choice == 'L':
                self.board.insert(0, self.flipPieceIfNeeded(piece, self.board[0][0], 'L'))
            else:
                self.board.append(self.flipPieceIfNeeded(piece, self.board[-1][1], 'R'))
        elif can_place_left:
            self.board.insert(0, self.flipPieceIfNeeded(piece, self.board[0][0], 'L'))
        elif can_place_right:
            self.board.append(self.flipPieceIfNeeded(piece, self.board[-1][1], 'R'))

    def placePieceOnBoardAI(self, piece, side):
        if not self.board:
            self.board.append(piece)
            return

        can_place_left, can_place_right = self.canPlacePieceLR(piece)

        if can_place_left and can_place_right:
            choice = side
            if choice == 'L':
                self.board.insert(0, self.flipPieceIfNeeded(piece, self.board[0][0], 'L'))
            else:
                self.board.append(self.flipPieceIfNeeded(piece, self.board[-1][1], 'R'))
        elif can_place_left:
            self.board.insert(0, self.flipPieceIfNeeded(piece, self.board[0][0], 'L'))
        elif can_place_right:
            self.board.append(self.flipPieceIfNeeded(piece, self.board[-1][1], 'R'))
            
    def drawPiece(self, hand):
        while not self.canPlacePiece(hand) and self.boneyard:
            hand.append(self.boneyard.pop())
        return hand

    def calculateScore(self, hand):
        return sum(sum(piece) for piece in hand)
    
    def isGameOver(self, score_limit):
        return self.player1_score >= score_limit or self.player2_score >= score_limit
    
    def updateScores(self):
        winPlayer2Score = self.calculateScore(self.player1)
        winPlayer1Score = self.calculateScore(self.player2)
        if winPlayer1Score > winPlayer2Score:
            self.player1_score += winPlayer1Score
            return 1
        else:
            self.player2_score += winPlayer2Score
            return 2
        
    def handleRoundOver(self):
        self.updateScores()
        
    # def handleRoundOverAiAi(self):
    #     winner = self.updateScores()
    #     if winner == 1:
    #         return 1
    #     elif winner == 2:
    #         return 2
    
    def validateInput(self, placeable_pieces, hand):
        ask = input("Select a piece to place by typing its number: ")
        while not ask.isdigit() or int(ask) < 1 or int(ask) > len(hand) or hand[int(ask)-1] not in placeable_pieces:
            ask = input("Invalid input. Please type the number of a placeable piece: ")
        return hand[int(ask) - 1]

    def getPlaceablePieces(self, hand):
        return [piece for piece in hand if self.canPlace(piece)]
    
    def getMove(self, hand):
        placeable_pieces = self.getPlaceablePieces(hand)
        print_colored("\nYour hand:", "yellow")
        for index, piece in enumerate(hand, start=1):
            if piece in placeable_pieces:
                print_colored(f"{index}. {piece}", "green")
            else:
                print_colored(f"    {piece}", "red")
        if not placeable_pieces:
            print_colored("\nNo pieces can be placed. Drawing from boneyard.", "orange")
            return None
        return self.validateInput(placeable_pieces, hand)
    
    def getAIMove(self, hand, AIName, AIstrat, prints=False):
        placeable_pieces = self.getPlaceablePieces(hand)
        if prints:
            print_colored("\n" + AIName + "'s hand:", "yellow")
            for index, piece in enumerate(hand, start=1):
                if piece in placeable_pieces:
                    print_colored(f"{index}. {piece}", "green")
                else:
                    print_colored(f"    {piece}", "red")
        if not placeable_pieces:
            if prints: print_colored("\nNo pieces can be placed. Drawing from boneyard.", "orange")
            return None, None
        return aiMoveChoice(self, hand, AIstrat, prints)

    def canPlacePiece(self, hand):
        return any(self.canPlace(piece) for piece in hand)

    def canPlacePieceLR(self, piece):
        left_end = self.board[0][0]
        right_end = self.board[-1][1]
        # Check if the piece can be placed on the left end
        can_place_left = piece[0] in [left_end] or piece[1] in [left_end]
        can_place_right = piece[1] in [right_end] or piece[0] in [right_end]
        return can_place_left, can_place_right
    
    def getPieceScore(self, piece):
        return sum(piece)