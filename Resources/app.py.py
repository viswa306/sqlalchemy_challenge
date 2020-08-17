import numpy as np
import os
import sqlalchemy
from sqlalchemy import desc
import datetime as dt
from datetime import datetime, timedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import alias
from sqlalchemy.sql import column

from flask import Flask, jsonify

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///hawaii.sqlite")
#engine = create_engine("sqlite:///..Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Station = Base.classes.station
Measurement = Base.classes.measurement

####
#Flask Setup
####
app = Flask (__name__)


#################################
#Flask Routes
#################################

    
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>" 
        f"/api/v1.0/start_date=<start_date>&end_date=<end_date>"
        
        

    )
@app.route("/api/v1.0/precipitation")
def precpitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Percipitations"""
    # Query all percipitations
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

        # Create a dictionary from the row data and append to a list of all_percipitation   []
    all_precipitation = []
    for date, prcp in results:
        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        
        all_precipitation.append(Measurement_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session =Session(engine)
    """Retun a list of stations from the dataset"""
    results = session.query(Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    all_stations= list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def mostactive_stations():
    session = Session(engine)
    most_active_stations = session.query(Measurement.station,func.count(Measurement.station)).\
                    group_by(Measurement.station).order_by(desc(func.count(Measurement.station))).all()
    prev_year = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    stmt = session.query(Measurement.date,Measurement.tobs).\
                    filter_by(station=most_active_stations[0][0]).\
                    filter(Measurement.date >= prev_year).all()

    #Return a JSON list of temperature observations (TOBS) for the previous year.

  
    # all_previousyear_tobs =list(np.ravel(stmt))
    # return jsonify(all_previousyear_tobs)



    acive_station_tobs = []
    for date, tobs in stmt:
        stationtobs_dict = {}
        stationtobs_dict["date"] = date
        stationtobs_dict["tobs"] = tobs
        
        acive_station_tobs .append(stationtobs_dict)

    return jsonify(acive_station_tobs)

@app.route("/api/v1.0/start_date/<start_date>")
# function usage example
#calc_temps('2012-02-28')
def calc_temps1(start_date ):
    session = Session(engine)
        
    calc_temps1 =session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start_date).all()                     
   
    return jsonify(calc_temps1)
   
    

@app.route("/api/v1.0/start_date=<start_date>&end_date=<end_date>")
# function usage example
#calc_temps('2012-02-28')
#def calc_temps(start_date ,end_date):
def calc_temps(start_date,end_date):
    session = Session(engine)
    
    calc_temps = session.query(Measurement.date,func.min(Measurement.tobs) , func.avg(Measurement.tobs) , func.max(Measurement.tobs)).\
                     filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()



    
     # Create a dictionary from the row data and append to a list of temp_calc[] to tempcal_dict
    temp_calc = []
    for date, tmin ,tavg,tmax in calc_temps:

        Tempcalc_dict = {}
        Tempcalc_dict["Date"] = date
        Tempcalc_dict["Tmin"] = tmin 
        Tempcalc_dict["Tavg"] = tavg 
        Tempcalc_dict["Tmax"] = tmax 
        temp_calc.append(Tempcalc_dict)

    return jsonify(temp_calc)


   # return jsonify(calc_temps)
   

    
if __name__ == "__main__":
    app.run(debug=True)