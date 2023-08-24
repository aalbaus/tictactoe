from fastapi import FastAPI, Query
from typing import List
import random, math

app = FastAPI()

WIN_LINES = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],  # horiz.
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],  # vertical
    [1, 5, 9],
    [3, 5, 7],  # diagonal
]

@app.get("/simple")
async def make_moves(board: List[int] = Query(...)):
    print(board)

    team = check_our_team(board)

    move = endgame(board, team)
    if move is not None:
        print(f'endgame {move}')
        return move

    move = do_the_algo(board, team)
    return move

def check_our_team(board):
    total_ones = sum([1 for x in board if x == 1])
    total_twos = sum([1 for x in board if x == 2])
    if total_ones > total_twos:
        return 2
    else:
        return 1

def endgame(board, team):
    their_team = [1, 2][team%2]
    print(f"our team {team} vs their team {their_team}")
    for line in WIN_LINES:
        us = sum([1 for x in line if board[x-1]==team])
        them = sum([1 for x in line if board[x-1]==their_team])
        if us == 2 and them == 0:
            print('we can win')
            value = [x for x in line if board[x-1]==0][0]-1
            return value
        if them == 2 and us == 0:
            print('they can win')
            value = [x for x in line if board[x-1]==0][0]-1
            return value

def do_the_algo(board, team):
    if board[0]!= 0:
        return 2
    return 0