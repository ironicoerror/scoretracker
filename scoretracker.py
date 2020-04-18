#!/usr/bin/python3
from sys import argv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import objectlib as olib
import mDB_CRUD as mdb

app = Flask(__name__, static_url_path="/static")
app.secret_key = b';\xf5!\xa7\xfa\xba\x9b\x94P\x15\n.V\xb9\x0c\xe7'

@app.route("/")
@app.route("/home")
def home():
    """checks if the mongoDB is reachable from current device and loads the home.html template"""
    online = not mdb.get_serverstatus()
    if online:
        flash("Server online.", "info")
    else:
        flash("Trouble reaching Database", "error")
    return render_template("home.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    """on GET: loads player and game table and fills the dropdown lists
    on POST: handles the three posible post methods from the form or addplayer/addgame"""
    if request.method == "GET":
        players = list(mdb.read_table("people"))
        games = mdb.read_table("games")
        return render_template("submit_game.html", players=players, games=games)
    if request.method == "POST":
        if not request.is_json: #form data
            try:
                update_gamedata(request.form["sgame"])
                if int(request.form["score_team1"]) > int(request.form["score_team2"]):
                    t1_won, t2_won = True, False
                elif int(request.form["score_team1"]) < int(request.form["score_team2"]):
                    t1_won, t2_won = False, True
                else: t1_won, t2_won = False, False  
                for player in request.form.getlist("team1"):
                    update_playerdata(player, t1_won)
                for player in request.form.getlist("team2"):
                    update_playerdata(player, t2_won)
                create_matchup(request.form)
                flash("Success.", "info")
            except Exception as e:
                flash("Trouble reaching database.\n{0}".format(e), "error")
            finally:
                return redirect(url_for("submit"))
        if request.is_json: #from scipt.js
            if request.headers.get("Js-Function", type=str) == "addGame":
                create_game(request.get_json()["game_name"])
            elif request.headers.get("Js-Function", type=str) == "addPlayer":
                create_player(request.get_json()["player_name"])
            return redirect(url_for("submit"))

@app.route("/stats")
def stats():
    """on GET: loads data from database and gets the connections between players, games and matchups
    on POST: ..."""
    players = mdb.read_table("people")
    games = mdb.read_table("games")
    matchups = mdb.read_table("people") 
    return render_template("stats.html", players=players, games=games, matchups=matchups)

def create_game(game_name):
    """creates a game in the games table with the stats from olib"""
    mdb.create_data(olib.Game(game_name).__dict__, "games")
    return 0

def create_player(player_name):
    """creates a player in the player table with the stats from olib"""
    mdb.create_data(olib.Player(player_name).__dict__, "people")
    return 0
def create_player(player_name):
    """creates a player in the player table with the stats from olib"""
    mdb.create_data(olib.Player(player_name).__dict__, "people")
    return 0
def update_gamedata(game_id):
    """sets the gamedata and updates it in the game table"""
    game_data = mdb.read_item("games", game_id)
    game_data["times_played"] += 1
    game_data["last_played"] = datetime.now()
    response = mdb.update_data(game_data, "games")
    return 0

def update_playerdata(player_id, won):
    """sets the playerdata and updates it in the database"""
    player_data = mdb.read_item("people", player_id)
    player_data["times_played"] += 1
    player_data["last_played"] = datetime.now()
    if won:
        player_data["wins"] += 1
    if not won:
        player_data["losses"] += 1
    response = mdb.update_data(player_data, "people")
    return 0
def create_matchup(form_data):
    """creates a matchup from the formdata and uploads it to the matchups table"""
    new_matchup = {
            "creation_date": datetime.now(),
            "game_played": form_data["sgame"],
            "team1": form_data.getlist("team1"),
            "team2": form_data.getlist("team2"),
            "score_team1": int(form_data["score_team1"]),
            "score_team2": int(form_data["score_team2"])
            }
    mdb.create_data(new_matchup, "matchups") 
    return 0
#test section
if __name__ == "__main__":
    usage_desc = """
    Usage: {0} <license_file> <database_name>
    Note: Please give the complete link to the license file /home/...
    """.format(argv[0])
    if len(argv) == 3:
        mdb.LICENSE_STRING = mdb.set_credentials(argv[1])
        mdb.CLIENT, mdb.DB = mdb.db_init(argv[2])
        app.run(debug=True, host="0.0.0.0")
    else: print(usage_desc)
    print("\n\n------------Success-------------")
