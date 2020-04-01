#!/usr/bin/python3

from flask import Flask, render_template
import objectlib as olib 

app = Flask(__name__, static_url_path="/static")
@app.route("/home")
def home():
    return render_template("home.html")
def show_players():
    print("Players currently listed:")
    for _player in olib.PLAYER_LIST:
        print(_player.name)
    return 0

def show_games():
    print("Games currently listed:")
    for _game in olib.GAMES_LIST:
        print(_game.name)
    return 0

def submit_game(team1, team2, game_played, final_score):
    olib.game_played.played()
    return 0 

def create_matchup(team1, team2):
    pass

def update_matchup(team1, team2):
    pass

#test section
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    print("\n\n------------Success-------------")
