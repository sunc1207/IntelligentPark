from flask import Flask
import csv
import json

app = Flask(__name__)


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


def get_json():
    csv_file = open("/home/inesa/IntelligentPark/test1.csv", encoding='utf-8')
    reader = csv.DictReader(csv_file)
    dict1 = {}
    value = []
    time = []
    for row in reader:
        value.append(row['value'])
        time.append(row['time'])
    dict1['time'] = time
    dict1['value'] = value
    j = json.dumps(dict1)
    return j


@app.route('/')
def hello_world():
    result = get_json()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5102)
