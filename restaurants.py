from flask import render_template, Blueprint, request
from pymongo import MongoClient
from flask_cors import CORS
import certifi

restaurants = Blueprint('restaurants', __name__)

CORS(restaurants)

client = MongoClient(f"mongodb+srv://sc_delaEmi:u2JsEd0nzYssgaMd@cluster0.8qczawe.mongodb.net/test?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client['test']
res = db.restaurants


@restaurants.route("/restaurants")
def restaurant_list():
    arr = list(res.find({}, {"_id":0, "location":1, "hours":1, "link":1, "description":1, "name":1}))
    return render_template("./locations.html", title="locations", arr=arr)

@restaurants.route("/filter_restaurants" , methods=['POST'])
def restaurant_filter():
    arr = list(res.find({ "category": request.form.get('filterRestaurants')}, {"_id":0, "location":1, "hours":1, "link":1, "description":1, "name":1}))
    return render_template("./locations.html", title="locations", arr=arr)
