from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

# Create Flask
app = Flask(__name__)

#get connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

@app.route("/")
def home():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mdata = mars_data)

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    m_data = scrape.scrape()
    mars_data.update({}, m_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)