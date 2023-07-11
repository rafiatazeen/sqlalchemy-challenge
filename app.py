# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify




#################################################
# Database Setup
#################################################

#engine = create_engine("sqlite:///hawaii.sqlite") - this path wasn't working so had to use the relative path
engine = create_engine("sqlite:///Module 10 Challenge\Starter_Code\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation/<br/>"
        f"/api/v1.0/stations/<br/>"
        f"/api/v1.0/tobs/<br/>"
        f"/api/v1.0/2016-08-23/<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23/"
    )


#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation/")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()
    session.close()
    prcp_data_list = []
    for date, prcp in prcp_data:
        precipitation_dict = {}
        precipitation_dict = {date: prcp}
        prcp_data_list.append(precipitation_dict)
    return jsonify(prcp_data_list)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations/")
def stations():
    session = Session(engine)
    stations_data = session.query(Station.station).all()
    session.close()
    all_stations_data = list(np.ravel(stations_data))
    return jsonify(all_stations_data)

# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs/")
def tobs():
    session = Session(engine)
    active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first().station
    active_temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == active_station).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()
    session.close()
    all_active_temps = list(np.ravel(active_temps))
    return jsonify(all_active_temps)


#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start.
@app.route("/api/v1.0/2016-08-23/")
def start():
    session = Session(engine)
    temps_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').all()
    session.close()
    all_temps = list(np.ravel(temps_start))
    return jsonify(all_temps)

# #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
@app.route("/api/v1.0/2016-08-23/2017-08-23/")
def start_end():
    session = Session(engine)
    temps_start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= '2016-08-23').filter(Measurement.date <= '2017-08-23').all()
    session.close()
    all_temps_start_end = list(np.ravel(temps_start_end))
    return jsonify(all_temps_start_end)



if __name__ == "__main__":
    app.run(debug=True)