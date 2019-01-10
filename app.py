try:
    from flask import Flask, send_file
    from flask.globals import request
    import subprocess
    import json
    from flask.json import jsonify
    from pymongo import MongoClient
    from datetime import datetime
    from flask_cors import CORS
except Exception:
    print("Please verify if you have installed all the necessary Python modules: flask, subprocess, json, pymongo, datetime")
    input()
    exit()

app = Flask(__name__)
CORS(app)
@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route('/ipsender', methods=['POST'])
def send_ip():
    status = ''
    ultpval = ''
    dltpval = ''
    serverIPval = ''
    serverPORTval = ''
    try:
        serverIPval = request.json['serverIP']
        serverPORTval = request.json['serverPORT']
        iperf_output = subprocess.check_output(["iperf3","-c",serverIPval.strip(),"-p",serverPORTval.strip(),"-J"],stderr=subprocess.STDOUT,universal_newlines=True,shell=True)
        ultpval = str(json.loads(iperf_output)['end']['sum_sent']['bits_per_second'])
        dltpval = str(json.loads(iperf_output)['end']['sum_received']['bits_per_second'])
        status = 'Connected to Server!'
    except subprocess.CalledProcessError:
        status = 'Check connection to server!'
    except KeyError:
        status = 'Check server credentials!'
    timestampval = str(datetime.now())
    try:
        client = MongoClient('localhost:27017')
        db = client.iperfdata
        db.iperf.insert_one(
                                {
                                 "server_ip":serverIPval,
                                 "server_port":serverPORTval,
                                 "timestamp":timestampval,
                                 "throughput_ul":ultpval,
                                 "throughput_dl":dltpval 
                                 }
                            )
    except Exception:
        status = 'Value not entered into database. Check database connection!'
    return jsonify({'ulspeed':ultpval,'dlspeed':dltpval,'status':status})




@app.route('/historygetter', methods=['GET'])
def get_history():
    historylist = []
    state = ''
    try:
        client = MongoClient('localhost:27017')
        db = client.iperfdata
        records_all = db.iperf.find({}, {'_id': False})
        for rec in records_all:
            historylist.append(rec)
        state = 'Connected to Database!'
    except Exception:
        state = 'Values not retrieved from database. Check database connection!'
    return jsonify({'historylist':historylist,'state':state})

if __name__ == "__main__":
    app.run(host='127.0.0.1')