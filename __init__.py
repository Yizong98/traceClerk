from flask import Flask, request, make_response
from clerk.util import write_json, check_exist, get_latest, validate_date, get_date_from_request, update_date_request
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import os
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    db_file_name = os.path.join(app.instance_path, 'historical_date.json')
    CORS(app, supports_credentials=True)
    print(db_file_name)

    @app.route('/get_latest_update')
    def get_latest_update():
        return get_latest(db_file_name)

    @app.route('/write_date', methods=['GET'])
    def write_date():
        error, date_val = get_date_from_request(request)
        if error:
            return make_response({"message": "no date inside the key!"}, 400)
        error, date_val = validate_date(date_val)
        if error:
            return make_response({"message": "date format is incorrect, must be mm/dd/yy"}, 400)
        if check_exist(date_val, db_file_name):
            return make_response({"message": "already updated!"})
        else:
            write_json(date_val, db_file_name)
            return make_response({"message": "successfully updated!"})

    @app.route('/fill_missing_data')
    def fill_missing_data():
        date_format = '%-m/%-d/%y'
        days_in_a_week = 7
        pst_dt_object = datetime.now(tz=timezone('US/Pacific'))
        message_result = {}
        for i in range(days_in_a_week):
            current_date_to_update = (
                pst_dt_object - timedelta(days=i)).strftime(date_format)
            message_result[current_date_to_update] = update_date_request(
                current_date_to_update)
        return make_response(message_result)

    return app
