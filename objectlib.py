#!/usr/bin python3

from datetime import datetime

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
        return 0
    def edit_name(self, name):
        self.name = name
        return 0
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
        return 0
    def edit_name(self, name):
        self.name = name
        return 0
#section for testing
if __name__ == "__main__":
    Player("Nico")
    print(PLAYER_LIST)
    print(PLAYER_LIST[0].__dict__)
    print("\n\n------------Success-------------")

