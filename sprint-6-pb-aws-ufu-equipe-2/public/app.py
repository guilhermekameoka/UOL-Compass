from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import urllib.request
import json

def apiPost(url, request):
    load_dotenv()

    url_address = os.getenv(url)
    request_body = request.get_json()

    headers = {'Content-Type': 'application/json'}
    req     = urllib.request.Request(url_address, data=json.dumps(request_body).encode('utf-8'), headers=headers)
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    return result

# Initializes our application
app = Flask(__name__, static_url_path='/static')

# Root
@app.route("/")
def index():
    return render_template("index.html")

# Route -> v1/tts
@app.route("/v1/tts", methods=["POST"])
def v1():
    return apiPost(url="route4_url", request=request)

# Route -> v2/tts
@app.route("/v2/tts", methods=["POST"])
def v2():
    return apiPost(url="route5_url", request=request)

# Route -> v3/tts
@app.route("/v3/tts", methods=["POST"])
def v3():
    return apiPost(url="route6_url", request=request)

# Runs application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)