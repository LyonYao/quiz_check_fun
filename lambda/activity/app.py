import json
import os
from flask import Flask, jsonify, request
import pytz
from activity.activity import activity
from subject.subject import subject
from checker.checker import checker
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.default_timezone = pytz.timezone('Asia/Hong_Kong')

@app.before_request
def set_default_timezone():
    app.current_request_tz = app.default_timezone
app.register_blueprint(activity)
app.register_blueprint(subject)
app.register_blueprint(checker)
@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response
__ENDPOINT_PRE__ = '/api/activity/'
@app.route('%sgreet' % __ENDPOINT_PRE__, methods=['GET','POST'])
def greet():
    if request.method == 'GET':
        
        return jsonify(message="Greetings from Function activity" )
    elif request.method == 'POST':
        data = request.json
        return jsonify(message=f"Received POST request with data: {data}")

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))  # 添加日志输出

    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    headers = event.get('headers', {})
    body = event.get('body', None)
    query_params = event.get('queryStringParameters', {})

    with app.test_client() as client:
        response = client.open(
            path=path,
            method=http_method,
            headers=headers,
            data=body,
            query_string=query_params
        )

        return {
            'statusCode': response.status_code,
            'body': response.get_data(as_text=True),
            'headers': dict(response.headers)
        }

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    app.run(debug=True)