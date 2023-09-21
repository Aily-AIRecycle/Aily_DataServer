from sched import scheduler
import time
from flask import Response, jsonify, request, Flask

from data import send_all_kgdata,find_all_cfp,KgData,CFP
from avgdata import send_all_data,Avgg2
from datafilebh import get_data_and_save
from trashdatasave import reciverdata
from fulllate import fulllate_calculate


app = Flask(__name__)

@app.route('/')
def hello_pybo():
    return 'Flask'

@app.route('/data/cfp', methods=['GET'])
def send_carbon():
    cfp_data = find_all_cfp()
    return cfp_data

@app.route('/data/kgd', methods=['GET'])
def send_kg():
    kg_data = send_all_kgdata()
    return kg_data

@app.route('/data/pd', methods=['GET'])
def send_avg():
    # return send_all_data()
    avg_data = send_all_data()
    return jsonify(avg_data)



@app.route('/fulllate', methods=['POST']) #post echo api
def post_get_fulllate():
    # global 이백
    이백 = jsonify(fulllate_calculate(request.get_json()))
    return 이백

# @app.route('/saturation', methods=['POST']) #post echo api
# def saturation():
#     global 이백
#     resultsaturation = 이백
#     return resultsaturation


#######################################################test단
#쓰레기 강제저장 ( test )
@app.route('/data/test3', methods=['GET'])
def sendd():
    return Avgg2()

@app.route('/data/test2', methods=['GET'])
def senddd():
    kg_data = KgData()
    return kg_data

@app.route('/data/test1', methods=['GET'])
def sendddd():
    # return send_all_data()
    return CFP()

#########################################################3

@app.route('/data/savedatafile', methods=['GET'])
def senddd2d():
    # return send_all_data()
    return get_data_and_save()


@app.route('/data/test4', methods=['POST'])
def sendd2d2d():
    received_data = request.get_json()
    print(received_data)



if __name__ == '__main__':
    app.run(debug=False,host="127.0.0.1",port=5000)
    