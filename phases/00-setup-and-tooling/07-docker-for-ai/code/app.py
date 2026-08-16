from flask import Flask, request, jsonify

app = Flask(__name__)

def predict(x):
    return {"input": x, "prediction": 2 * x}

@app.route("/predict", methods=["POST"])
def handle():
    x = request.get_json()["x"]
    return jsonify(predict(x))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
