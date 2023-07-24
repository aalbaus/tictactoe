from fastapi import FastAPI, Query
from typing import List
import random, math

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/random")
async def randommove():
    return random.randint(0, 8)

@app.get("/randommove")
async def randommove(board: List[int] = Query(...)):
    print(board)
    m = random.randint(0, 8)
    print(m)
    while(board[m]!=0):
        m = random.randint(0, 8)
        print(m)
    print("Found Move")
    return m

@app.get("/minmaxmove")
async def minmaxmove(board: List[int] = Query(...)):
    if board.count(1) > board.count(2):
        player = 2
    else:
        player = 1
    print(player)
    m = get_best_move(board, player)
    return m

def check_winner(board, player):
    # Check rows, columns, and diagonals for a winner
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]

    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True

    return False

def get_empty_cells(board):
    return [i for i in range(len(board)) if board[i] == 0]

def minimax(board, depth, maximizing_player, player):
    if check_winner(board, 3-player):
        return -10 + depth
    if check_winner(board, player):
        return 10 - depth
    if len(get_empty_cells(board)) == 0:
        return 0

    if maximizing_player:
        max_eval = -math.inf
        for i in get_empty_cells(board):
            board[i] = player
            eval = minimax(board, depth + 1, False, player)
            board[i] = 0
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in get_empty_cells(board):
            board[i] = 3-player
            eval = minimax(board, depth + 1, True, player)
            board[i] = 0
            min_eval = min(min_eval, eval)
        return min_eval

def get_best_move(board, player):
    best_move = -1
    best_eval = -math.inf
    for i in get_empty_cells(board):
        board[i] = player
        eval = minimax(board, 0, False, player)
        board[i] = 0
        if eval > best_eval:
            best_eval = eval
            best_move = i
    return best_move