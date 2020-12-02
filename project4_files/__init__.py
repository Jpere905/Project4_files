import urllib

from flask import Flask
from flask_pymongo import PyMongo
from project4_files import main_functions



cred_dict = main_functions.read_from_file("project4_files/JSON_Documents/credentials.json")
username = cred_dict["username"]
password = urllib.parse.quote_plus(cred_dict["password"])

app = Flask(__name__)
app.config["SECRET_KEY"] = "a strong secret key"
app.config["MONGO_URI"] = \
    "mongodb+srv://{0}:{1}@learningmongodb.ckcw7.mongodb.net/db?retryWrites=true&w=majority".format(username, password)

mongo = PyMongo(app)


# this has to be down here for some reason cant really figure out why
# something to do with a cyclic call from __init__.py
from project4_files import routes