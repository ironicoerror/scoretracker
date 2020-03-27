#!/usr/bin/python3

import trackerlib as tl 

def show_players():
    print("Players currently listed:")
    for _player in tl.PLAYER_LIST:
        print(_player.name)
    return 0

def show_games():
    print("Games currently listed:")
    for _game in tl.GAMES_LIST:
        print(_game.name)
    return 0

def submit_game(team1, team2, game_played, final_score):
    tl.game_played.played()
    return 0 

def create_matchup(team1, team2):
    pass

def update_matchup(team1, team2):
    pass

if __name__ == "__main__":
    tl.create_player("Thorsten Tester") 
    print(tl.PLAYER_LIST[0].__dict__)
    tl.PLAYER_LIST[0].won(True)
    print(tl.PLAYER_LIST[0].__dict__)
    print("\n\n------------Success-------------")
