import json
import datetime
import requests


def get_date_from_request(request):
    try:
        date_val = request.args['date']
        return False, date_val
    except KeyError:
        return True, None


def validate_date(date_val):
    try:
        trimmed_date_val = datetime.datetime.strptime(
            date_val, '%m/%d/%y').strftime('%-m/%-d/%y')
        return False, trimmed_date_val
    except ValueError:
        return True, None


def get_latest(filename):
    data = read_file(filename)
    return data[-1]


def write_json(date_val, filename):
    data = read_file(filename)
    data.append(date_val)
    data.sort(key=lambda x: datetime.datetime.strptime(x, '%m/%d/%y'))

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return


def check_exist(date_val, filename):
    data = read_file(filename)
    return date_val in data


def read_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


def update_date_request(date):
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{{"body":{{"date":"{date}","mode":"historical","password":"Open, sesame"}}}}'.format(
        date=date)

    response = requests.post(
        'http://new-trace-with-db.default.svc.cluster.local:8080/2015-03-31/functions/function/invocations', headers=headers, data=data)
    return response.text
