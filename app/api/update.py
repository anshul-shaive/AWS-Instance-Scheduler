from flask import jsonify
from flask import request
from flask import Blueprint
import boto3
import os

update_api = Blueprint('update_api', __name__)


@update_api.route('/update_schedule', methods=['POST', 'GET'])
def update_schedule():
    if request.method == 'POST':
        json_data = request.get_json()
        instances = json_data['InstanceID']
        start = json_data['Schedule']['Start']
        stop = json_data['Schedule']['Stop']

        access_id = os.environ.get('AWS_ACCESS_KEY_ID')
        secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        client = boto3.resource('dynamodb', aws_access_key_id=access_id,
                                aws_secret_access_key=secret_key,
                                region_name='us-east-2')
        ins_tab = client.Table('InstanceSchedule')

        try:
            response = ins_tab.update_item(
                Key={
                    'InstanceID': instances
                },
                UpdateExpression="set Schedule.Start=:st, Schedule.Stop=:sp",
                ExpressionAttributeValues={
                    ':st': start,
                    ':sp': stop
                },
                ReturnValues="UPDATED_NEW"
            )

            return jsonify({'msg': response.text})
        except Exception as e:
            return jsonify({'msg': 'fail', 'err': str(e)})
    else:
        return jsonify({'msg': 'Send a post request with JSON data in body containing instance id and updated schedule'})
