from sched import scheduler
import time
from flask import Response, jsonify, request, Flask

from data import send_all_kgdata,find_all_cfp,KgData,CFP
from avgdata import send_all_data,Avgg2
from datafilebh import get_data_and_save



app = Flask(__name__)

@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'

@app.route('/data/cfp', methods=['GET'])
def send2():
    cfp_data = find_all_cfp()
    return cfp_data

@app.route('/data/kgd', methods=['GET'])
def send():
    kg_data = send_all_kgdata()
    return kg_data

@app.route('/data/pd', methods=['GET'])
def test():
    # return send_all_data()
    avg_data = send_all_data()
    return jsonify(avg_data)


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


@app.route('/data/savedatafile', methods=['GET'])
def senddd2d():
    # return send_all_data()
    return get_data_and_save()

if __name__ == '__main__':
    app.run(debug=False,host="127.0.0.1",port=5000)
    