from flask import jsonify
from flask import request
import requests
from flask import Blueprint

create_api = Blueprint('create_api', __name__)


@create_api.route('/create_schedule', methods=['POST', 'GET'])
def create_schedule():
    if request.method == 'POST':
        json_data = request.get_json()
        instances = json_data['InstanceID']
        start = json_data['Schedule']['Start']
        stop = json_data['Schedule']['Stop']
        region_name = 'us-east-2'

        lambda_json = {"data": {"start": "False",
                                "stop": "False",
                                "delete": "False",
                                "instances": instances,
                                "region": region_name,
                                "schedule": {"start": start,
                                             "stop": stop
                                             }
                                }}

        try:
            resp = requests.post(url='https://nzp4rwufki.execute-api.us-east-2.amazonaws.com/default/instanceScheduler',
                                 json=lambda_json)

            return jsonify({'msg': resp.text})
        except Exception as e:
            return jsonify({'msg': 'fail', 'err': str(e)})
    else:
        return jsonify({'msg': 'Send a post request with JSON data in body containing instance id and schedule '})
