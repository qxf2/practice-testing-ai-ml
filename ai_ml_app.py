"""
A Flask application that wraps around AI/ML models.
Qxf2 wrote this to help testers practice testing AI/ML based applications.
To learn more, see the README.md of this application.
"""
from flask import Flask, jsonify, render_template, request
import is_pto.is_pto as pto_classifier
from flask import Flask, Response
from prometheus_client import generate_latest
from prometheus_client import Gauge
import psutil

app = Flask(__name__)

cpu_usage = Gauge('cpu_usage', 'CPU usage percentage')
ram_usage = Gauge('ram_usage', 'Memory usage percentage')

@app.route("/")
def index():
    "Home page"
    return render_template("index.html")

@app.route("/about")
def about():
    "About page"
    return render_template("about.html")

@app.route("/is-pto", methods=['GET', 'POST'])
def is_pto():
    "Is the message a PTO?"
    response = render_template("is_pto.html")
    if request.method == 'POST':
        message = request.form.get('message')
        prediction_score = int(pto_classifier.is_this_a_pto(message))
        response = jsonify({"score" : prediction_score, "message" : message})
    return response

@app.route("/metrics")
def metrics():
    # update Prometheus gauges with CPU and RAM usage
    cpu_percent = psutil.cpu_percent()
    ram_info = psutil.virtual_memory()
    cpu_usage.set(cpu_percent)
    ram_usage.set(ram_info.percent)

    # generate Prometheus metrics in the appropriate format
    return Response(generate_latest(), mimetype="text/plain")

#---START OF SCRIPT
if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=6464)
