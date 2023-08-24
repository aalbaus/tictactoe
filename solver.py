from fastapi import FastAPI, Query
from typing import List
import random, math

app = FastAPI()

@app.get("/simple")
async def randommove(board: List[int] = Query(...)):
    print(board)
    return 0

