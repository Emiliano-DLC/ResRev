from flask import Flask, render_template, redirect, Blueprint, url_for, request
from pymongo import MongoClient
from flask_cors import CORS
import certifi

reservation = Blueprint('reservation', __name__)

CORS(reservation)


db=client['test']
reservations=client['reservations']


#Redirect to the specific restaurant
@reservation.route('/respageBurritos', methods=['POST'])
def respageBurritos():
    return render_template("./reservation.html", restaurant="Burrito")

@reservation.route('/respageBurger', methods=['POST'])
def respageBurger():
    return render_template("./reservation.html", restaurant="Burger")

@reservation.route('/respageMenudo', methods=['POST'])
def respageMenudo():
    return render_template("./reservation.html", restaurant="Menudo")

@reservation.route('/respagePizza', methods=['POST'])
def respagePizza():
    return render_template("./reservation.html", restaurant="Pizza")

@reservation.route('/respageChinese', methods=['POST'])
def respageChinese():
    return render_template("./reservation.html", restaurant="Chinese")
#-------------------------------------------------------------------------

@reservation.route('/confirmationPage', methods=['POST'])
def confirmationPage():
    db.reservations.insert_one({
        'restaurantName': request.form.get('restaurantName'),
        'reservationName': request.form.get('nameInput'),
        'guests': request.form.get('inputGuess'),
        'times': request.form.get('seletedHour'),
        'adaneeded': request.form.get('ada'),
        'coments': request.form.get('comments')
    })

    return render_template("./confirmationPage.html")