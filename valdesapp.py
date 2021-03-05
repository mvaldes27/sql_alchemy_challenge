import numpy as np
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

###############################################
#Database setup
###############################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using automap_base()
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

#save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

###############################################
#Flask setup
###############################################
app = Flask(__name__)

###############################################
# Flask Routes
###############################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
        #f"/api/v1.0/<start><br/>"
        #f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session from Python to the DB
    session = Session(engine) 

    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    """Return the JSON representation of your dictionary."""

    recent_year = dt.date(2017, 8 ,23)
    # Calculate the date one year from the last date in data set.
    previous_year = recent_year - dt.timedelta(days=365)
    precip_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    # type(precip_query)

    session.close()

    # Convert list of tuples into normal list
    # precipitation = list(np.ravel(precip_query))
    

    return jsonify(precip_query)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session from Python to the DB
    session = Session(engine) 

    """Return a JSON list of stations from the dataset."""
    # Query all active stations
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # stations = list(np.ravel(active_stations))
    stations = active_stations

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session from Python to the DB
    session = Session(engine)

    """Query the dates and temperature observations of the most active station for the last year of data."""
    """Return a JSON list of temperature observations (TOBS) for the previous year."""





if __name__ == "__main__":
    app.run(debug=True)

