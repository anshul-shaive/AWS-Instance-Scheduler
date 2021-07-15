from flask import jsonify
from flask import request
from flask import Blueprint
import boto3
import os

read_api = Blueprint('read_api', __name__)


@read_api.route('/read_schedule', methods=['POST', 'GET'])
def read_schedule():
    if request.method == 'POST':
        json_data = request.get_json()
        instances = json_data['InstanceID']
        region_name = 'us-east-2'

        access_id = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        client = boto3.resource('dynamodb', aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key,
                                region_name=region_name)
        ins_tab = client.Table('InstanceSchedule')

        try:
            response = ins_tab.get_item(Key={'InstanceID': instances})

            return jsonify({'msg': response.text, 'item': response['Item']})
        except Exception as e:
            return jsonify({'msg': 'fail', 'err': str(e)})
    else:
        return jsonify({'msg': 'Send a post request with JSON data in body containing instance id to be read'})
