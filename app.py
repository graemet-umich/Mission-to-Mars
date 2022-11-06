# 10.5.1 Use Flask to Create a Web App

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# set up our Flask routes: one for the main HTML page everyone 
# will view when visiting the web app, and one to actually scrape 
# new data using the code we've written
@app.route("/")
def index():
    # find the "mars" collection in our database
    mars = mongo.db.mars.find_one()
    # use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

# set up our scraping route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   # referencing the scrape_all function in the scraping.py 
   # file exported from Jupyter Notebook
   mars_data = scraping.scrape_all()
   # update the database, $set means modify, 
   # upsert=True means create a new document if one doesn't already exist, 
   # and new data will always be saved
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
   