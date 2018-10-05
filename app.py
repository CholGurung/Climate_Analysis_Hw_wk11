#libraries to import
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect


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

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


#index page
@app.route("/")
def home():
    return (f"Climate API<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start/<br/>"
    f"/api/v1.0/start/end/")




#Query for the dates and temperature observations from the last year.
#Convert the query results to a Dictionary using date as the key and tobs as the value.
@app.route("/api/v1.0/precipitation")
def temp_observ():
    query_result = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").all()
    results = list(np.ravel(query_result))

    return jsonify(results)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station():
    station_result = session.query(Station.station, Station.name).all()
    results = list(np.ravel(station_result))

    return jsonify(results)




#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def temp_observation():
    results = []
    query_result = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    results = list(np.ravel(query_result))
    return jsonify(results)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def calculate_temp(start):
    temps_query = session.query(func.min(Measurement.tobs),\
                                func.max(Measurement.tobs),\
                                func.avg(Measurement.tobs)).\
                                filter(Measurement.date >= start).first()
   
    temperature_dict = {"TMIN": temps_query[0], "TMAX": temps_query[1], "TAVG": temps_query[2]}
    return jsonify(temperature_dict)



    
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def calculate_temp_range(start,end):
    temp_range_query = session.query(func.min(Measurement.tobs),\
                                     func.max(Measurement.tobs),\
                                     func.avg(Measurement.tobs)).\
                                     filter(Measurement.date >= start).\
                                     filter(Measurement.date <= end).all()
    print("its here ")
    #create dictionary from result
    temperature_dict1 = {"TMIN": temp_range_query[0], "TMAX": temp_range_query[1],\
                         "TAVG": temp_range_query[2]}
    return jsonify(temperature_dic1)

if __name__ == '__main__':
    app.run(debug=True)
