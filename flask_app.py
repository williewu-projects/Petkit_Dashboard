from flask import Flask, send_from_directory, render_template
import threading
import time
import schedule
import os
from graph_generator import generate_graph, generate_duration_histogram, generate_usage_bar_chart

app = Flask(__name__)


# Schedule graph to regenerate every 10 minutes
def run_scheduler():
    schedule.every(10).minutes.do(generate_graph)
    schedule.every(10).minutes.do(generate_duration_histogram)
    schedule.every(10).minutes.do(generate_usage_bar_chart)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/")
def index():   
    return render_template("index.html")

@app.route("/weight_chart")
def serve_weight_chart():
    generate_graph()
    return send_from_directory("static", "weight_chart.png")

@app.route("/duration_histogram")
def serve_duration_histogram():
    generate_duration_histogram()
    return send_from_directory("static", "toilet_duration_histogram.png")

@app.route("/usage_bar_chart")
def serve_usage_bar_chart():
    generate_usage_bar_chart()
    return send_from_directory("static", "toilet_usage_bar_chart.png")

if __name__ == "__main__":

    generate_graph()
    generate_duration_histogram()
    generate_usage_bar_chart()
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    app.run(host="0.0.0.0", port=5000)
