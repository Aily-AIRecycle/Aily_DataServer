from sched import scheduler
import time
from flask import Response, jsonify, request, Flask

from data import send_all_kgdata,CFP
from avgdata import send_all_data


app = Flask(__name__)

@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'

@app.route('/data/cfp', methods=['GET'])
def send2():
    return CFP()

@app.route('/data/kgd', methods=['GET'])
def send():
    kg_data = send_all_kgdata()
    return kg_data

@app.route('/data/pd', methods=['GET'])
def test():
    # return send_all_data()
    avg_data = send_all_data()
    return jsonify(avg_data)


if __name__ == '__main__':
    app.run(debug=False,host="127.0.0.1",port=5000)
    