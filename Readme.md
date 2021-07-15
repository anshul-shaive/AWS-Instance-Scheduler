Instance Scheduler
------------------
### Running Instructions:

 - Run `pip install -r requirements.txt`
 - `set FLASK_APP = app`
 - Run `flask run` in cmd

### Working:

 - Send a post request to the route /create_schedule with JSON data in body
<br/>
   Example: <br/>
   `{
   "InstanceID": "i-0bfab3afe78f999d7",
    "Schedule": {
        "Start": "0123", 
        "Stop": "456"
    }
}`
   
 - Schedule can be the days which the instances needs to be active, inactive or both
 - In the above example, the instance specified by the instance id will remain active from monday to thursday and
   then inactive until the next monday.
   
 - Internally, this request is converted to a JSON object like: <br/>
`        {"data": {"start": "False",
                                "stop": "False",
                                "delete": "False",
                                "instances": instances,
                                "region": region_name,
                                "schedule": {"start": start,
                                             "stop": stop
                                             }
                                }}`
   
 - This JSON data is then passed to AWS Lambda which checks the condition 
if schedule is present or not. If the schedule is not empty it first adds the tag `scheduled = True` to the specified
   EC2 instace using boto3 and after that it creates an entry in
   a DynamoDB table whose primary key is instance id and it stores the schedule.
   
 - The different conditions then check if the start, stop or delete values passed is true and performs the appropriate operation

 - The lambda function is invoked every 10 mins using the EventBridge trigger and the main condition which determines if data is passed, meaning if it is called from the api endpoint becomes false and the other part is run. It loads all the items present in the 
   DynamoDB table and check the schedule of every instance then determines which instance needs to be stopped or started. 
   After that the lambda function invokes itself from the API gateway api and passes the data accordingly to start or shut down an instance.
   See the file lambda.py for more details.
   
 - The other routes for update, read and delete works directly with DynamoDB.
   
### Run in a docker container:

 - Create Dockerfile and docker-compose.yml files
 - Put the environment variables such as aws keys in a .env file
 - run `docker compose up`
 - open `http://localhost:8000/read_all_schedule` in a browser
