#!/usr/bin python3

from datetime import datetime

server_starttime = datetime.now()
PLAYER_LIST = []
GAMES_LIST = []

class Game:
    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()
        self.times_played = 0
        GAMES_LIST.append(self)
    def played(self):
        self.last_played = datetime.now()
        self.times_played += 1
     
class Player:
    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()
        self.times_played = 0
        self.wins = 0
        PLAYER_LIST.append(self)
    def won(self, win):
        self.last_played = datetime.now()
        self.times_played += 1
        if win is True: 
            self.wins += 1

def create_player(player_name):
    new_player = Player(player_name)
    return 0

def create_game(game_name):
    new_game = Game(game_name)
    return 0

if __name__ == "__main__":
    print("\n\n------------Success-------------")

