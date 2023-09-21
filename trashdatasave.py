import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

CORS(app)

mysql = MySQL(app)

app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")


def reciverdata():
    data = request.json
    print("Received data:", data)
    return jsonify({"message": "Data received successfully"}), 200
