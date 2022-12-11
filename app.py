from flask import Flask, render_template, request, jsonify
from chat import get_response

app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    action_and_data = get_response(text)
    message = {"answer": action_and_data}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)