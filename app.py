''' Multiple Prometheus metrics endpoints without authentication '''

import threading
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, make_wsgi_app
from werkzeug.serving import make_server

app = Flask(__name__)

# Define a counter metric
REQUEST_COUNT = Counter("my_app_requests_total", "Total requests to my app")

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello, World!"

""" Utility to run a Flask app on its own port in a thread """

def run_app(flask_app, port):
    server = make_server("0.0.0.0", port, flask_app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    print(f"Started {flask_app.name} on port {port}")

if __name__ == "__main__":
        # Run two separate metrics servers
    metrics_app1 = Flask("metrics1")
    @metrics_app1.route("/metrics1")
    def metrics1():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
    run_app(metrics_app1, 8081)

    metrics_app2 = Flask("metrics2")
    @metrics_app2.route("/metrics2")
    def metrics2():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
    run_app(metrics_app2, 8082)

    # Start the main application
    # Run on 0.0.0.0 so it’s reachable in Kubernetes
    app.run(host="0.0.0.0", port=8080)