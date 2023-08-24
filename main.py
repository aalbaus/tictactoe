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
    if sum(board) == 0:
        return first_move()
    # if sum(board) == 1:
    #     return first_response()

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

def first_move():
    return 0

# def first_response(board, team):
#     return 

def do_the_algo(board, team):
    their_team = [1, 2][team%2]
    open_spots = [x+1 for x in range(9) if board[x]==0]
    print(open_spots)
    spot_score = [0 for x in open_spots]
    for i, each in enumerate(open_spots):
        win_opportunities = 0
        for line in WIN_LINES:
            if each+1 in line:
                line_status = [board[x-1] for x in line]
                if their_team in line_status:
                    pass
                elif team in line_status:
                    win_opportunities += 1
                elif sum(line_status) == 0:
                    win_opportunities += 0.5
                else:
                    print("this shouldn't happen")
        spot_score[i] = win_opportunities
    print(open_spots, spot_score)
    chosen_pos = open_spots[spot_score.index(max(spot_score))]
    print(chosen_pos)
    return chosen_pos