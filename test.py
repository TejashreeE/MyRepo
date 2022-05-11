from multiprocessing.dummy import DummyProcess
from pydoc import doc
import re
from unicodedata import name
from flask import Flask, render_template, redirect, request, session, url_for
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
from numpy import equal
#from flask_login import login_required
from pymongo import MongoClient
from bson import ObjectId
from datetime import date, datetime
import bcrypt
import sys
import subprocess
import shlex

myclient = MongoClient("mongodb://root:N5tfgb9QExIGYXIq@cluster0-shard-00-00.e4swe.mongodb.net:27017,cluster0-shard-00-01.e4swe.mongodb.net:27017,cluster0-shard-00-02.e4swe.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-biz1ll-shard-0&authSource=admin&retryWrites=true&w=majority")

def get_db():
    client = myclient
    db = client["Customer"]
    print ("Connected")
    return db

title = "To Save requirements from Customer"
heading = "Customer Requirements"

db = get_db()
records = db.register
todos = db.todo



#for doc in todos.find({}): 
#    met = doc['name']
#db.items.find_all({"key, value": {"$in": [("a", "b"), ("x", "y")]}})
#met = todos.find({"key, value": {"$in": [("name", "Environment", "Region")]}})
Name = "Dummy"
##met = db.todo.find( { name: { "$not": [ Name ] } }, { "_id": 0 } )
#met = todos.find({"name": "Prashant", "Environment": "Production", "Region": "North #Europe"})
##my = met[1]
#print(met)
#
#db.todo.find( { name: { "$in": [ Name ] } }, { "_id": 0 } );

my = db.todo.find( { "name": { "$not": re.compile("^Dummy.*") } } ).sort( [( '_id' , -1 )] ).sort( { date: -1 } )
print(my)

db.todo.find({ 'name':{'$regex':Name}}).sort( [( '_id' , -1 )] ).sort( { date: -1 } )

db.todo.find().sort( { date: -1 } )

#db.todo.find()._addSpecial( "$orderby", { date : -1 } )
#
#db.todo.find( { $query: {}, $orderby: { date : -1 } } )