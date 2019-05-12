import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Session maneja Querys
# Base es para objetos en python
# Engine es para la  conexion

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    """Return  stations"""
    # Query all stations
    results = session.query(Station.name).all()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return precipitations"""
    # Query all passengers
    results = session.query(Measurement.prcp, Measurement.date).all()

    # Create a dictionary 
    presip = []
    for date, prcp in results:
        presip_dict = {}
        presip_dict["date"] = date
        presip_dict["prcp"] = prcp
        presip.append(presip_dict)

    return jsonify(presip)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return tobs"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-8-23').all()
    # Create a dictionary 
    tobs = []
    for date, tobs2 in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs2
        tobs.append(tobs_dict)

    return jsonify(tobs)

@app.route("/api/v1.0/<date>")
def dates(date):
    results = session.query (Measurement.date, Measurement.prcp).filter(Measurement.date >= date).all()
    dates = []
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        dates.append(dates_dict)

    return jsonify(dates)


if __name__ == '__main__':
    app.run(debug=True)
