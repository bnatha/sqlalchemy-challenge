import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import style
style.use('fivethirtyeight')

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

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
        f"Homepage:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<end><br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    maxdate = dt.datetime(2017,8,23)
    mindate = dt.datetime(2016,8,23)

    # Query 
    prcp_data = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date <= maxdate).filter(measurement.date >= mindate).all()
    
    session.close()

    all_prcp = []
    # Convert to json
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query stations
    stations = session.query(station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    all_stations = list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query temperatures
    temp_results = session.query(measurement.station, measurement.tobs).\
                filter(measurement.station == best_station).\
                filter(measurement.date <= maxdate).filter(measurement.date >= mindate).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_temps = list(np.ravel(temp_results))

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)
