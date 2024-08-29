from domino import *
from prints import *

def playHumanHuman(scoreLimit):
    
    game = DominoGame1v1()
    
    print_colored("Game between Human and Human", "pink")
    while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
        print_colored(f"\nScores: \nPlayer 1: ", "magenta", end="")
        print_colored(f"{game.player1_score} ", "blue", end="")
        print_colored("\nPlayer 2: ", "magenta", end="")
        print_colored(f"{game.player2_score}", "blue")    
        
        # new round
        print_colored("\nNew round starts", "blue")

        game.initializeGame()
        while True:
            if game.isRoundOver():
                game.handleRoundOver()
                break
            
            print_colored("\nPlayer 1's turn\n", "blue")
            printBoard(game.board)
            move = game.getMove(game.player1)
            if move is None: # if player can't place a piece, draw a piece
                game.player1 = game.drawPiece(game.player1)
                move = game.getMove(game.player1)
                if move is None: # if player can't draw a piece, round is over
                    game.handleRoundOver()
                    break
            game.player1.remove(move)
            game.placePieceOnBoard(move)
            
            if game.isRoundOver():
                game.handleRoundOver()
                break
            
            print_colored("\nPlayer 2's turn\n", "blue")
            printBoard(game.board)
            move = game.getMove(game.player2)
            if move is None:
                game.player2 = game.drawPiece(game.player2)
                move = game.getMove(game.player2)
                if move is None:
                    game.handleRoundOver()
                    break
            game.player2.remove(move)
            game.placePieceOnBoard(move)
            
def playHumanAI(scoreLimit):
    
    game = DominoGame1v1()
    
    print_colored("Game between Human and AI", "pink")
    first = input("Who goes first? (H/A): ").strip().upper()
    while first not in ['H', 'A']:
        print_colored("Invalid choice. Type 'H' for Human or 'A' for AI.", "red")
        first = input("Who goes first? (H/A): ").strip().upper()
    
    if first == 'H':
        player1 = "Human"
        player2 = "AI"
    else:
        player1 = "AI"
        player2 = "Human"
    
    while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
        print_colored(f"\nScores: \n{player1}: ", "magenta", end="")
        print_colored(f"{game.player1_score} ", "blue", end="")
        print_colored(f"\n{player2}: ", "magenta", end="")
        print_colored(f"{game.player2_score}", "blue")
        
        # new round
        print_colored("\nNew round starts", "blue")
        
        game.initializeGame()
        while True:
            if game.isRoundOver():
                game.handleRoundOver()
                break
            
            if player1 == "Human":
                print_colored("\nPlayer's turn\n", "blue")
                printBoard(game.board)
                move = game.getMove(game.player1)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    move = game.getMove(game.player1)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoard(move)
            else:
                print_colored("\nAI's turn\n", "blue")
                printBoard(game.board)
                move, side = game.getAIMove(game.player1)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    move, side = game.getAIMove(game.player1)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoard(move)
            
            if game.isRoundOver():
                game.handleRoundOver()
                break
            
            if player2 == "Human":
                print_colored("\nPlayer 2's turn\n", "blue")
                printBoard(game.board)
                move = game.getMove(game.player2)
                if move is None:
                    game.player2 = game.drawPiece(game.player2)
                    move = game.getMove(game.player2)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoard(move)
            else:
                print_colored("\nAI's turn\n", "blue")
                printBoard(game.board)
                move, side = game.getAIMove(game.player2)
                if move is None:
                    game.player2 = game.drawPiece(game.player2)
                    move, side = game.getAIMove(game.player2)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoardAI(move, side)
                
def playAIAI(scoreLimit, iterations, AI1, AI2, prints=False):
    
    (Type, AI1Name, AI1Strat) = AI1
    (Type, AI2Name, AI2Strat) = AI2
    
    wins = {AI1Name: 0, AI2Name: 0}
    winner = None
    
    print_colored(f"Starting {iterations} games between {AI1Name} ({AI1Strat}) and {AI2Name} ({AI2Strat})", "pink")
    
    for i in range(iterations):
        game = DominoGame1v1()
        
        if prints: print_colored(f"Game {i + 1}", "blue")
        roundCounter = 0
        
        while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
            # new round
            roundCounter += 1
            winner = None
            game.initializeGame()
            if prints: print(f"\nRound {roundCounter}")
                        
            while True:
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored("\nAI 1's turn\n", "blue")
                if prints: printBoard(game.board)
                move, side = game.getAIMove(game.player1, AI1Name, AI1Strat)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    move, side = game.getAIMove(game.player1, AI1Name, AI1Strat)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoardAI(move, side)
                
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored("\nAI 2's turn\n", "blue")
                if prints: printBoard(game.board)
                move, side = game.getAIMove(game.player2, AI2Name, AI2Strat)
                if move is None:
                    game.player2 = game.drawPiece(game.player2)
                    move, side = game.getAIMove(game.player2, AI2Name, AI2Strat)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoardAI(move, side)
        
        if game.player1_score >= scoreLimit:
            winner = AI1Name
            wins[AI1Name] += 1
        else:
            winner = AI2Name
            wins[AI2Name] += 1
    
    print_colored(f"{AI1Name} ({AI1Strat}) wins: {wins[AI1Name]}", "green")
    print_colored(f"{AI2Name} ({AI2Strat}) wins: {wins[AI2Name]}", "green")

                
def playGenAIGenAI(scoreLimit, iterations, AI1, AI2, prints=False, printResults=False):
    
    AI1Name = AI1
    AI2Name = AI2
    
    wins = {AI1Name: 0, AI2Name: 0}
    winner = None
    
    if printResults: print_colored(f"Starting {iterations} games between {AI1Name} and {AI2Name} ({AI1Name} playing in first)", "pink")
    
    for i in range(iterations):
        game = DominoGame1v1()
        
        if prints: print_colored(f"Game {i + 1}", "blue")
        roundCounter = 0
        
        while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
            # new round
            roundCounter += 1
            winner = None
            game.initializeGame()
            if prints: print(f"\nRound {roundCounter}")
                        
            while True:
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored("\nAI 1's turn\n", "blue")
                if prints: printBoard(game.board)
                if game.board:
                    move, side = AI1.choose_move(game.getPlaceablePieces(game.player1), [game.player1 + game.board], game.board[0], game.board[-1], game.board)
                else:
                    move, side = AI1.choose_move(game.getPlaceablePieces(game.player1), [game.player1 + game.board], None, None, game.board)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    if game.board:
                        move, side = AI1.choose_move(game.getPlaceablePieces(game.player1), [game.player1 + game.board], game.board[0], game.board[-1], game.board)
                    else:
                        move, side = AI1.choose_move(game.getPlaceablePieces(game.player1), [game.player1 + game.board], None, None, game.board)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoardAI(move, side)
                
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored("\nAI 2's turn\n", "blue")
                if prints: printBoard(game.board)
                move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                if move is None:
                    game.player2 = game.drawPiece(game.player2)
                    move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoardAI(move, side)
        
        if game.player1_score >= scoreLimit:
            winner = AI1Name
            wins[AI1Name] += 1
        else:
            winner = AI2Name
            wins[AI2Name] += 1
            
    if printResults: print_colored(f"{AI1Name} wins: {wins[AI1Name]}", "green")
    if printResults: print_colored(f"{AI2Name} wins: {wins[AI2Name]}", "green")
    
    return wins[AI1Name]


def playAIgenAI(scoreLimit, iterations, AI1, AI2, prints=False, printResults=False):
    
    (AI1Type, AI1Name, AI1Strat) = AI1
    AI2Name = AI2
    
    wins = {AI1Name: 0, AI2Name: 0}
    winner = None
    
    if prints: print_colored(f"Starting {iterations} games between {AI1Name} and {AI2Name}", "pink")
    
    for i in range(iterations):
        game = DominoGame1v1()
        
        if prints: print_colored(f"Game {i + 1}", "blue")
        roundCounter = 0
        
        while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
            # new round
            roundCounter += 1
            winner = None
            game.initializeGame()
            if prints: print(f"\nRound {roundCounter}")
                        
            while True:
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored(f"\n{AI1Name}'s turn\n", "blue")
                if prints: printBoard(game.board)
                move, side = game.getAIMove(game.player1, AI1Name, AI1Strat, prints)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    move, side = game.getAIMove(game.player1, AI1Name, AI1Strat, prints)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoardAI(move, side)
                
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored(f"\n{AI2Name}'s turn\n", "blue")
                if prints: printBoard(game.board)
                if prints: print_colored(f"\n{AI2Name}'s hand:", "yellow")
                if prints:
                    for index, piece in enumerate(game.player2):
                        if piece in game.getPlaceablePieces(game.player2):
                            print_colored(f"{index}. {piece}", "green")
                        else:
                            print_colored(f"    {piece}", "red")
                if game.board:
                    move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                else:
                    move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], None, None, game.board)
                if move is None:
                    if prints: print_colored("\nNo pieces can be placed. Drawing from boneyard.", "orange")
                    game.player2 = game.drawPiece(game.player2)
                    if game.board:
                        move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                    else:
                        move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], None, None, game.board)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoardAI(move, side)
                
        if game.player1_score >= scoreLimit:
            winner = AI1Name
            wins[AI1Name] += 1
        else:
            winner = AI2Name
            wins[AI2Name] += 1
    
    if printResults:     
        print_colored(f"{AI1Name} wins: {wins[AI1Name]}", "green")
        print_colored(f"{AI2Name} wins: {wins[AI2Name]}", "green")
    
    return wins[AI1Name]

def playGenAIAI(scoreLimit, iterations, AI2, AI1, prints=False, printResults=False):
    
    (AI1Type, AI1Name, AI1Strat) = AI1
    AI2Name = AI2
    
    wins = {AI1Name: 0, AI2Name: 0}
    winner = None
    
    if prints: print_colored(f"Starting {iterations} games between {AI1Name} and {AI2Name}", "pink")
    
    for i in range(iterations):
        game = DominoGame1v1()
        
        if prints: print_colored(f"Game {i + 1}", "blue")
        roundCounter = 0
        
        while game.player1_score < scoreLimit and game.player2_score < scoreLimit:
            # new round
            roundCounter += 1
            winner = None
            game.initializeGame()
            if prints: print(f"\nRound {roundCounter}")
                        
            while True:
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored(f"\n{AI2Name}'s turn\n", "blue")
                if prints: printBoard(game.board)
                if prints: print_colored(f"\n{AI2Name}'s hand:", "yellow")
                if prints:
                    for index, piece in enumerate(game.player2):
                        if piece in game.getPlaceablePieces(game.player2):
                            print_colored(f"{index}. {piece}", "green")
                        else:
                            print_colored(f"    {piece}", "red")
                if game.board:
                    move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                else:
                    move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], None, None, game.board)
                if move is None:
                    if prints: print_colored("\nNo pieces can be placed. Drawing from boneyard.", "orange")
                    game.player2 = game.drawPiece(game.player2)
                    if game.board:
                        move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], game.board[0], game.board[-1], game.board)
                    else:
                        move, side = AI2.choose_move(game.getPlaceablePieces(game.player2), [game.player2 + game.board], None, None, game.board)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player2.remove(move)
                game.placePieceOnBoardAI(move, side)
                
                if game.isRoundOver():
                    game.handleRoundOver()
                    break
                
                if prints: print_colored(f"\n{AI1Name}'s turn\n", "blue")
                if prints: printBoard(game.board)
                move, side = game.getAIMove(game.player1, AI1Name, AI1Strat, prints)
                if move is None:
                    game.player1 = game.drawPiece(game.player1)
                    move, side = game.getAIMove(game.player1, AI1Name, AI1Strat, prints)
                    if move is None:
                        game.handleRoundOver()
                        break
                game.player1.remove(move)
                game.placePieceOnBoardAI(move, side)
                
        if game.player1_score >= scoreLimit:
            winner = AI1Name
            wins[AI1Name] += 1
        else:
            winner = AI2Name
            wins[AI2Name] += 1
           
    if printResults:
        print_colored(f"{AI1Name} wins: {wins[AI1Name]}", "green")
        print_colored(f"{AI2Name} wins: {wins[AI2Name]}", "green")
    
    return wins[AI2Name]
