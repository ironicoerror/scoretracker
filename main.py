#!/usr/bin python3

from flask import Flask, render_template, url_for, redirect
from datetime import datetime

server_starttime = datetime.now()
player_list = []
games_list = []
class Game:
    def __init__(self, name):
        self.name = name
        self.times_played = 0
        self.created_on = datetime.now()
        games_list.append(self)
    def called(self):
        self.times_played += 1
        self.last_played = datetime.now()
     
class Player:
    def __init__(self, name):
        self.name = name
        self.times_played = 0
        self.created_on = datetime.now()
        player_list.append(self)
    def called(self):
        self.times_played += 1
        self.last_played = datetime.now()
def create_player(player_name):
    new_player = Player(player_name)
    player_list.append(new_player)
def create_game(game_name):
    new_game = Game(game_name)
    games_list.append(new_game)
def show_players():
    print("Players currently listed:")
    for __player in games_list:
        print(__player.name)
def show_games():
    print("Games currently listed:")
    for __game in games_list:
        print(__game.name)
fifa = Game("FIFA")
forza = Game("Forza Horizon")
show_games()
print("\n\n------------Success-------------")
