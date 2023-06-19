#!flask/bin/python
from flask import Flask
from flask import request
from classes.xgboost_predictor import XgboostPredictor

xgboost_model = XgboostPredictor()

app = Flask(__name__)

# index route
@app.route('/')
def index():
  return 'This is an python flask api created by group 3 for Compass UOL sprint 5 😀'

# predict route
@app.route('/api/v1/predict', methods=['POST'])
def post_prediction():
  class_predicted, error_message = xgboost_model.predict(args = request.get_json())
  if error_message != None:
    return f'Error: {error_message}', 403
  return { 'result': class_predicted }, 200

# Runs API
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)