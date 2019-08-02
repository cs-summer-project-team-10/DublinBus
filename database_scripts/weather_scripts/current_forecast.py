import requests
import json

while True:

    response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=7778677&APPID=0927fd5dff272fdbd486187e54283310")
    weather_data = json.loads(response.content.decode('utf-8'))
    print(weather_data['dt'])

    weather_id = weather_data['weather'][0]['id']
    weather_main = weather_data['weather'][0]['main']
    weather_description = weather_data['weather'][0]['description']

    weather_temp = round(weather_data['main']['temp'] - 273.15, 2)
    weather_humidity = weather_data['main']['humidity']

    timestamp = weather_data['dt']

    try:
        weather_rain = weather_data['rain']
        print(weather_rain)
    except:
        pass
    print(weather_id, weather_main, weather_description, weather_temp, weather_humidity, timestamp)
    break
    #insert into table

    #sleep 1 hour
    #sleep 3600
