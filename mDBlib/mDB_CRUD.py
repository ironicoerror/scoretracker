#! /usr/bin/python3
"""connect to a mongoDB created by Mongo Atlas Free"""

import pymongo
from credentials_import import ImportFromFile
from datetime import datetime
from random import randint
from sys import stdout, stderr
from os import path
from bson.objectid import ObjectId

#database init
path_to_license = str(path.dirname(path.abspath(__file__))) + "/license_files/" 
client = pymongo.MongoClient(ImportFromFile("cred_mongoDB.lic", path_to_license).import_string())
database_name = "test"
db = client[database_name]

def get_serverstatus():
    return db.command("serverstatus")

def write_sample_data(num, collection):
    response = []
    for x in range(0,num):
        test_object ={
                    'Date' : datetime.now(),
                    'Temp' : randint(-5, 30),
                    'Humi' : randint(20, 80)
        }
        last_response = write_data(test_object, collection)
    return last_response

def write_data(upload_object, collection):
    if type(upload_object) == dict:
        response = db[collection].insert_one(upload_object)
        return response
    else:
        raise TypeError

def read_cursor(collection):
    cursor = db[collection].find({})
    return cursor

if __name__ == "__main__":
    #print(write_sample_data(5, "testcollection"))
    for _ in read_cursor("testcollection"):
        if datetime.date(_["Date"]) == datetime.date(datetime.today()):
            print(_)
   
