from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SHHHH SECRETS'

boggle_game = Boggle()

@app.route('/')
def boggle_home():
    """
    get a new board class and set the board to the session, return the board template with the board list passed to the template
    """
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('board_template.html', board = board)

@app.route('/submit')
def submit_guess():
    """
    get word from query string and get the board from session
    use the word and the board to check if the word is valid using the Boggle Class that was initialized
    """
    word = request.args['word']
    board = session['board']
    return jsonify({'result': boggle_game.check_valid_word(board, word)})

@app.route('/game-over', methods=['POST'])
def game_over():
    """
    run when the game is over. Get the score from the json that the post query returned and update times played, and update the highscore if needed.
    """
    score = request.get_json()['score']
    if (not bool(session.get('times'))):
        session['times'] = 1
    else:
        session['times'] += 1
    if (not bool(session.get('highscore'))):
        session['highscore'] = score
    else:
        if session['highscore'] < score:
            session['highscore'] = score
    return 'done'

