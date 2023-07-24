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
fristtime = 1689778800
lasttime = 1689864600

def first_time_set():
    global fristtime
    fristtime = time.time()
    print("fristtime = %s",str(fristtime))
    
    
def last_time_set():
    lasttime = time.time()
    print("lasttime =",lasttime)
    return lasttime

real = True

app = Flask(__name__)

CORS(app)

mysql = MySQL(app)

app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")



#db에 데이터값 저장
def save_data(day,number,can,pet,gen):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pd (day,number,can,gen,pet) VALUE(%s,%s,%s,%s,%s)",(day,number,can,pet,gen))
        mysql.connection.commit() 
        cur.close()

#기계별로 캔,페트,일반 더한 값
def data_all_sum(datanumber):
    global fristtime
    global lasttime
    last_time_set()
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(resultdata.can),SUM(resultdata.pet), SUM(resultdata.gen) FROM resultdata WHERE number = %s AND resultdata.localdate BETWEEN %s AND %s",(datanumber,fristtime,lasttime))
        results = cur.fetchall() 
        cur.close()
        data = [int(item) if item is not None else 0 for item in results[0]]
        return data

#기계별로 캔,페트,일반 다 더한 값
def all_sum(datanumber):
    global fristtime
    global lasttime
    last_time_set()
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT SUM(resultdata.can) + SUM(resultdata.pet) + SUM(resultdata.gen) FROM resultdata WHERE number = %s AND resultdata.localdate BETWEEN %s AND %s",(datanumber,fristtime,lasttime))
        results = cur.fetchall() 
        cur.close()
        data = [int(item) if item is not None else 0 for item in results[0]]
        return data

#설치된 기계의 넘버링
def data_all_number():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT resultdata.number FROM resultdata WHERE number")
        pp = cur.fetchall()
        cur.close()
        data = [item[0] for item in pp]
        return data

#각 캔,페트,일반의 비율의 데이터를 검색
def find_all_pddata():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT * FROM pd")
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

#기계별로 일반,페트,캔의 총 버려진 갯수 퍼센트구해서 db에 저장
def Avgg2():
    date_strin = datetime.datetime.now()
    now = date_strin.strftime("%Y-%m-%d")
    #정해진 시각에 작동하도록 하는 수식어
    start_time = datetime.time(00, 30, 0)  # 시 분 초
    end_time = datetime.time(23, 59, 10)  # 시 분 초
    numberset = data_all_number()
    numberset.sort()
    if start_time <= date_strin.time() <= end_time:
        
        for i in numberset:
            lsatresult = []
            all = all_sum(i)
            for z in range(0,3):
                for data in data_all_sum(i):
                    lsatresult.append(data/all[0]*100)

            save_data(now,i,format(lsatresult[0],".2f"),format(lsatresult[2],".2f"),format(lsatresult[1],".2f"))                     
    
    return "savedataok!"
    

#db에서 검색한 정보를 프론트로 전송
def send_all_data():
    date_string = datetime.datetime.now()
    # Modifier to operate at a fixed time
    start_time = datetime.time(00, 30, 0) # hours minutes seconds
    end_time = datetime.time(23, 59, 10) # hours minutes seconds
    dd = find_all_pddata()
    return dd
    





    
##정해진 시간에 열리는 수식어와 아래의 스케쥴 함수를 이용하면 정확히 정해진 시각에 1번만 작동
schedule = BackgroundScheduler(timezone='Asia/Seoul') 
# schedule.add_job(AvgData, 'cron', hour='23', minute='59', second='03')
#-------00시 자정 시간 체크
schedule.add_job(first_time_set, 'cron', hour='00', minute='00', second='00')





schedule.start()



