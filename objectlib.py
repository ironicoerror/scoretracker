#!/usr/bin/env python3

from datetime import datetime

PLAYER_LIST = []
GAMES_LIST = []


class Game:
    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()
        self.times_played = 0
        self.last_played = None
        GAMES_LIST.append(self)


class Player:
    def __init__(self, name):
        self.name = name
        self.created_on = datetime.now()
        self.times_played = 0
        self.wins = 0
        self.losses = 0
        self.last_played = None
        PLAYER_LIST.append(self)


# section for testing
if __name__ == "__main__":
    Player("Nico")
    print(PLAYER_LIST)
    print(PLAYER_LIST[0].__dict__)
    print("\n\n------------Success-------------")
