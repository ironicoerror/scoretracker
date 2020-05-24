# README.md

# Description:

gamescore tracker with a database running on mongodb 
the application will run on localhost and can be accessed through browser 


# Installation notes:
Installing the python packages:

`pip3 install -r requirements.txt`

Installing the Pymongo drivers for the database application:

On Fedora:

`sudo dnf install python3-pymongo`

On Debian/Ubuntu:

`sudo apt install python3-pymongo`


# Troubleshooting:
running a web-based mongodb server like atlas-mongodb:
connection issues:
- check of you whitelisted your IP:
    - type `curl ifconfig.me` to terminal
    - goto https://www.mongodb.com/cloud and login
    - whitelist this IP on tab "network access"

