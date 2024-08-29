from tkinter import Tk, Canvas
from PIL import Image, ImageTk

class DominoGameUI:
    DOMINO_WIDTH = 645
    DOMINO_HEIGHT = 1215
    HAND_OFFSET_X = 100
    HAND_PLAYER1_Y = 600
    HAND_PLAYER2_Y = 100
    BOARD_OFFSET_X = 600
    BOARD_OFFSET_Y = 350
    PIECE_DISPLAY_WIDTH = 55
    PIECE_DISPLAY_HEIGHT = 120
    PIECE_GAP = 60
    
    def __init__(self, master):
        self.master = master
        self.canvas = Canvas(master, width=1200, height=800, bg="white")
        self.canvas.pack()
        
        self.BOARD = []
        self.PLAYER1_HAND = []
        self.PLAYER2_HAND = []
        
        self.loadImages()
        self.updateGameFlag = False
        self.master.mainloop()
        
    def startUpdateLoop(self):
        self.updateGameFlag = True
        self.updateGame()

    def updateGame(self):
        if self.updateGameFlag:  # Check the flag before updating
            self.renderGame()
            print("hi")
            self.master.after(1000, self.updateGame)

    def renderGame(self):
        self.canvas.delete("all")
        self.displayHand(self.player1Hand, self.HAND_OFFSET_X, self.HAND_PLAYER1_Y)
        self.displayHand(self.player2Hand, self.HAND_OFFSET_X, self.HAND_PLAYER2_Y)
        self.displayBoard(self.board, self.BOARD_OFFSET_X, self.BOARD_OFFSET_Y)
        self.master.update()
        
    def updateGame(self):
        # Placeholder for game state update logic
        self.renderGame()
        self.master.after(1000, self.updateGame)

    def loadImages(self):
        try:
            self.dominoesImage = Image.open("images/dominoes.jpg")
            self.dominoesPhotoImage = ImageTk.PhotoImage(self.dominoesImage)
        except IOError:
            print("Error loading dominoes image.")
            self.master.destroy()
            
    def displayDominoPiece(self, dominoValue, x, y):
        index = dominoValue[0] * 7 + dominoValue[1] - sum(range(dominoValue[0] + 1))
        sx = (index % (self.dominoesImage.width // self.DOMINO_WIDTH)) * self.DOMINO_WIDTH
        sy = (index // (self.dominoesImage.width // self.DOMINO_WIDTH)) * self.DOMINO_HEIGHT
        pieceImage = self.dominoesImage.crop((sx, sy, sx + self.DOMINO_WIDTH, sy + self.DOMINO_HEIGHT))
        pieceImage = pieceImage.resize((self.PIECE_DISPLAY_WIDTH, self.PIECE_DISPLAY_HEIGHT), Image.Resampling.LANCZOS)
        self.canvas.create_image(x, y, image=ImageTk.PhotoImage(pieceImage), anchor="nw")

    def displayHand(self, hand, x, y):
        for i, piece in enumerate(hand):
            self.displayDominoPiece(piece, x + i * self.PIECE_GAP, y)

    def displayBoard(self, board, x, y):
        for i, piece in enumerate(board):
            self.displayDominoPiece(piece, x + i * self.PIECE_GAP, y)
            

    
def renderGame(board, player1Hand, player2Hand, gameUI):
    gameUI.renderGame(board, player1Hand, player2Hand)