from flask import Flask
import requests
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route("/get_webpage")
def get_page():
    response = requests.get("https://www.quasicoherentlabs.com")
    return response.headers['Content-Encoding']

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
