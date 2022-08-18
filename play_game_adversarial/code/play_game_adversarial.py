import pygame
import math
import sys
import random
import time
from pygame.locals import *

tick = 1
win=pygame.display.set_mode((700,700))
pygame.init()
Font = pygame.font.SysFont
mouse = pygame.mouse.get_pos()

def squareDetection(mouse):
    # square detection is done by finding the closest square to the mouse position
    for i in range (size_board):
        if mouse[0] > (xc + i*(width-width/7)) and mouse[0] < xc+(((i+1)*5-1)*(width-width/7)):
            newx=i
        if mouse[1] > (yc + i*(width-width/7)) and mouse[1] < yc+(((i+1)*5-1)*(width-width/7)):
            newy=i
    try:
        feldnr=(newy-1)*size_board+newx-1
    except UnboundLocalError:
        return False
    
    try:
        if board[newy][newx] == 0:
            board[newy][newx] = 2
            return True
    except UnboundLocalError:
        pass

def victorycheck():
    #  check for victory 
    counter=0
    for i in range (size_board):
        for j in range (size_board):

            # Horizontal victory
            for k in range (triumph-1):
                if j+k+1 < size_board:
                    if board[i][j+k] == board[i][j+k+1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                    return float('inf')
                else:
                    return float('-inf')
            counter=0

            # vertical victorytest
            for k in range (triumph-1):
                if i+k+1 < size_board:
                    if board[i+k][j] == board[i+k+1][j] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                    return float('inf')
                else:
                    return float('-inf')
            counter=0

            #Diagonal victorytest
            for k in range (triumph-1):
                if i+k+1 < size_board and j+k+1 < size_board:
                    if board[i+k][j+k] == board[i+k+1][j+k+1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                    return float('inf')
                else:
                    return float('-inf')
            counter=0

            #Diagonal victorytest
            for k in range (triumph-1):
                if i+k+1 < size_board and j-k-1 >= 0:
                    if board[i+k][j-k] == board[i+k+1][j-k-1] != 0:
                        counter+=1
            if counter == triumph-1:
                if board[i][j] == 1:
                    return float('inf')
                else:
                    return float('-inf')
            counter=0
    return 1

def alp_bet_prunning(maximizing, depth, alpha, beta):
    victory = victorycheck()
    if True:
        check = False
        for i in range (size_board):
            for j in range (size_board):
                if board[i][j] == 0:
                    check = True
        if check == False and abs(victory) != float('inf'):
            victory = 0    
    # if the game is over, return the victory value
    if depth==0 or victory != 1:
        if victory == float('inf') or victory == float('-inf'):
            return victory
        else:
            return evaluation()
    # if the bot is the current player, maximize
    if maximizing:
        maxvalue = float('-inf')
        possibleMoveList = possibleMoves(0,False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])
            # if the move is a winning move, return infinity
            value = alp_bet_prunning(False,depth-1,alpha,beta)
            # if the move is a losing move, return -infinity
            undoMove(possibleMoveList[i])
            # if the move is a draw, return 0
            maxvalue = max(maxvalue,value)
            alpha = max(alpha,value)
            # if the alpha value is bigger than the beta value, return the alpha value
            if True:
                if beta <= alpha:
                    break
        return maxvalue

    # if the bot is the opponent, minimize
    elif not maximizing:
        # if the bot is the opponent, minimize
        minvalue = float('inf')
        possibleMoveList = possibleMoves(1,False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])
            # if the move is a winning move, return -infinity
            value = alp_bet_prunning(True,depth-1,alpha,beta)
            undoMove(possibleMoveList[i])
            # if the move is a losing move, return infinity
            minvalue = min(minvalue,value)
            beta = min(beta,value)
            # if the beta value is smaller than the alpha value, return the beta value
            if True:
                if beta <= alpha:
                    break
        return minvalue


def minimax(maximizing, depth, alpha, beta):
    victory = victorycheck()
    if True:
        check = False
        for i in range (size_board):
            for j in range (size_board):
                if board[i][j] == 0:
                    check = True
        if check == False and abs(victory) != float('inf'):
            victory = 0
                    
    # if the game is over, return the victory value
    if depth == 0 or victory != 1:
        if victory == float('inf') or victory == float('-inf'):
            return victory
        else:
            return evaluation()

    # if the bot is the current player, maximize
    if maximizing:
        maxvalue=float('-inf')
        possibleMoveList = possibleMoves(0,False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])
            # if the move is a winning move, return infinity
            value = minimax(False,depth-1,alpha,beta)
            # if the move is a losing move, return -infinity
            undoMove(possibleMoveList[i])
            # if the move is a draw, return 0
            maxvalue = max(maxvalue,value)
            alpha = max(alpha,value)
        return maxvalue

    # if the bot is the opponent, minimize
    elif not maximizing:
        minvalue = float('inf')
        possibleMoveList = possibleMoves(1, False)
        for i in range (len(possibleMoveList)):
            doMove(possibleMoveList[i])
            # if the move is a winning move, return -infinity
            value = minimax(True,depth-1,alpha,beta)
            undoMove(possibleMoveList[i])
            # if the move is a losing move, return infinity
            minvalue = min(minvalue,value)
            beta = min(beta,value)
        return minvalue
    
def possibleMoves(testturn,presorting):
    moveList=[]
    victory = victorycheck()
    if victory == 1:
        for i in range(size_board):
            for j in range(size_board):
                if (board[i][j]==0):
                    move=[i,j,testturn+1]
                    moveList.append(move)
    if presorting:
        return presortingPossibleMoves(moveList)
    else:
        return moveList

    # if AI is the current player, maximize

def presortingPossibleMoves(moveList):
    quality=[]
    for i in range (len(moveList)):
        evaluationMoves(moveList[i])
        quality.append(moveList[i][3])
    quality = sorted(quality, reverse=True)
    betterListedArray=[]
    for j in range (len(quality)):
        for i in range (len(moveList)):
            if quality[j] == moveList[i][3]:
                betterListedArray.append(moveList[i])
    return betterListedArray

def doMove(move):
    y=move[0]
    x=move[1]
    board[y][x]=move[2]

def undoMove(move):
    y=move[0]
    x=move[1]
    board[y][x]=0

def evaluation():
    eval=0.0
    center=(size_board-1)/2
    for i in range (size_board):
        for j in range (size_board):
            if board[i][j] == 1:
                # if AI is in the center, return a high value
                eval += 1/(math.sqrt((center-i)**2 + (center-j)**2)+1)
                if i == j or size_board-1-i == j or i == size_board-1 -j:
                    eval+=0.15
            elif board[i][j] == 2:
                # if the opponent is in the center, return a low value
                eval -= 1/(math.sqrt((center-i)**2 + (center-j)**2)+1)
                if i==j or size_board-1-i == j or i == size_board-1 -j:
                    eval-=0.15
    return eval

def evaluationMoves(move):
    eval = 0.0
    center=(size_board-1)/2
    if move[0]==move[1] or size_board-1-move[0] == move[1] or move[0] == size_board-1 -move[1]:
        eval+=0.15
    eval += 1/(math.sqrt((center-move[0])**2 + (center-move[1])**2)+1)
    move=move.append(eval)
    return move


def settings(mouse):
    global size_board
    global circle_position
    global circle_position_turn
    global circle_type_search
    global search_type
    global requesteddepth
    global turn
    if 115 < mouse[0] < 130 and 50 < mouse[1] < 70 and size_board != 3:
        size_board = 3
        requesteddepth = 5
        circle_position = 120
        reset_board()
    if 165 < mouse[0] < 190 and 50 < mouse[1] < 70 and size_board != 5:
        size_board = 5
        requesteddepth = 3
        circle_position = 170
        reset_board()
    if 230 < mouse[0] < 240 and 55 < mouse[1] < 70 and size_board != 7:
        size_board = 7
        requesteddepth = 3
        circle_position = 235
        reset_board()
    if 535 < mouse[0] < 565 and 55 < mouse[1] < 70:
        circle_position_turn = 550
        reset_board()
    if 580 < mouse[0] < 620 and 55 < mouse[1] < 70:
        circle_position_turn = 600
        reset_board()
    if 315 < mouse[0] < 330 and 55 < mouse[1] < 70:
        circle_type_search = 320
        search_type = 1
        reset_board()
    if 400 < mouse[0] < 425 and 55 < mouse[1] < 70:
        circle_type_search = 420
        search_type = 2
        reset_board()

def reset_board():
    global board
    global triumph 
    global width
    global bestMove
    global requesteddepth
    global mouse
    triumph=round(size_board/2+1.77)
    print ("Board",triumph)
    width=int(700/size_board)
    board = []
    xBoard = []
    for i in range (size_board):
        for t in range (size_board):
            xBoard.append(0)
        board.append(xBoard)
        xBoard=[]
    bestMove=[]
    win.fill((30,30,30))
    drawRectangles(win, size_board, mouse, width,xc,yc)
    drawFigures(win, size_board, board, xc, yc, width)
    drawUI(win, circle_position, circle_position_turn, circle_type_search, triumph)

def drawUI(win, circle_position, circle_position_turn, circle_type_search, triumph):
    pygame.draw.rect(win,("white"),(120,57,120,5))
    pygame.draw.rect(win,("white"),(550,57,50,5))
    pygame.draw.rect(win,("white"),(320,57,100,5))
    pygame.draw.circle(win,("red"), (circle_position_turn,60) , 8, 10)
    pygame.draw.circle(win,("red"), (circle_position,60) , 8, 10)
    pygame.draw.circle(win,("red"), (circle_type_search, 60) , 8, 10)

    Font = pygame.font.SysFont
    font1=Font("Arial",20)
    numbers = font1.render("3        5          7", 1, ("white"))
    textAboutSideLength = font1.render("Side Length", 1, ("white"))

    textAboutTurn = font1.render("Who first?", 1, ("white"))
    turnText = font1.render("AI     Human", 1, ("white"))
    
    type_advsearchmessage = font1.render("Which type adversarial search ?", 1, ("white"))
    type_advsearch = font1.render("Minimax        a_b_prunning", 1, ("white"))

    triumphmessage_1 = "You need "
    triumphmessage_2 = " to win"
    triumphmessage = triumphmessage_1 + str(triumph) + triumphmessage_2
    tellVictoryText = font1.render(triumphmessage,1,("white"))

    textrect_1 = numbers.get_rect()
    textrect_2 = textAboutSideLength.get_rect()
    textrect_3 = textAboutTurn.get_rect()
    textrect_4 = turnText.get_rect()
    
    textrect_10 = tellVictoryText.get_rect()

    textrect_11 = type_advsearchmessage.get_rect()
    textrect_12 = type_advsearch.get_rect()

    textrect_1.topleft = (120, 30)
    textrect_2.topleft = (10, 30)
    textrect_3.topleft = (530, 10)
    textrect_4.topleft = (530, 30)
    textrect_10.topleft = (280, 65)

    textrect_11.topleft = (280, 10)
    textrect_12.topleft = (280, 30)

    win.blit(numbers,textrect_1)
    win.blit(textAboutSideLength,textrect_2)
    win.blit(textAboutTurn,textrect_3)
    win.blit(turnText,textrect_4)
    win.blit(tellVictoryText,textrect_10)
    win.blit(type_advsearchmessage, textrect_11)
    win.blit(type_advsearch, textrect_12)

def drawFigures(win, size_board, board, xc, yc, width):
    for i in range (size_board):
        for t in range (size_board):
            if board[i][t] == 1:
                pygame.draw.circle(win,("red"), (int(xc+(0.25*width)+t*(width-width/7)) , int(yc+(0.25*width)+i*(width-width/7))) , int(width/5) , int(width/12))
            if board[i][t] == 2:
                # draw the / sign
                pygame.draw.line(win,("black"), (int(xc+(0.4*width)+t*(width-width/7)) , int(yc+(0.05*width)+i*(width-width/7))) , (int(xc+(0.1*width)+t*(width-width/7)) , int(yc+(0.12*width)+i*(width-width/7))+int(width/3)), int(width/10))
                # draw the \ sign
                pygame.draw.line(win,("black"), (int(xc+(0.1*width)+t*(width-width/7)) , int(yc+(0.05*width)+i*(width-width/7))) , (int(xc+(0.4*width)+t*(width-width/7)) , int(yc+(0.12*width)+i*(width-width/7))+int(width/3)), int(width/10))


def drawRectangles(win, size_board, mouse, width,x,y):
    for i in range (size_board):
        for t in range (size_board):
            if x <= mouse[0] <= x+(width/2) and y <= mouse[1] <= y+(width/2):
                pygame.draw.rect(win,("light grey"),(x,y,width/2,width/2))
            else:
                pygame.draw.rect(win,("white"),(x,y,width/2,width/2))
            x+=(width-width/7)
        x-=size_board*(width-width/7)
        y+=(width-width/7)

# Render the objects


if True:    
    hit=False
    feldnr = 0
    size_board=3
    circle_position = 120 # size board check
    circle_position_turn = 550 # change turn
    circle_type_search = 320

    # 1: minimax // 2: alpha-beta prunning
    search_type = 1
    turn=-1
    board=[]
    requesteddepth=5
    presortingInitialMoves=False
    xc=80
    yc=100

    reset_board()

    bot = False
    presorting=False

run = True

while run:
    pygame.time.delay(tick)
    mouse = pygame.mouse.get_pos()
    win.fill((55, 235, 200))

    # Event Handling
    drawRectangles(win, size_board, mouse, width,xc,yc)    
    drawFigures(win, size_board, board, xc, yc, width)
    drawUI(win, circle_position, circle_position_turn, circle_type_search, triumph)
        
    if True:
        if turn == float('inf'):
            font1 = pygame.font.SysFont("Arial",100)
            redWins = font1.render("Haha, Loser !!!", 1, ((200,50,50)))
            textrect_7 = redWins.get_rect()
            textrect_7.topleft = (100, 300)
            win.blit(redWins,textrect_7)
        if turn == float('-inf'): 
            font1=pygame.font.SysFont("Arial",100)
            blueWins = font1.render("You won !!!", 1, ((100,0,255)))
            textrect_8 = blueWins.get_rect()
            textrect_8.topleft = (100, 300)
            win.blit(blueWins,textrect_8)
        if True:
            check = False
            for i in range (size_board):
                for j in range (size_board):
                    if board[i][j] == 0:
                        check = True
            if check == False and abs(turn) != float('inf'):
                font1=pygame.font.SysFont("Arial",100)
                noWins = font1.render("Draw. No Winner", 1, ("blue"))
                textrect_9 = noWins.get_rect()
                textrect_9.topleft = (25, 300)
                win.blit(noWins,textrect_9)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and turn == -1:
            hit=squareDetection(mouse)
            if hit:
                turn = victorycheck()
        if event.type == pygame.MOUSEBUTTONDOWN and (600 < mouse[1] or mouse[1] < 100) :
            settings(mouse)
    # Check Turn
    if True:
        check_turn = 0
        for i in range (size_board):
            for j in range (size_board):
                if board[i][j] != 0:
                    check_turn += 1
        if check_turn < 1:
            if circle_position_turn == 550:
                turn = 1
            else:
                turn = -1
    
    if turn == 1:
        # AI active
        savedMove=bestMove
        zeitVorher=time.time()
        font1=Font("Arial",20)
        # prolonged
        redWins = font1.render("AI Calculating...", 1, ((0,0,255)))
        textrect_7 = redWins.get_rect()
        textrect_7.topleft = (300, 650)
        win.blit(redWins,textrect_7)
        pygame.display.update()
        bestSituation = -100
        check = 0
        for i in range (size_board):
            for j in range (size_board):
                if board[i][j] != 0:
                    check += 1
        print("Check:",check)
        if check > 0:
            betterListedArray = possibleMoves(0,presortingInitialMoves)
            for i in range (len(betterListedArray)):
                doMove(betterListedArray[i])
                if search_type == 1:
                    situation = minimax(False,requesteddepth,bestSituation,float('inf'))
                elif search_type == 2:
                    situation = alp_bet_prunning(False,requesteddepth,bestSituation,float('inf'))
                print("AI:",situation)
                undoMove(betterListedArray[i])
                if situation > bestSituation:
                    bestSituation = situation
                    bestMove = betterListedArray[i]
            check_turn = 0
            if bestMove == savedMove and len(betterListedArray) != 0:
                check_turn = float('-inf')
        else:
            center = int((size_board-1)/2)
            bestMove=[center,center,1]
        doMove(bestMove)
        zeitNachher = time.time()

        if False:
            while True:
                yBot=random.randint(0,size_board-1)
                xBot=random.randint(0,size_board-1)
                if board[yBot][xBot]==0:
                    break
            board[yBot][xBot]=1

        turn=victorycheck()*-1
        if turn == float('-inf') or turn == float('-inf'):
            turn = turn * -1
        print ("board:",triumph , "x", triumph)
        if check_turn == float('-inf'):
            turn = check_turn
    pygame.display.update()