from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify
import numpy as np
import pandas as pd

# Database Setup
database_path = "../Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{database_path}")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

#print(Base.classes.keys())

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Define a session
session = Session(engine)
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all routes that are available."""
    return ("List of Available Routes:<br/> \
            /api/v1.0/precipitation<br/> \
            /api/v1.0/stations<br/> \
            /api/v1.0/tobs<br/> \
            /api/v1.0/start<br/> \
            /api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def dates():
    """ Return a list of all dates and temperature observations
    """
    # Query all dates and temperature observations for last year
    one_year_prcp = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date.between('2016-08-23', '2017-08-23')).\
            group_by(Measurement.date).order_by(Measurement.date).all()

    #Convert query results to dictionary
    prcp_data = []
    for prcp in one_year_prcp:
        prcp_dict = {}
        prcp_dict["date"] = prcp.date
        prcp_dict["prcp"] = prcp.prcp
        prcp_data.append(prcp_dict)

    # Convert list of tuples into normal list
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Measurement.station).\
                      filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
                      
    all_stations = []
    for station in station_results:
        station_dict = {}
        station_dict["station"]=station.station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_tobs = session.query(Measurement.tobs).\
                    filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
                      
    tobs_data = []
    for tob in one_year_tobs:
        tob_dict = {}
        tob_dict["Temp. Observations"]= tob.tobs
        tobs_data.append(tob_dict)

    return jsonify(tobs_data)

if __name__ == "__main__":
    app.run(debug=True)