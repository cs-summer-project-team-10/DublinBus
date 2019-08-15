import requests
import json
import psycopg2
import datetime

while True:
    try:
        params = {
            'database': 'weather',
            'user': 'stephen',
            'password': '1993',
            'host': 'localhost',
            'port': 5432
            }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print("Database connected")

        #psql_query = 'INSERT INTO current_weather (city, weather_id, weather_main, weather_description, weather_temp, weather_rain, weather_humidity, timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);'
        #values = ("Dublin City", "10d", "cloud", "cloudy", 19.2, 0, 85, date)

        #response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Buenaventura,CO&appid=0927fd5dff272fdbd486187e54283310")
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310")
        weather_data = json.loads(response.content.decode('utf-8'))

        key = weather_data['name']
        weather_id = weather_data['weather'][0]['id']
        weather_main = weather_data['weather'][0]['main']
        weather_description = weather_data['weather'][0]['description']

        weather_temp = round(weather_data['main']['temp'] - 273.15, 2)
        weather_humidity = weather_data['main']['humidity']

        timestamp = weather_data['dt']
        date = datetime.datetime.fromtimestamp(timestamp)

        if "rain" in weather_data:

            if "1h" in weather_data['rain']:
                weather_rain = weather_data['rain']["1h"]

            elif "3h" in weather_data['rain']:
                weather_rain = weather_data['rain']["3h"]/3
        else:
            weather_rain = 0

        psql_update_query = 'INSERT INTO current_weather (city, weather_id, weather_main, weather_description, weather_temp, weather_rain, weather_humidity, timestamp) \
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (city) DO UPDATE  SET weather_id = excluded.weather_id, weather_main = excluded.weather_main, \
                            weather_description = excluded.weather_description, weather_temp = excluded.weather_temp, weather_rain = excluded.weather_rain, \
                            weather_humidity = excluded.weather_humidity, timestamp = excluded.timestamp;'

        values = ("Dublin City", weather_id, weather_main, weather_description, weather_temp, weather_rain, weather_humidity, date)
        curs.execute(psql_update_query, values)

        conn.commit()


    except (Exception, psycopg2.Error) as error :
        print(error)

    finally:
        if(conn):
            curs.close()
            conn.close()
            print("PostgreSQL connection is closed")

    break
    #sleep 1 hour
    #sleep 3600
