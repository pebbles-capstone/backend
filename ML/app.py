from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route("/status")
def status():
    return "<p>Healthy</p>"


@app.route("/staticRec")
def staticRec():
    return "<p>Starting rec!</p>"


@app.route("/dynamicRec")
def dynamicRec():
    return "<p>Starting rec!</p>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000", debug=True)
