#! /usr/bin/python3
"""connect to a mongoDB created by Mongo Atlas Free"""

import pymongo
from credentials_import import ImportFromFile
from datetime import datetime
from random import randint
from sys import stdout, stderr
from os import path
from bson.objectid import ObjectId

#licensing
path_to_license = str(path.dirname(path.abspath(__file__))) + "/license_files/"
license_string = ImportFromFile("cred_mongoDB.lic", path_to_license).import_string()

#database init
client = pymongo.MongoClient(license_string)
database_name = "scoretracker_test"
db = client[database_name]

def get_serverstatus():
    """returns the Server Status of the mongo DB Client"""
    return db.command("serverstatus")
#CRUD
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
    cursor = db[collection].find({})
    return cursor


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
    names = ["Tobi", "Nico", "Laura", "Florian", "Paul", "Raffi"]
    for x in range(0,len(names)):
        test_object ={
                    'name' : names[x],
                    'creation_date' : datetime.now(),
                    'times_played' : randint(0, 100),
                    'last_played' : datetime.now()
        }
        last_response = create_data(test_object, collection)
    return 0

if __name__ == "__main__":
    #pretty print of the specified table
    data = read_table("people")
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
