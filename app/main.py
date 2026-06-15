from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Flask running on Kubernetes !",
        "status": "healthy",
        "version": "1.0.0",
        "pod_name": os.getenv("POD_NAME", "unknown"),
        "node_name": os.getenv("NODE_NAME", "unknown")
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/metrics")
def metrics():
    return """
# HELP flask_requests_total Total requests
# TYPE flask_requests_total counter
flask_requests_total 1
""", 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)