from sched import scheduler
import time
from flask import Response, jsonify, request, Flask

from data import send_all_kgdata,find_all_cfp,KgData,CFP,trash_insert_database
from avgdata import send_all_data,Avgg2
from datafilebh import get_data_and_save
from trashdatasave import reciverdata
from fulllate import fulllate_calculate


app = Flask(__name__)

@app.route('/')
def hello_pybo():
    return 'Flask'

@app.route('/data/trashtype', methods=['POST'])
def get_trash():
    # Check if the incoming request contains JSON data
    if request.is_json:
        try:
            trash_data = request.get_json()
            trash_insert_database(trash_data['devicenumber'],trash_data['can'],trash_data['pet'],trash_data['gen'])
            return "성공적으로 데이터를 받았습니다."
        except Exception as e:
            return f"파일 받기에 실패했습니다.: {str(e)}", 400
    else:
        return "요청이 못되었습니다.", 400
    
    
#각 기계별 날짜별 쓰레기,페트 탄소저람걍
@app.route('/data/cfp', methods=['GET'])
def send_carbon():
    cfp_data = find_all_cfp()
    return jsonify(cfp_data)

#각 기계별 날짜별 캔,페트,일반 버려진 총 중량
@app.route('/data/kgd', methods=['GET'])
def send_kg():
    kg_data = send_all_kgdata()
    return jsonify(kg_data)

#각 기계별 캔,페트,일반 비율 %
@app.route('/data/pd', methods=['GET'])
def send_avg():
    # return send_all_data()
    avg_data = send_all_data()
    return jsonify(avg_data)

#각 기계별 일반,페트,캔 차있는 비율 ( 0~100% )
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
    