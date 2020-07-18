import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from sqlalchemy import literal

import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

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


@app.route("/api/v1.0/precipitation")
def dates():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement data including prcp of each date"""
    # Query all dates in last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23', Measurement.date<='2017-08-23').order_by(Measurement.date).all()

    session.close()
   
    
    # Create a dictionary from the row data and append to a list of all_dates
    all_dates = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_dates.append(prcp_dict)

    return jsonify(all_dates)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query most active station

    results = session.query(Measurement.station,Measurement.date, Measurement.prcp).filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23', Measurement.date<='2017-08-23').order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    active_station = list(np.ravel(results))

    return jsonify(active_station)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #convert to date
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    
    # Query all min, max, avg from start date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date>=start_date)).all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #convert to date
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date = dt.datetime.strptime(start,'%Y-%m-%d')

    # Query all min, max, avg from start to end date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs).filter(Measurement.date>=start_date, Measurement.date<=end_date)).all()

    session.close()

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=False)
    
    
    
    
    
    
    