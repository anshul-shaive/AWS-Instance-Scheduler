import json
import boto3
import ast
import datetime
import requests


def lambda_handler(event, context):
    # Added it here for reference, it is used only in lambda.
    request_data = event.get("data", '')
    if request_data:
        start = request_data['start']
        stop = request_data['stop']
        delete = request_data['delete']
        region = request_data['region']
        # instances = ast.literal_eval(request_data['instances'])
        instances = [request_data['instances']]
        schedule = request_data['schedule']

        ec2 = boto3.client('ec2', region_name=region)
        dynamodb = boto3.resource('dynamodb', region_name=region)
        ins_tab = dynamodb.Table('InstanceSchedule')

        if schedule:
            ec2.create_tags(Resources=instances, Tags=[{'Key': 'scheduled', 'Value': 'True'}])

            try:
                response = ins_tab.put_item(
                    Item={
                        'InstanceID': instances[0],
                        'Schedule': {
                            'Start': schedule['start'],
                            'Stop': schedule['stop'],
                        }
                    })
                return {'msg': response}
            except Exception as e:
                return {'msg': 'fail', 'err': str(e)}

        if stop:
            ec2.stop_instances(InstanceIds=instances)
            print('stoping instances: ' + str(instances))

        if start:
            ec2.start_instances(InstanceIds=instances)
            print('starting instances: ' + str(instances))

        if delete:
            ec2.delete_tags(Resources=instances, Tags=[{'Key': 'scheduled'}])

        return {
            'statusCode': 200,
            'body': json.dumps({'msg': 'Instance Scheduler Lambda', 'vars': [start, stop, delete, str(instances)]})
        }

    else:
        # This part will run every 10 mins when EventBridge triggers it to check which instances needs to start or stop.
        region_name = 'us-east-2'
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        ins_tab = dynamodb.Table('InstanceSchedule')
        resp = ins_tab.scan()
        scheduled_instances = resp.get('Items')
        for ins in scheduled_instances:
            Start = "False"
            Stop = "False"

            for day in list(ins['Schedule'].get("Start", [])):
                if int(day) - datetime.datetime.today().weekday() == 0:
                    Start = "True"
            for day in list(ins['Schedule'].get("Stop", [])):
                if int(day) - datetime.datetime.today().weekday() == 0:
                    Stop = "True"

            lambda_json = {"data": {"start": Start,
                                    "stop": Stop,
                                    "delete": "False",
                                    "instances": ins.get('InstanceID'),
                                    "region": region_name,
                                    "schedule": {}
                                    }}
            resp = requests.post(url='https://nzp4rwufki.execute-api.us-east-2.amazonaws.com/default/instanceScheduler',
                                 json=lambda_json)
        return {'msg': resp.text}
