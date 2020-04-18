#!/usr/bin/python3
"""connect to a mongoDB created by Mongo Atlas Free"""

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
    with open(license_file, "r") as fh:
        cred_string = fh.read().rstrip()
    return cred_string

def connect_client():
    """sets up a client conncetion to the database"""
    if LICENSE_STRING == None:
        raise Exception("No License information given. Edit LICENSE_STRING.")
    else:
        return pymongo.MongoClient(LICENSE_STRING)

def set_db(db_name):
    """selects the database from mongodb"""
    return CLIENT[db_name]

def get_serverstatus():
    """returns the Server Status of the mongo DB Client"""
    return DB.command("serverstatus")

def create_data(upload_object, collection):
    """writes one dictionary object to the collection specified"""
    if type(upload_object) != dict:
        raise TypeError("Data has to be dict type.")
    else:
        return DB[collection].insert_one(upload_object)

def read_table(collection):
    """reads the whole collection table specified"""
    return DB[collection].find({})

def read_item(collection, unique_id):
    """reads an item in the collection from its ID and returns it as a dict"""
    return DB[collection].find_one({"_id" : ObjectId(unique_id)})

def read_matchup(collection, field, searchstring):
    """reads all items in the collection that match a certain string and returns it as a dict"""
    if field == "_id": searchstring = ObjectId(searchstring)
    return DB[collection].find_one({field : ObjectId(unique_id)})

def update_data(update_object, collection):
    """searches for an entryid in the specified collection and updates it"""
    return DB[collection].update_one({"_id": update_object["_id"]}, {"$set": update_object})

def delete_data(del_object, collection):
    """searches for an entryid and deletes the entry"""
    return DB[collection].delete_one({"_id": del_object["_id"]})

if __name__ == "__main__":
    usage_desc = """Usage:
    {0} <lic_file> <list> to list the databases on the server.
    {0} <lic_file> <list> <db_name> to list the tables.
    {0} <lic_file> <list> <db_name> <table> to list a tables content.
    {0} <lic_file> <status> <db_name> to print the database status.
    """.format(argv[0])
    commands = ["list", "status"]
    if (len(argv) > 2) and (argv[2] in commands):
        LICENSE_STRING = get_credentials(argv[1])
        CLIENT = connect_client()
        #list
        if argv[2] == "list":
            if len(argv) == 3:
                print([database["name"] for database in CLIENT.list_databases()])
            elif len(argv) == 4:
                DB = set_db(argv[3])
                print([table["name"] for table in DB.list_collections()])
            elif len(argv) == 5:
                DB = set_db(argv[3])
                print([doc for doc in read_table(argv[4])])
        #status
        if argv[2] == "status":
            DB = set_db(argv[3])
            print("Connected") if not get_serverstatus() else print("No connection")
    else:
        print(usage_desc) 
