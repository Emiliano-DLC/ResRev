from flask import Flask, render_template, redirect, Blueprint, url_for, request
from pymongo import MongoClient, ReturnDocument
from flask_cors import CORS
import certifi
import random
import string

reservation = Blueprint('reservation', __name__)

CORS(reservation)

client = MongoClient(f"mongodb+srv://sc_delaEmi:u2JsEd0nzYssgaMd@cluster0.8qczawe.mongodb.net/test?retryWrites=true&w=majority",tlsCAFile=certifi.where()) 
db=client['test']
reservations=db.reservations

#Reference to the spaces collection in the database
#lay as of layout
lay = db.spaces


#Redirect to the specific restaurant in html
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
    #Generates random key
    letters=string.ascii_lowercase
    result=''.join(random.choice(letters) for i in range(5))
    print(result)
    #---------------------------------

    arr = list(lay.find({'restaurantName': request.form.get('restaurantName'), 'hour': request.form.get('seletedHour'),"tab_id": request.form.get('tabId')}, {"_id":0, "restaurantName":1, "hour":1, "tab_id":1, "avalible":1}))
    print(arr[0]["avalible"])
    if arr[0]["avalible"]:
        db.reservations.insert_one({
        'restaurantName': request.form.get('restaurantName'),
        'reservationName': request.form.get('nameInput'),
        'guests': request.form.get('inputGuess'),
        'times': request.form.get('seletedHour'),
        'adaneeded': request.form.get('ada'),
        'coments': request.form.get('comments'),
        'key': result,
        'tab_id':request.form.get('tabId')})
        

        lay.update_one(
            { 'tab_id':request.form.get('tabId'), 'restaurantName': request.form.get('restaurantName'), 'hour': request.form.get('seletedHour')},
            {"$set": { "avalible": False }}
        )

        return render_template("./confirmationPage.html", result=result)
    else:
        return "Invalid"
    
#---------------------------------------------------------------------


@reservation.route('/deleteReservation')
def deleteReservationForm():
   return render_template("./deleteReservation.html")

@reservation.route('/deleteReservationQuery', methods=['POST'])
def deleteReservation():
    name = request.form.get('userName')
    keyRes = request.form.get('keyRes')

    reservationList = list(reservations.find({"reservationName": name, "key": keyRes}, {"_id":0, "tab_id":1, "restaurantName":1, "times":1}))

    if len(reservationList) < 1:
        alertMsg = "Invalid reservation"
        return render_template("./deleteReservation.html", alertMsg=alertMsg)

    reservation = reservations.find_one({"reservationName": name, "key": keyRes})

    if reservation:
        reservations.delete_one({"reservationName": name, "key": keyRes})

        lay.update_one(
            { 'tab_id':reservationList[0]['tab_id'], 'restaurantName':reservationList[0]['restaurantName'], 'hour':reservationList[0]['times']},
            {"$set": { "avalible": True }}
        )
        return render_template("./conPage.html", output="Query has been deleted")
    else:
        alertMsg = "Reservation does not exist"
        return render_template("./deleteReservation.html", alertMsg=alertMsg)
#---------------------------------------------------------------------

@reservation.route('/editReservation')
def editReservationForm():
    return render_template("./editReservationQuery.html")

@reservation.route('/editReservationFinder', methods=['POST'])
def editReservationFinder():
    name=request.form.get('userName')
    keyRes=request.form.get('keyRes')

    reservation = reservations.find_one({"reservationName": name, "key": keyRes})
    if reservation:
        query = {
            "reservationName": reservation["reservationName"],
            "guests": reservation["guests"],
            "adaneeded": reservation["adaneeded"],
            "coments": reservation["coments"],
            "restaurantName": reservation["restaurantName"],
            "times": reservation["times"],
            "key": reservation["key"]
        }
        return render_template("./editReservation.html", query=query)
    else:
        alertMsg = "Reservation does not exist"
        return render_template("./editReservationQuery.html", alertMsg=alertMsg)
        

@reservation.route('/editReservationQuery', methods=['POST'])
def editReservationQuery():
    name=request.form.get('userName')
    guestNo=request.form.get('guests')
    keyRes=request.form.get('keyRes')
    comments=request.form.get('coments')
    print(name)

    print(reservations.update_one(
            { "reservationName":name, "key":keyRes},
            { "$set": { "guests": guestNo,
                       "coments": comments } }
        ))
    
    return render_template("./conPage.html", output="Query has been updated")
