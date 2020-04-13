#! /usr/bin/python3

from os import path

current_location = str(path.dirname(path.abspath(__file__)) + "/") 
class ImportFromFile:
    def __init__(self, credentials_file_name, path_to=current_location):
        self.filename, self.file_path = credentials_file_name, path_to

    def import_direct(self):
        try:
            fh = open(self.filename, "r")
            cred_string = fh.read().rstrip()
            fh.close()
        except FileNotFoundError:
            print("Credential file not found, please create one.")
            raise FileNotFoundError
        return cred_string

    def import_relative(self):
        try:
            fh = open(self.file_path + self.filename, "r")
            cred_string = fh.read().rstrip()
            fh.close()
        except FileNotFoundError:
            print("Credential file not found, please create one.")
            raise FileNotFoundError
        return cred_string
