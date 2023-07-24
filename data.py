import os
import json
import random
import math
import smtplib
import sys
import time
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from apscheduler.schedulers.background import BackgroundScheduler 
import datetime
import random


load_dotenv()
global real
global fristtime
global lasttime
fristtime = 1689865200

app = Flask(__name__)

CORS(app)

mysql = MySQL(app)

app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

def first_time_set():
    global fristtime
    fristtime = time.time()
    print("fristtime = %s",str(fristtime))
    
    
def last_time_set():
    lasttime = time.time()
    print("lasttime =",lasttime)
    return lasttime
    

#kg데이터를 db에 저장
def save_kgdata(day,number,can,pet,gen):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO kgd (day,number,can,gen,pet) VALUE(%s,%s,%s,%s,%s)",(day,number,can,pet,gen))
        mysql.connection.commit() 
        cur.close()

#cfp데이터를 db에 저장
def save_CFPdata(day,number,can,pet):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO cfp (day,number,can,pet) VALUE(%s,%s,%s,%s)",(day,number,can,pet))
        mysql.connection.commit() 
        cur.close()

#kg의 데이터를 모두 조회
def find_all_kgdata():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM kgd")
        rows = cur.fetchall()
        cur.close()
        datalist = {}
        for row in rows:
            date, number, can, gen, pet = row
            if date not in datalist:
                datalist[date] = {}
            datalist[date][number] = {
                "can": format(can, ".2f"),
                "gen": format(gen, ".2f"),
                "pet": format(pet, ".2f")
            }
        return datalist

#cfp(절약되는 탄소의양)의 데이터를 모두 조회(gm 기준)
def find_all_cfp():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM cfp")
        rows = cur.fetchall()
        cur.close()
        datalist = {}
        for row in rows:
            date, number, can, pet = row
            if date not in datalist:
                datalist[date] = {}
            datalist[date][number] = {
                "can": format(can, ".2f"),
                "pet": format(pet, ".2f")
            }
        return datalist



#설치된 기계의 넘버링 모두 조회
def data_all_number():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT resultdata.number FROM resultdata WHERE number")
        pp = cur.fetchall()
        cur.close()
        data = [item[0] for item in pp]
        return data

#기계별로 캔,페트,일반 더한 값
def Bring_All_Data(number):
    global fristtime
    lasttime = last_time_set()
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT sum(can*16), sum(gen*15), sum(pet*16) FROM resultdata where number= %s AND resultdata.localdate BETWEEN %s AND %s",(number,fristtime,lasttime))
        results = cur.fetchall() 
        cur.close()
        data = [int(item) if item is not None else 0 for item in results[0]]
        return data

#기계별로 kg을 구해서 백엔드로 정보를 db에 저장 (현재까지 버려진 kg or 달 별로 계산 가능)
def KgData():
    date_strin = datetime.datetime.now()
    now = date_strin.strftime("%Y-%m-%d")
    
    machinenumber = data_all_number()
    machinenumber.sort()

    for number in machinenumber:
        numberdata = Bring_All_Data(str(number))
        print(numberdata)
        can = numberdata[0]/100
        gen = numberdata[1]/100
        pet = numberdata[2]/100
        save_kgdata(now,number,can,gen,pet)
    
    return "savedataok!"
    
#kg 데이터셋을 프론트로 전송
def send_all_kgdata():
    date_string = datetime.datetime.now()
    # Modifier to operate at a fixed time
    start_time = datetime.time(00, 30, 0) # hours minutes seconds
    end_time = datetime.time(23, 59, 10) # hours minutes seconds
    dd = find_all_kgdata()
    return dd


#각 기계별 페트,캔의 탄소 저감량 캔 절감되는 에너지양 (95%기준, 페트 70% 기준)을 계산하여 db에 저장
def CFP():
    date_strin = datetime.datetime.now()
    now = date_strin.strftime("%Y-%m-%d")
    machinenumber = data_all_number()
    machinenumber.sort()
    for number in machinenumber:
        numberdata = Bring_All_Data(str(number))
        print(numberdata)
        can = numberdata[0]*10*0.95
        pet = numberdata[2]*3.8*0.7
        save_CFPdata(now,number,can,pet)
        
    return "savedataok!"
    
    
#kg 데이터셋을 프론트로 전송
def send_all_cfp():
    date_string = datetime.datetime.now()
    # Modifier to operate at a fixed time
    start_time = datetime.time(00, 30, 0) # hours minutes seconds
    end_time = datetime.time(23, 59, 10) # hours minutes seconds
    dd = find_all_cfp()
    return dd

#더미값 생성 함수
# Function to generate a random number between 1 and 4 for 'number'
def generate_random_number():
    return random.randint(1, 4)

# Function to generate random values between 0 and 100 for 'can', 'gen', and 'pet'
def generate_random_value():
    return random.randint(0, 10)

# Function to get the current time as 'localdate'
def get_current_time():
    return time.time()

# Flask route to insert data into the MySQL table
def insert_data():
    with app.app_context():
        cur = mysql.connection.cursor()
        print(time.time())
        # Generate random values for 'can', 'gen', and 'pet'
        can_value = generate_random_value()
        gen_value = generate_random_value()
        pet_value = generate_random_value()

        # Generate a random number for 'number'
        number_value = generate_random_number()

        # Get the current time as 'localdate'
        localdate_value = get_current_time()

        cur.execute("INSERT INTO resultdata (localdate, number, can, gen, pet) VALUES (%s, %s, %s, %s, %s)", (localdate_value, number_value, can_value, gen_value, pet_value))
        mysql.connection.commit()    
        cur.close()

        return "Data inserted successfully!"

    
##정해진 시간에 열리는 수식어와 아래의 스케쥴 함수를 이용하면 정확히 정해진 시각에 1번만 작동
schedule = BackgroundScheduler(timezone='Asia/Seoul') 
# schedule.add_job(now_time, 'cron', hour='00', minute='00', second='00')
# schedule.add_job(AvgData, 'cron', hour='23', minute='59', second='03')

#-------00시 자정 시간 체크
schedule.add_job(first_time_set, 'cron', hour='00', minute='00', second='00')


schedule.add_job(insert_data, 'cron', second='10')

schedule.start()



