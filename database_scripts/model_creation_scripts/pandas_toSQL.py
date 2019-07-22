from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy


engine = create_engine('postgresql+psycopg2://student:group10bus@127.0.0.1:3333/dub_bus')


#data = pd.read_csv("../csvs/shapes.txt")
#data.to_sql('test', engine, if_exists = 'append', chunksize = 1000)

data = pd.read_csv("../csvs/stop_times.txt")

data = data[['trip_id', 'stop_id', 'stop_sequence', 'arrival_time', 'departure_time', 'stop_headsign', 'shape_dist_traveled']]

data.to_sql(name = 'map_trip_stop_times', con = engine, if_exists = 'append', chunksize = 1000, index = False, \
            dtype = {"trip_id" : sqlalchemy.types.VARCHAR(length=100),
                    "stop_id" : sqlalchemy.types.VARCHAR(length=100),
                    "stop_sequence" : sqlalchemy.types.INTEGER(),
                    "scheduled_arrival_time" : sqlalchemy.DateTime(),
                    "scheduled_dept_time" : sqlalchemy.DateTime(),
                    "stop_headsign" : sqlalchemy.types.VARCHAR(length=200),
                    "distance_travelled" : sqlalchemy.types.VARCHAR(length=200)})
