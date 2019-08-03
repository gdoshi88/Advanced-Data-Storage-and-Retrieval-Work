import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, or_

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)


@app.route('/')
def Home():
    return(
        "CLIMATE APP<br />"
        "Available Routes:<br />"
        "/api/v1.0/precipitation<br />"
        "/api/v1.0/stations<br />"
        "/api/v1.0/tobs<br />"
        "ADD YOUR DESIRED DATE BELOW IN THIS FORMAT: YYYY-MM-DD. Prints minimum tobs, average tobs, max tobs in that order.<br />"
        "/api/v1.0/<date><br />"
        "ADD YOUR DESIRED START DATE AND END DATE BELOW IN THIS FORMAT: YYYY-MM-DD/YYYY-MM-DD. Prints minimum tobs, average tobs, max tobs in that order.<br />"
        "/api/v1.0/<startdate>/<enddate><br />"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    precipitation_results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= "2011-01-01", Measurement.date <= "2012-01-01")\
        .order_by(Measurement.date).all()
    all_prcp_results = []
    for prcp in precipitation_results:
        prcp_dictionary = {}
        prcp_dictionary["date"] = prcp.date
        prcp_dictionary["prcp"] = prcp.prcp
        all_prcp_results.append(prcp_dictionary)

    return jsonify(all_prcp_results)


@app.route('/api/v1.0/stations')
def stations():
    stations_results = session.query(Station.station, Station.name).all()
    all_stations = []
    for station in stations_results:
        stations_dictionary = {}
        stations_dictionary["station"] = station.station
        stations_dictionary["name"] = station.name
        all_stations.append(stations_dictionary)

    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date >= "2011-01-01", Measurement.date <= "2012-01-01").all()
    all_tobs = []
    for tob in tobs_results:
        tobs_dictionary = {}
        tobs_dictionary['date'] = tob.date
        tobs_dictionary['tobs'] = tob.tobs
        all_tobs.append(tobs_dictionary)

    return jsonify(all_tobs)


@app.route('/api/v1.0/<date>/')
def date_given(date):
    date_results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(
        Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == date).all()

    return jsonify(date_results)


# @app.route('/api/v1.0/<startdate>/<enddate>')
# def dateinput(startdate, enddate):
#     date_input_results = session.query(Measurement.date, Measurement.tobs).filter(
#         Measurement.date >= startdate, Measurement.date <= enddate).all()

#     start_end_date_input = []
#     for result in date_input_results:
#         input_dictionary = {}
#         input_dictionary['tobs'] = func.min(result.tobs)
#         input_dictionary['tobs'] = func.max(result.tobs)
#         input_dictionary['tobs'] = func.avg(result.tobs)
#         start_end_date_input.append(input_dictionary)

#     return jsonify(start_end_date_input)

@app.route('/api/v1.0/<startdate>/<enddate>')
def dateinput(startdate, enddate):
    temp_sel = [func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)]
    date_input_results = session.query(
        *temp_sel).filter(Measurement.date >= startdate, Measurement.date <= enddate).all()

    start_end_date_input = []
    for tmin, tavg, tmax in date_input_results:
        input_dictionary = {}
        input_dictionary['min'] = tmin
        input_dictionary['avg'] = tavg
        input_dictionary['max'] = tmax
        start_end_date_input.append(input_dictionary)

    return jsonify(start_end_date_input)


if __name__ == "__main__":
    app.run(debug=True)
