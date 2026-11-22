"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import csv
import io

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
db = client.brevets

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.route("/test_db")
def test_db():
    client.admin.command("ping")
    return "MongoDB connection works!"


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.

    Expects the control distance, brevet distance, start date,
    and start time as URL-encoded arguments.

    """
    
    app.logger.debug("Got a JSON request")

    km = request.args.get('km', type=float)

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    brevet_dist = request.args.get('brevet_dist_km', type=int)
    date = request.args.get('begin_date')
    time = request.args.get('begin_time')

    start_time = date + "T" + time

    open_time = acp_times.open_time(km, brevet_dist, start_time)
    close_time = acp_times.close_time(km, brevet_dist, start_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

def make_csv(controls, fields): 
    #Helper function for CSV conversion
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)

    writer.writeheader()
    writer.writerows(controls)

    return flask.Response(output.getvalue(), mimetype="text/csv")

def get_times(field):
    top = request.args.get("top", type=int)

    controls = db.controls.find({}, {
        "_id": 0,
        field: 1
    }).sort(field, 1)

    if top is not None and top > 0:
        controls = controls.limit(top)

    return list(controls)

@app.route("/listAll")
@app.route("/listAll/json")
def list_all():
    controls = list(db.controls.find({}, {
        "_id": 0,
        "open": 1,
        "close": 1
    }))

    return flask.jsonify(controls)

@app.route("/listOpenOnly")
@app.route("/listOpenOnly/json")
def list_open_only():
    controls = get_times("open")
    return flask.jsonify(controls)




@app.route("/listCloseOnly")
@app.route("/listCloseOnly/json")
def list_close_only():
    controls = get_times("close")
    return flask.jsonify(controls)


@app.route("/listAll/csv")
def list_all_csv():
    controls = list(db.controls.find({}, {
        "_id": 0,
        "open": 1,
        "close": 1
    }))

    return make_csv(controls, ["open", "close"])


@app.route("/listOpenOnly/csv")
def list_open_only_csv():
    controls = get_times("open")
    return make_csv(controls, ["open"])


@app.route("/listCloseOnly/csv")
def list_close_only_csv():
    controls = get_times("close")
    return make_csv(controls, ["close"])

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

@app.route("/_submit", methods=["POST"])
def submit_controls():
    data = request.get_json()
    controls = data.get("controls", []) if isinstance(data, dict) else []

    if not controls:
        return flask.jsonify(error="No controls to save"), 400

    db.controls.insert_many(controls)

    return flask.jsonify(message="Controls saved")

@app.route("/display")
def display_controls():
    controls = list(db.controls.find())
    return flask.render_template("display.html", controls=controls)

@app.route("/_clear", methods=["POST"])
def clear_controls():
    db.controls.delete_many({})
    return flask.jsonify(message="Saved controls cleared")

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
