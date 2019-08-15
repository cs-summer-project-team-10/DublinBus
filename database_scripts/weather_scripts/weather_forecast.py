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

        response = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=7778677&APPID=0927fd5dff272fdbd486187e54283310")
        weather_data = json.loads(response.content.decode('utf-8'))
        weather_data_list = weather_data['list']


        for i in range(len(weather_data_list)):
            timestamp = weather_data_list[i]["dt"]
            date = datetime.datetime.fromtimestamp(timestamp)

            weather_id = weather_data_list[i]['weather'][0]['id']
            weather_main = weather_data_list[i]['weather'][0]['main']
            weather_description = weather_data_list[i]['weather'][0]['description']

            weather_temp = round(weather_data_list[i]['main']['temp'] - 273.15, 2)
            weather_humidity = weather_data_list[i]['main']['humidity']

            if "rain" in weather_data_list[i]:

                if "1h" in weather_data_list[i]['rain']:
                    weather_rain = weather_data_list[i]['rain']["1h"]

                elif "3h" in weather_data_list[i]['rain']:
                    weather_rain = weather_data_list[i]['rain']["3h"]/3
            else:
                weather_rain = 0

            psql_insert_query = 'INSERT INTO weather_forecast (city, weather_id, weather_main, weather_description, weather_temp, weather_rain, weather_humidity, timestamp) \
                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (timestamp) DO NOTHING;'
            values = ("Dublin City", weather_id, weather_main, weather_description, weather_temp, weather_rain, weather_humidity, date)

            curs.execute(psql_insert_query, values)
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
