from flask import jsonify
from flask import request
import requests
from flask import Blueprint
import boto3
import os

delete_api = Blueprint('delete_api', __name__)


@delete_api.route('/delete_schedule', methods=['POST', 'GET'])
def delete_schedule():
    if request.method == 'POST':
        json_data = request.get_json()
        instances = json_data['InstanceID']
        region_name = 'us-east-2'

        access_id = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        client = boto3.resource('dynamodb', aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key,
                                region_name='us-east-2')
        ins_tab = client.Table('InstanceSchedule')

        lambda_json = {"data": {"start": "False",
                                "stop": "False",
                                "delete": "True",
                                "instances": instances,
                                "region": region_name,
                                "schedule": {}
                                }}

        try:
            response = ins_tab.delete_item(
                Key={
                    'InstanceID': instances
                }
            )

            # invoking lambda function with delete=True will delete the tag from instance
            resp = requests.post(url='https://nzp4rwufki.execute-api.us-east-2.amazonaws.com/default/instanceScheduler',
                                 json=lambda_json)

            return jsonify({'msg': [response.text, resp.text]})
        except Exception as e:
            return jsonify({'msg': 'fail', 'err': str(e)})
    else:
        return jsonify({'msg': 'Send a post request with JSON data in body containing instance id to be deleted'})
