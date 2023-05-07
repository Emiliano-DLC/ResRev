from flask import render_template, Blueprint, request
from pymongo import MongoClient
from flask_cors import CORS
import certifi

restaurants = Blueprint('restaurants', __name__)

CORS(restaurants)

client = MongoClient(f"mongodb+srv://sc_delaEmi:u2JsEd0nzYssgaMd@cluster0.8qczawe.mongodb.net/test?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client['test']
res = db.restaurants
lay = db.spaces


@restaurants.route("/restaurants")
def restaurant_list():
    arr = list(res.find({}, {"_id":0, "location":1, "hours":1, "link":1, "description":1, "name":1}))
    return render_template("./locations.html", title="locations", arr=arr)

@restaurants.route("/filter_restaurants" , methods=['POST'])
def restaurant_filter():
    arr = list(res.find({ "category": request.form.get('filterRestaurants')}, {"_id":0, "location":1, "hours":1, "link":1, "description":1, "name":1}))
    return render_template("./locations.html", title="locations", arr=arr)

@restaurants.route("/restaurant_layout" , methods=['POST'])
def restaurant_layout():
    print(request.form.get('restaurantId'))
    print(request.form.get('seletedHour'))
    arr = list(lay.find({'restaurantName': request.form.get('restaurantId'), 'hour': request.form.get('seletedHour')}, {"_id":0, "restaurantName":1, "hour":1, "tab_id":1, "avalible":1}))
    resarr = list(res.find({ "name": request.form.get('restaurantId')}, {"_id":0, "location":1, "hours":1, "link":1, "description":1, "name":1}))
    link = resarr[0]["link"]
    location = resarr[0]["location"]
    return render_template("./resLay.html", title="Layout", arr=arr, link=link, location=location)



















#Form to fill out the restaurant layout
@restaurants.route("/fill_res")
def fill_res():
    restaurantName = {"Mexican Place", "Sunday Menudo", "Burger House", "Pizza place", "Comida china"}
    hour = {"12-1", "1-2", "2-3", "3-4", "4-5"}
    tab_id = {"1a", "1b","1c","1d","1e"}

    for i in restaurantName:
        for j in hour:
            for k in tab_id:
                db.spaces.insert_one({
        'restaurantName': i,
        'hour': j,
        'tab_id': k,
        'avalible': True
    })
    return "Database created"
