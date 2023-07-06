from flask import Flask, jsonify
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def make_external_request():
    response = requests.get("https://www.bbc.co.uk/")
    response.raise_for_status()
    return response.text
    
@app.route('/health')
def health():
    return "OK"
    
@app.route('/')
def hello():
    try:
        external_response = make_external_request()
        return f"Hello, World! External response: {external_response}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    metrics.track_flask_app(app)
    app.run(host='0.0.0.0', port=5000)