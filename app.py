from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define a counter metric
REQUEST_COUNT = Counter("my_app_requests_total", "Total requests to my app")

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello, World!"

@app.route("/metrics1")
def metrics1():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/metrics2")
def metrics2():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Run on 0.0.0.0 so it’s reachable in Kubernetes
    app.run(host="0.0.0.0", port=8080)