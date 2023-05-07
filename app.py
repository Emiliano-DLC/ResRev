from flask import Flask, jsonify, render_template, request, redirect, Blueprint
from flask_cors import CORS

#blueprints
from restaurants import restaurants
from reservation import reservation

app = Flask(__name__)
app.register_blueprint(restaurants)
app.register_blueprint(reservation)

CORS(app)

@app.route("/")
def home():
    return render_template("./home.html")

