#!/usr/bin/python3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
import objectlib as olib 
import mDB_CRUD as mdb

app = Flask(__name__, static_url_path="/static")
app.secret_key = b';\xf5!\xa7\xfa\xba\x9b\x94P\x15\n.V\xb9\x0c\xe7'

@app.route("/")
@app.route("/home")
def home():
    online = not mdb.get_serverstatus()
    if online:
        flash("Server online.", "info")
    else:
        flash("Trouble reaching Database", "error")
    return render_template("home.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        if len(request.form) == 3:
            try:
                for player in request.form.getlist("team1"):
                    update_playerdata(player)
                for player in request.form.getlist("team2"):
                    update_playerdata(player)
                flash("Success.", "info")
            except:
                flash("Trouble reaching database.", "error")
            finally:
                return redirect(url_for("submit"))
        else:
            flash("Please enter all information.", "error")
            return redirect(url_for("submit")) 
    if request.method == "GET":
        players = list(mdb.read_table("people"))
        return render_template("submit_game.html", players=players)

def update_playerdata(player_id):
    player_data = mdb.read_item("people", player_id)
    player_data["times_played"] += 1
    player_data["last_played"] = datetime.now()
    response = mdb.update_data(player_data, "people")
    return 0

#test section
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    print("\n\n------------Success-------------")
