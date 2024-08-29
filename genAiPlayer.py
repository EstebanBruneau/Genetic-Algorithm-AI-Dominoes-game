import numpy as np
import os

class genAiPlayer:
    def __init__(self, name, weights=None):
        self.name = name
        self.weights = weights if weights is not None else np.random.randn(40)
        self.fitness = 0

    def choose_move(self, placeablePieces, knownPieces, firstBoardPiece, lastBoardPiece, boardState):
        bestPiece = None
        bestScore = -1
        for piece in placeablePieces:
            score = self.getPieceScore(piece, knownPieces, firstBoardPiece, lastBoardPiece, boardState)
            if score > bestScore:
                bestScore = score
                bestPiece = piece
        return bestPiece, "R"

    def getPieceScore(self, piece, knownPieces, firstBoardPiece, lastBoardPiece, boardState):
        if firstBoardPiece is None:
            features = self.getFeatures(piece, knownPieces, [], [], boardState)
        features = self.getFeatures(piece, knownPieces, firstBoardPiece, lastBoardPiece, boardState)
        return np.dot(features, self.weights)
    
    def count(self, pieces, number):
        return sum(number in piece for piece in pieces)

    def getFeatures(self, piece, knownPieces, firstBoardPiece, lastBoardPiece, boardState):
        features = np.zeros(40)
        
        # Current piece features
        for i in range(7):
            features[i] = 1 if i in piece else 0
            
        # Known pieces features
        for i in range(7):
            features[i + 7] = self.count(knownPieces, i)
            
        # First board piece features
        if firstBoardPiece is not None:
            for i in range(7):
                features[i + 14] = 1 if i in firstBoardPiece else 0
        else:
            features[14:21] = 0  # No first board piece
        
        # Last board piece features
        if lastBoardPiece is not None:
            for i in range(7):
                features[i + 21] = 1 if i in lastBoardPiece else 0
        else:
            features[21:28] = 0  # No last board piece
            
        # Board state features
        for i in range(7):
            features[i + 28] = self.count(boardState, i)
        
        features[35] = len(knownPieces)  # Total number of known pieces
        features[36] = len(boardState)  # Total number of pieces on the board
        features[37] = len(set(num for piece in boardState for num in piece))  # Diversity of numbers on the board
        
        # Potential moves feature
        if firstBoardPiece is not None and lastBoardPiece is not None:
            features[38] = sum(1 for kp in knownPieces if any(x in kp for x in firstBoardPiece) or any(x in kp for x in lastBoardPiece))
        else:
            features[38] = 0
        
        # Known vs. Unknown pieces feature
        features[39] = len(knownPieces) - sum(1 for kp in knownPieces if set(kp).issubset(piece))
        
        return features
        
    def __repr__(self):
        return f"AIPlayer({self.name})"
        
