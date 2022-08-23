from main import *

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    data = findValue()
    return {"date": data[0],
            "daily": data[1],
            "avg": data[5],
            "remain": data[2],
            "max": data[3],
            "min": data[4]}

@app.route("/daily")
def daily():
    data = findValue()
    return {"daily": data[1]}

@app.route("/average")
def avg():
    data = findValue()
    return {"avg": data[5]}

@app.route("/remain")
def remain():
    data = findValue()
    return {"remain": data[2]}

@app.route("/max")
def maxs():
    data = findValue()
    return {"max": data[3]}
    # {"max":"\u0e04\u0e48\u0e32\u0e40\u0e14\u0e34\u0e19\u0e17\u0e32\u0e07"}

@app.route("/min")
def mins():
    data = findValue()
    return {"min": data[4]}

# flask --app genAPI run