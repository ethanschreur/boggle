from boggle import Boggle
from flask import Flask, request, render_template, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SHHHH SECRETS'

boggle_game = Boggle()

@app.route('/')
def boggle_home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board_template.html', board = board)
@app.route('/submit')
def submit_guess():
    boggle_game.check_valid_word()