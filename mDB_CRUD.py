#! /usr/bin/python3
"""connect to a mongoDB created by Mongo Atlas Free"""

from sys import stdout, stderr, argv
import pymongo
from credentials_import import ImportFromFile
from datetime import datetime
from random import randint, choice, choices
from os import path
from bson.objectid import ObjectId
usage_desc = """Usage:
{0} <list> to list the present dbs.
{0} <db_name> <status> to print the server status.
{0} <db_name> <list> to list the tables.
{0} <db_name> <read> <table> to read a tables content""".format(argv[0])
#licensing
path_to_license = str(path.dirname(path.abspath(__file__))) + "/license_files/"
license_string = ImportFromFile("cred_mongoDB.lic", path_to_license).import_string()

#database init
client = pymongo.MongoClient(license_string)
db = client["scoretracker_test"]

def get_serverstatus():
    """returns the Server Status of the mongo DB Client"""
    try:
        db.command("serverstatus")
    except:
        return 1 
    return 0 

"""------------------Here begins the CRUD----------------------"""
def create_data(upload_object, collection):
    """writes one dictionary object to the collection specified"""
    if type(upload_object) == dict:
        response = db[collection].insert_one(upload_object)
        return response
    else:
        print("Your data has to be of dict type.") 
        raise TypeError
def read_table(collection):
    """reads the whole collection table specified"""
    if db[collection].count_documents({}) != 0:
        return db[collection].find({})
    else:
        raise Exception("Table not found. Check spelling. Valid Tables are:\n{0}".format([table["name"] for table in  db.list_collections()]))
def read_item(collection, unique_id):
    """reads an item in the collection from its ID and returns it as a dict"""
    response = db[collection].find_one({"_id" : ObjectId(unique_id)})
    return response
def read_matchup(collection, field, searchstring):
    """reads all items in the collection that match a certain string and returns it as a dict"""
    if field == "_id":
        searchstring = ObjectId(searchstring)
    response = db[collection].find_one({field : ObjectId(unique_id)})
    return response
def update_data(update_object, collection):
    """searches for an entryid in the specified collection and updates it"""
    response = db[collection].update_one(
            {"_id": update_object["_id"]}, {"$set": update_object})
    return response

def delete_data(del_object, collection):
    """searches for an entryid and deletes the entry"""
    response = db[collection].delete_one({"_id": del_object["_id"]})
    return response

def create_sample_data(collection):
    """writes a specified num of datapoints as sample to collection specified"""
    game_table = read_table("games")
    games = []
    for game in game_table:
        games.append(game["name"])
    player_table = read_table("people")
    ids = []
    for player in player_table:
        ids.append(player["_id"])
    for x in range(0,10):
        test_object ={
                    'creation_date' : datetime.now(),
                    'game' : choice(games),
                    'team1' : choices(ids, k=2),
                    'team2' : choices(ids, k=2),
                    'score_team1' : randint(1,10),
                    'score_team2' : randint(1,10)
        }
        last_response = create_data(test_object, collection)
    return 0

if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] == "list":
            for database in client.list_databases():
                print(database["name"])
    elif len(argv) > 2:
        db = client[argv[1]]
        if len(argv) == 3:
            if argv[2] == "status" or "s":
                print(get_serverstatus())
            elif argv[2] == "list" or "l":
                for table in db.list_collections():
                    print(table["name"])
        elif len(argv) == 4:
            if argv[2] == "read" or "r":
                #pretty print of the specified table
                data = read_table(argv[3])
                i = 0
                for entry in data:
                    if i == 0:
                        for key, value in entry.items():
                            print(key, " " * (len(str(value))-len(str(key))), end="\t") 
                            i += 1
                        print("\n")
                    for key, value in entry.items():
                        print(value, end="\t")
                    print("\n")
    else:
        print(usage_desc) 
