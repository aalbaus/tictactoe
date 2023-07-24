from flask import Flask, render_template, session, redirect, url_for, request
from flask_session import Session
from tempfile import mkdtemp
import urllib.request, json

app = Flask(__name__)

#app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

@app.route("/")
def index():
    if ("teams" not in session):
        return redirect(url_for('teams'))
    if ("board" not in session) or ("reset" in request.form):
        session["board"] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        session["turn"] = session["start"]
        session["symbols"][session["turn"]] = 1
        session["symbols"][not session["turn"]] = 2
        session["start"] = not session["start"]
        session["win"] = False
        session["draw"] = False
    while session["apibool"][session["turn"]] and session["win"] == False and session["draw"] == False:
        move = retrievemove(session["teams"][session["turn"]],session["board"])
        play(move)
    return render_template("game.html", game=session["board"], turn=session["turn"], teams=session["teams"], win=session["win"], draw=session["draw"], score=session["score"])

@app.route("/reset")
def reset():
    if ("board" in session):
        session.pop("board")
    return redirect(url_for("index"))

@app.route("/play/<int:move>")
def play(move):
    if session["board"][move] == 0:
        session["board"][move] = session["symbols"][session["turn"]]
    else:
        session["turn"] = not session["turn"]
        session["win"] = True
        session["score"][session["turn"]] += 100
    if checkwin(session["board"],session["symbols"][session["turn"]]):
        session["win"] = True
        session["score"][session["turn"]] += 100
    elif 0 not in session["board"]:
        session["draw"] = True
    else:
        session["turn"] = not session["turn"]
    return redirect(url_for("index"))

@app.route('/teams', methods=('GET', 'POST'))
def teams():
    if request.method == 'POST':
        session["score"] = [0,0]
        session["teams"] = [request.form['api1'], request.form['api2']]
        if 'boolapi1' in request.form:
            a = True
        else:
            a = False
        if 'boolapi2' in request.form:
            b = True
        else:
            b = False
        session["apibool"] = [a, b]
        session["start"] = 0
        session["symbols"] = [1,2]
        print(request.form)
        return redirect(url_for("reset"))
    return render_template('players.html')

def checkwin(board, player):
    for i in WIN_LINES:
        if board[i[0]-1] == player and board[i[1]-1] == player and board[i[2]-1] == player:
            return True
    return False

def retrievemove(api, board):
    boardq = "?board=" + str(board[0])
    for b in board[1:]:
        boardq += "&board=" + str(b)
    url = "http://" + api + boardq
    m = urllib.request.urlopen(url).read()
    return int(json.loads(m))

if __name__ == "__main__":
    app.run()