from fastapi import FastAPI, Query
from typing import List
import random, math

app = FastAPI()

@app.get("/simple")
async def make_moves(board: List[int] = Query(...)):
    print(board)

    team = check_our_team(board)
    
    move = check_wins(board, team)
    if move is not None:
        return move
    move = check_block(board, team)
    if move is not None:
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
    
