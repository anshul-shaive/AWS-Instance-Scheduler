from flask import jsonify
from flask import request
from flask import Blueprint
import boto3
import os

read_all_api = Blueprint('read_all_api', __name__)


@read_all_api.route('/read_all_schedule', methods=['POST', 'GET'])
def read_all_schedule():
    if request.method == 'GET':
        region_name = 'us-east-2'

        access_id = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        client = boto3.resource('dynamodb', aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key,
                                region_name=region_name)
        ins_tab = client.Table('InstanceSchedule')

        try:
            resp = ins_tab.scan()
            scheduled_instances = resp.get('Items')

            return jsonify({'msg': resp, 'items': scheduled_instances})
        except Exception as e:
            return jsonify({'msg': 'fail', 'err': str(e)})
    else:
        return jsonify({'msg': 'Send a get request to read all schedules'})
