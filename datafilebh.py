import json
import os
from flask import Flask, jsonify
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

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def find_all_resultdata():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM resultdata")
        rows = cur.fetchall()
        cur.close()
        datalist = {}

        for row in rows:
            date, number, can, gen, pet = row
            formatted_data = {
                "can": format(can, ".2f"),
                "gen": format(gen, ".2f"),
                "pet": format(pet, ".2f")
            }

            if date not in datalist:
                datalist[date] = {}
            datalist[date][number] = formatted_data

        return datalist



#resultdata에 있는 데이터를 전부 json파일에 저장하여 세이브, 파일이없으면 새로 생성
def get_data_and_save():
    with app.app_context():
        data = find_all_resultdata()

        # Convert the list to JSON with proper indentation (4 spaces)
        data_json = json.dumps(data, default=custom_encoder, indent=4)

        # Specify the path to save the JSON file (replace 'path/to/save' with your desired path)
        save_path = 'C:\DataFile\data.json'

        try:
            # Check if the file exists and is non-empty
            if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                with open(save_path, 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                existing_data = {}
        except FileNotFoundError:
            existing_data = {}

        # Merge existing data with new data
        existing_data.update(data)

        # Save the merged data to the JSON file with proper indentation
        with open(save_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    return jsonify({"message": "Data saved as data.json in the specific path."})

