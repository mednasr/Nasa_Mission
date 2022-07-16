# import necessary libraries
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_pymongo import PyMongo
import pymongo
import scrape_nasa
from bson.json_util import dumps
import csv
import requests

# create instance of Flask app
app = Flask(__name__)

# Use PyMongo to establish Mongo connection

mongo = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.md8r6.mongodb.net/?retryWrites=true&w=majority")
db = mongo['nasa_data']
status = "Not connected"



# create route that renders index.html template
@app.route("/home")
def home():
    global status

    #nasa_data = scrape_nasa.scrape()
    if ( status == "Not connected"):
        #print(" 1 Python is " + status)

        # Return template and data if not loggedIn
        return render_template('login.html')

    elif ( status == "connected"):
        status = " Not connected"
        #print("2 Python is " + status)

    # Find one record of data from the mongo database
    # nasa_data = mongo.db.collection.find_one()

    # Run the scrape function
    nasa_data = scrape_nasa.scrape()

    # Return template and data
    return render_template("index.html", nasa=nasa_data)


# Route for handling the scrapping function if you want to have it as a seperate logic
@app.route("/scrape")
def scrape():

    # Run the scrape function
    nasa_data = scrape_nasa.scrape()

    # Insert the record
    mongo.db.collection.update_one({}, {"$set": nasa_data}, upsert=True)

    # Redirect back to home page
    return redirect("/home")


# Route for handling the API get all data call logic
@app.route("/get_all_data", methods = ['GET'])
def get_all_data():
    try:
        # Find a record of data from the mongo database
        data = mongo.db.collection.find()

        # Return the data
        return dumps(data)
    except Exception as e:
        return dumps({'error' : str(e)})



# Route for handling the save to csv file logic
@app.route("/save")
def save():
    # Find a record of data from the mongo database
    nasa_data = mongo.db.collection.find()

    # Find one record of data from the mongo database
    #mars_data = mongo.db.collection.find_one()

    # Return template and data
    return Response(dumps(nasa_data), headers={"Content-disposition": "attachment; filename=nasa_data.csv"})


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    global status
    status = "Not conected"
    #print("Python is " + status )
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            status = " conected"
            return redirect(url_for('home'))

    # Return template and data
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)

