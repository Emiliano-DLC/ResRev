from flask import Flask, render_template, redirect, Blueprint, url_for, request
from pymongo import MongoClient
from flask_cors import CORS
import certifi

reservation = Blueprint('reservation', __name__)

CORS(reservation)

client = MongoClient(f"mongodb+srv://sc_delaEmi:u2JsEd0nzYssgaMd@cluster0.8qczawe.mongodb.net/test?retryWrites=true&w=majority",tlsCAFile=certifi.where()) 
db=client['test']
reservations=db.reservations
lay = db.spaces


#Redirect to the specific restaurant
@reservation.route('/respageBurritos', methods=['POST'])
def respageBurritos():
    hour = request.form.get('restaurantHour')
    location = request.form.get('restaurantType')
    name = request.form.get('restaurantId')
    tab = request.form.get('tabId')
    print(name)
    return render_template("./reservation.html", restaurant="Burrito", hour=hour, location=location, name=name, tab=tab)

@reservation.route('/respageBurger', methods=['POST'])
def respageBurger():
    hour = request.form.get('restaurantHour')
    location = request.form.get('restaurantType')
    name = request.form.get('restaurantId')
    tab = request.form.get('tabId')
    return render_template("./reservation.html", restaurant="Burger", hour=hour, location=location, name=name, tab=tab)

@reservation.route('/respageMenudo', methods=['POST'])
def respageMenudo():
    hour = request.form.get('restaurantHour')
    location = request.form.get('restaurantType')
    name = request.form.get('restaurantId')
    tab = request.form.get('tabId')
    return render_template("./reservation.html", restaurant="Menudo", hour=hour, location=location, name=name, tab=tab)

@reservation.route('/respagePizza', methods=['POST'])
def respagePizza():
    hour = request.form.get('restaurantHour')
    location = request.form.get('restaurantType')
    name = request.form.get('restaurantId')
    tab = request.form.get('tabId')
    print(name)
    return render_template("./reservation.html", restaurant="Pizza", hour=hour, location=location, name=name, tab=tab)

@reservation.route('/respageChinese', methods=['POST'])
def respageChinese():
    hour = request.form.get('restaurantHour')
    location = request.form.get('restaurantType')
    name = request.form.get('restaurantId')
    tab = request.form.get('tabId')
    return render_template("./reservation.html", restaurant="Chinese", hour=hour, location=location, name=name, tab=tab)
#-------------------------------------------------------------------------

@reservation.route('/confirmationPage', methods=['POST'])
def confirmationPage():
    print(request.form.get('restaurantName'))
    print(request.form.get('tabId'))
    print(request.form.get('seletedHour'))

    arr = list(lay.find({'restaurantName': request.form.get('restaurantName'), 'hour': request.form.get('seletedHour'),"tab_id": request.form.get('tabId')}, {"_id":0, "restaurantName":1, "hour":1, "tab_id":1, "avalible":1}))
    print(arr[0]["avalible"])
    if arr[0]["avalible"]:
        db.reservations.insert_one({
        'restaurantName': request.form.get('restaurantName'),
        'reservationName': request.form.get('nameInput'),
        'guests': request.form.get('inputGuess'),
        'times': request.form.get('seletedHour'),
        'adaneeded': request.form.get('ada'),
        'coments': request.form.get('comments')})

        lay.update_one(
            { 'tab_id':request.form.get('tabId'), 'restaurantName': request.form.get('restaurantName'), 'hour': request.form.get('seletedHour')},
            {"$set": { "avalible": False }}
        )

        return render_template("./confirmationPage.html")
    else:
        return "Invalid"

