from email import message
from email.message import Message
from pydoc import doc
import re
from tabnanny import check
from unicodedata import name
from flask import Flask, render_template, redirect, request, session, url_for
# The Session instance is not used for direct access, you should always use flask.session
from flask_session import Session
#from logging import FileHandler, WARNING
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AJDJRJS24$($(#$$33--'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def redirect_url():
    return request.args.get('next') or \
        request.referrer or ('index')


def getNextIP(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    address_space = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        address_space = doc["Address_Space"]
        
    #p = 1	
    listOfrange = address_space.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)

def getMongoSub(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    mongo_subnet = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        mongo_subnet = doc["Mongo_Subnet"]
    
    #p = 1	
    listOfrange = mongo_subnet.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)

def getREL_IDSub(EnvType,p):
    s = '.'
    #cursor = db.todo.find().sort({"_id":-1}).limit(1)
    #key = EnvType
    #refer = "Environment"    
    relid_subnet = ""
    for doc in todos.find({"Environment": EnvType},{"_id":0}).sort("_id",-1).limit(1):
        relid_subnet = doc["Rel-ID_Subnet"]
    
    #p = 1
    listOfrange = relid_subnet.split(s)
    listOfrange[p] = str(int(listOfrange[p])+1)
    return s.join(listOfrange)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/register", methods=["POST", "GET"])
def register():

    today = date.today()
    current_time = str(today)

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email-id")
        passwd1 = request.form.get("passwd1")
        passwd2 = request.form.get("passwd2")

        #validation if records already present in the database
        username_found = records.find_one({"username": username})
        email_found = records.find_one({"email": email})

        if username_found:
            message = 'username already exists'
            return render_template('register.html', message=message)

        if email_found:
            message = 'email already exists'
            return render_template('register.html', message=message)

        if passwd1 != passwd2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)

        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(passwd2.encode('utf-8'), bcrypt.gensalt())
            #Save records to db
            user_input = {'username': username, 'created date': current_time, 'email': email, 'password': hashed}
            records.insert_one(user_input)
            #return render_template('registered.html', username=username)
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #validate user name and password
        username = request.form.get("username")
        passwd = request.form.get("password")
        session["username"] = request.form.get("username")

        # Check if username present in database
        username_found = records.find_one({"username": username})
        
        if username_found:
            username_val = username_found['username']
            passwordcheck = username_found['password']

            #encode the password and check if it matches
            if bcrypt.checkpw(passwd.encode('utf-8'), passwordcheck):
                session["username"] = username_val
                return redirect(url_for("dashboard"))
            else:
                message = 'Please enter correct password'
                return render_template("login.html", message=message)
        else:
            message = 'username not found'
            return render_template("login.html", message=message)
        
        #if request.form.get("username") == "Amit":
        #else:
        #    return render_template("register.html")
    return render_template("login.html")     


@app.route('/dashboard')
def dashboard():

    todos_l = todos.find( { "name": { "$not": re.compile("^Dummy.*") } } ).sort( [( '_id' , -1 )] ).sort( 'date', -1 )
    #todos_l = todos.find().sort( [( '_id' , -1 )] ).sort( 'date', -1 )
    #records_1 = records.find({})
    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a1 = "active"
    if "username" in session:
        username = session["username"] 
        return render_template('dashboard.html', username=username, a1=a1, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)
    else:
        return redirect(url_for("login"))


@app.route("/list")
def lists():
    
    todos_l = todos.find()

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a2 = "active"
    return render_template('dashboard.html', a2=a2, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/uncompleted")
def tasks():
   
    # Display the Uncompleted Tasks
    print('Calling dashboard.html')
    todos_l = todos.find({"done": "no"})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])
    print('calling dashboard.html')
    a3 = "active"
    return render_template('dashboard.html', a3=a3, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/completed")
def completed():
    
    # Display the Completed Tasks
    todos_l = todos.find({"done": "yes"})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a4 = "active"
    return render_template('dashboard.html', a4=a4, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes)


@app.route("/done")
def done():
    
    # Done-or-not ICON
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})
    if(task[0]["done"] == "yes"):
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "no"}})
    else:
        todos.update({"_id": ObjectId(id)}, {"$set": {"done": "yes"}})
    redir = redirect_url()

    return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
    
    if "username" in session:
        username = session["username"] 

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    a5 = "active"
    
    #todos_l = db.todo.find({ 'name':{'$regex':Name}}).sort( [( 'date' , -1 )] )
    #todos_l = todos.find( { "name": { "$not": re.compile("^Dummy.*") } } ).sort( { date: -1 } )
    name = request.form.get("name")
    envtype = request.form.get("environment")
    date = request.form.get("date")
    region = request.form.get("region")
    deletion_date = request.form.get("deletion_date")
    
    todos_l = todos.find( { "name": { "$not": re.compile("^Dummy.*") } } ).sort( [( '_id' , -1 )] ).sort( 'date', -1 )
    
    #todos_l =  db.todo.find().sort( [( '_id' , -1 )] ).sort( 'date', -1 )
    #validation if Customer name already present in the database
    name_found = todos.find_one({"name": name, "Environment": envtype, "Region": region})
    
    #for doc in todos.find({"name": name}):
    #for doc in todos.find({}):
    #for doc in todos.find().sort({"_id":1}):
    #for doc in todos.find({"name": name},{"Environment": envtype},{"Region": region}):
    #for doc in todos.find({"name": name},{"_id":0}).sort("_id",-1).limit(1):
        #myname = doc["name"]
        #myenv = doc['Environment']
        #myregion = doc['Region']
        
    if name_found:
        message = "Customer Name already exists..!"
        return render_template("dashboard.html", a5=a5, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes, message=message)

    #if name_found:
    #    message = 'Customer Name already exists..!'
    #    return render_template('dashboard.html', a5=a5, todos=todos_l, t=title, h=heading, regions=regions, envtypes=envtypes, message=message)
    
    
    elif envtype == "Development":
        newaddressspace = getNextIP(envtype,1)
        print(newaddressspace)
        NewMongoSubnet = getMongoSub(envtype,1)
        print(NewMongoSubnet)

        #subprocess.call(shlex.split(f"./0-Start.sh {name} {envtype} \"{region}\"{newaddressspace} {NewMongoSubnet}"))

        todos.insert_one({ "username": username, "name": name, "Environment": envtype,
                     "date": date, "Deletion Date": deletion_date, "Region": region, "Address_Space":newaddressspace, "Mongo_Subnet":NewMongoSubnet, "done": "no"})

        #subprocess.call(shlex.split(f"./0-Start.sh {name} {envtype} \"{region}\" {newaddressspace} {NewMongoSubnet}"))

    else:
        newaddressspace = getNextIP(envtype,1)
        print(newaddressspace)
        NewMongoSubnet = getMongoSub(envtype,1)
        print(NewMongoSubnet)
        NewRelIDSubnet = getREL_IDSub(envtype,1)
        print(NewRelIDSubnet)

        #subprocess.call(shlex.split(f"/home/azureuser/relid-saas/Dash-8april/0-Start.sh {name} {envtype} \"{region}\" {newaddressspace} {NewMongoSubnet} {NewRelIDSubnet}"))

        todos.insert_one({ "username": username, "name": name, "Environment": envtype,
                     "date": date, "Deletion Date": deletion_date, "Region": region, "Address_Space":newaddressspace, "Mongo_Subnet":NewMongoSubnet, "Rel-ID_Subnet":NewRelIDSubnet, "done": "no"})

        #subprocess.call(shlex.split(f"/home/azureuser/relid-saas/Dash-8april/0-Start.sh #{name} {envtype} \"{region}\" {newaddressspace} {NewMongoSubnet} #{NewRelIDSubnet}"))
        
    # print(environment)
    # return redirect('index.html', regions=regions, answers=regions)
    #rc = subprocess.call("./script.sh")
    #subprocess.check_call(['./script.sh', 'name', 'region', 'envtype'])

    #return redirect("/list")
    return redirect("/dashboard") 

@app.route("/remove")
def remove():

        today = date.today()
        #date_format = date.strftime("%d/%m/%Y")
        deletion_date = str(today)
    
    # Deleting a Task with various references
        #key = request.values.get("_id")
        #todos.update_one({"Deletion Date": deletion_date})

        id = request.values.get("_id")
        todos.update_one({"_id": ObjectId(id)}, {'$set': {
                     "Deletion Date": deletion_date}})
        return redirect(url_for("dashboard"))

    
@app.route("/update")
def update():
    
    id = request.values.get("_id")
    task = todos.find({"_id": ObjectId(id)})

    regions = []
    cursor = db.regions.find({}, {"region": 1})
    for document in cursor:
        regions.append(document['region'])        # <- append to the list

    envtypes = []
    cursor = db.envtypes.find({}, {"envtype": 1})
    for document in cursor:
        envtypes.append(document['envtype'])

    return render_template('update.html', tasks=task, h=heading, t=title, regions=regions, envtypes=envtypes)


@app.route("/action3", methods=['POST', 'GET'])
def action3():
    
    # Updating a Task with various references
    name = request.values.get("name")
    envtype = request.values.get("environment")
    print("The type is : ", type(envtype))
    date = request.values.get("date")
    region = request.values.get("region")
    id = request.values.get("_id")
    todos.update_one({"_id": ObjectId(id)}, {'$set': {
                     "name": name, "Environment": envtype, "date": date, "Region": region}})
    return redirect("/")


@app.route("/search", methods=['GET'])
def search():
    
    # Searching a Task with various references

    key = request.values.get("key")
    refer = request.values.get("refer")
    if(key == "_id"):
        todos_l = todos.find({refer: ObjectId(key)})
    else:
        todos_l = todos.find({refer: key})
    return render_template('searchlist.html', todos=todos_l, t=title, h=heading)


@app.route("/logout")
def logout():
	session["name"] = None
	return redirect("/")


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    sys.stdout.write("%s\n", app('environ', 'start_response'))
