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
        "/api/v1.0/<start><br />"
        "/api/v1.0/<start>/<end><br />"
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


@app.route('<start>')
@app.route('<start>/<end>')
def dateinput(start, end=None):
    if end == None:
        end = session.query(Measurement.date).order_by(
            Measurement.date.describe()).first()[0]
        # Session.bind doesnt work below. Find a different way to specify dates?
        tobs = session.query(Measurement.tobs).filter(Measurement.date >= start, Measurement.date <= end).statement, session.bind)

        tobs_dictionary2={}
        tobs_dictionary2["TMIN"]=tobs.describe().loc[tobs.describe().index='min']['tobs'][0]
        tobs_dictionary2["TAVG"]=tobs.describe().loc[tobs.describe().index='mean']['tobs'][0]
        tobs_dictionary2["TMAX"]=tobs.describe().loc[tobs.describe().index='mean']['tobs'][0]

        return jsonify(tobs_dictionary2)


if __name__ == "__main__":
    app.run(debug = True)
