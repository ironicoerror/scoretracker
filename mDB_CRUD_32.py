#!/usr/bin/python3
"""connect to a local mongoDB using pymongo 3.4.0 cause raspi only supports the 32-bit version

functions that changed:
find_One - find_one
insert_One - insert
update_One - update
remove_One - remove
"""
from sys import stdout, stderr, argv
import pymongo
from datetime import datetime
from random import randint, choice, choices
from os import path
from bson.objectid import ObjectId

#licensing
LICENSE_STRING = None 
CLIENT = None
DB = None

def get_credentials(license_file):
    """copies credential string from file given"""
    print(license_file)
    with open(license_file, "r") as fh:
        cred_string = fh.read().rstrip()
    return cred_string

def connect_client():
    """sets up a client conncetion to the database"""
    if LICENSE_STRING == None:
        stderr.write("No License information given. Edit LICENSE_STRING.")
    else:
        return pymongo.MongoClient(LICENSE_STRING)

def set_db(db_name):
    """selects the database from mongodb"""
    return CLIENT[db_name]

def get_serverstatus():
    """returns the Server Status of the mongo DB Client"""
    return DB.command("ismaster")

def create_data(upload_object, collection):
    """writes one dictionary object to the collection specified"""
    if type(upload_object) != dict:
        stderr.write("Data has to be dict type.")
    else:
        return DB[collection].insert(upload_object)

def read_table(collection):
    """reads the whole collection table specified"""
    return DB[collection].find({})

def read_item(collection, unique_id):
    """reads an item in the collection from its ID and returns it as a dict"""
    return DB[collection].find_one({"_id" : ObjectId(unique_id)})

def read_matchup(collection, field, searchstring):
    """reads all items in the collection that match a certain string and returns it as a dict"""
    if field == "_id": searchstring = ObjectId(searchstring)
    return DB[collection].find_one({field : searchstring})

def update_data(update_object, collection):
    """searches for an entryid in the specified collection and updates it"""
    object_id = update_object.pop("_id") # 32-bit version of mongodb doesn't allow manipulation of the _id tag 
    return DB[collection].update({"_id": object_id}, {"$set": update_object})

def delete_data(del_object, collection):
    """searches for an entryid and deletes the entry"""
    return DB[collection].remove({"_id": del_object["_id"]})

def main(argumentlist):
    """mongo adaptation to python using pymongo like the mongo shell. found out about it a little to late"""
    global LICENSE_STRING, CLIENT, DB
    usage_desc = """Usage:
    {0} <lic_file/local> <list> to list the databases on the server.
    {0} <lic_file/local> <list> <db_name> to list the tables.
    {0} <lic_file/local> <list> <db_name> <table> to list a tables content.
    {0} <lic_file/local> <status> <db_name> to print the database status.
    """.format(argumentlist[0])
    commands = ["local", "list", "status"]
    if (len(argumentlist) > 2) and (argumentlist[2] in commands):
        if argumentlist[1] == "local":
            LICENSE_STRING = "localhost"
        else:
            LICENSE_STRING = get_credentials(argumentlist[1])
        CLIENT = connect_client()
        #list
        if argumentlist[2] == "list":
            if len(argumentlist) == 3:
                print([database["name"] for database in CLIENT.list_databases()])
            elif len(argumentlist) == 4:
                DB = set_db(argumentlist[3])
                print([table["name"] for table in DB.list_collections()])
            elif len(argumentlist) == 5:
                DB = set_db(argumentlist[3])
                print([doc for doc in read_table(argumentlist[4])])
        #status
        if argumentlist[2] == "status":
            DB = set_db(argumentlist[3])
            print("Connected") if not get_serverstatus() else print("No connection")
    else:
        print(usage_desc) 
if __name__ == "__main__":
    main(argv)
