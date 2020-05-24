#!/usr/bin/env python3
"""Server app, containing the routes to the Putzplan and Scoretracker
with a given mongoDB login or local mongoDB you can setup a server
that is tracking players, games and matchups for statistics"""

from os import path
from sys import argv, stderr
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import objectlib as olib
import putzplan as pp

# flask initialization 
app = Flask(__name__, static_url_path="/static")
app.secret_key = b';\xf5!\xa7\xfa\xba\x9b\x94P\x15\n.V\xb9\x0c\xe7'

@app.route("/")
def root():
    """load the root homepage"""
    return render_template("root.html")

@app.route("/putzplan", methods=["POST", "GET"])
def putzplan():
    """create putzplan list over last 4 weeks open/create lookupfile
    on GET: read the lookupfile for the checked boxes
    on POST: writes the current checked boxes"""
    lufile = path.expanduser("~/checkboxes.txt")
    pplist = pp.main(datetime.now().date().isocalendar(), 4)
    if not path.exists(lufile):
            with open(lufile, "w"): pass
    with open(lufile, "r") as lastchange:
        if request.method == "GET":
            checkarray = [lol.rstrip() for lol in lastchange.readlines()]
            return render_template("putzplan.html", mbwlist=pp.MITBEWOHNER, plans=pplist, checkarray=checkarray)
        if request.method == "POST":
            for checkbox in request.form:
                lastchange.write(checkbox + "\n")
            return redirect(url_for("putzplan"))

@app.route("/scoretracker")
def scoretracker():
    """check if the mongoDB is reachable from current device
    and load the home.html template"""
    try:
        mdb.get_serverstatus()
        flash("Server online.", "info")
    except:
        flash("Trouble reaching Database.", "error")
    return render_template("scoretracker.html")

@app.route("/scoretracker/submit", methods=["POST", "GET"])
def st_submit():
    """on GET: load player and game table and fill the dropdown lists
    on POST: handle the three possible post methods"""
    if request.method == "GET":
        players = list(mdb.read_table("people"))
        games = mdb.read_table("games")
        return render_template("st_submit_game.html", players=players, games=games)
    if request.method == "POST":
        if not request.is_json: #form data
            update_gamedata(request.form["sgame"])
            update_playerdata(request.form)
            create_matchup(request.form)
            flash("Success.", "info")
        if request.is_json: #from scipt.js
            if request.headers.get("Js-Function", type=str) == "addGame":
                create_game(request.get_json()["game_name"])
                flash("Game created.", "info")
            elif request.headers.get("Js-Function", type=str) == "addPlayer":
                create_player(request.get_json()["player_name"])
                flash("Player created.", "info")
        return redirect(url_for("st_submit"))

@app.route("/scoretracker/stats")
def st_stats():
    """on GET: load data from database and render template
    on POST: ..."""
    players = mdb.read_table("people")
    games = mdb.read_table("games")
    matchups = mdb.read_table("people")
    return render_template("st_stats.html", players=players, games=games, matchups=matchups)

def create_game(game_name):
    """create a game in the games table with the dict from olib"""
    mdb.create_data(olib.Game(game_name).__dict__, "games")
    return 0

def create_player(player_name):
    """create a player in the player table with the dict from olib"""
    mdb.create_data(olib.Player(player_name).__dict__, "people")
    return 0

def update_gamedata(game_id):
    """set the gamedata and update it in the game table"""
    game_data = mdb.read_item("games", game_id)
    game_data["times_played"] += 1
    game_data["last_played"] = datetime.now()
    mdb.update_data(game_data, "games")
    return 0

def update_playerdata(form_data):
    """set the playerdata and update it in the database"""
    for player in form_data.getlist("team1"):
        player_data = mdb.read_item("people", player)
        player_data["times_played"] += 1
        player_data["last_played"] = datetime.now()
        if int(form_data["score_team1"]) > int(form_data["score_team2"]):
            player_data["wins"] += 1
        elif int(form_data["score_team1"]) < int(form_data["score_team2"]):
            player_data["losses"] += 1
        mdb.update_data(player_data, "people")
    for player in form_data.getlist("team2"):
        player_data = mdb.read_item("people", player)
        player_data["times_played"] += 1
        player_data["last_played"] = datetime.now()
        if int(form_data["score_team1"]) < int(form_data["score_team2"]):
            player_data["wins"] += 1
        elif int(form_data["score_team1"]) > int(form_data["score_team2"]):
            player_data["losses"] += 1
        mdb.update_data(player_data, "people")
    return 0

def create_matchup(form_data):
    """create a matchup from the formdata and upload it to the matchups table"""
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

if __name__ == "__main__":
    usage_desc = """
    Usage: {0} <local or license_file> <database_name>
    Note: Please give the complete link to the license file /home/...
    """.format(argv[0])
    if len(argv) == 3:
        if argv[1] == "local":
            import mDB_CRUD_32 as mdb
            mdb.LICENSE_STRING = "localhost"
        else:
            import mDB_CRUD_64 as mdb
            mdb.LICENSE_STRING = mdb.get_credentials(argv[1])
        mdb.CLIENT = mdb.connect_client()
        mdb.DB = mdb.set_db(argv[2])
        app.run(debug=True, host="0.0.0.0")
    else: print(usage_desc)
