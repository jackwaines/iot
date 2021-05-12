from flask import Flask, jsonify, render_template, request, Response
from flask_mqtt import Mqtt
from datetime import datetime
import webbrowser
import time
import json
import logging

temp = 0
hum = 0
pre = 0

temperature = 0
humidity = 0
pressure = 0

city = 0
wind = 0
description = 0
icon = 0

day = 0
night = 0
prediction = 0
instuction = 0
email = 0

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'AWS_IP_adress' # replace your AWS IP_adress
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'mqtt_user_name' # replace your mqtt user_name
app.config['MQTT_PASSWORD'] = 'mqtt_Passwd' # replace your mqtt Passwd
app.config['MQTT_REFRESH_TIME'] = 1.0
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sensor')
    mqtt.subscribe('api')
    mqtt.subscribe('forecast')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    global temp, hum, pre
    global temperature, humidity, pressure
    global city, wind, description, icon
    global day, night, prediction, instuction, email

    topic = message.topic
    if topic == 'sensor':
        sensor = message.payload.decode()
        sensor_data = json.loads(sensor)

        temp = sensor_data["temp"]
        hum = sensor_data["hum"]
        pre = sensor_data["pre"]
        # print(senosr_data)

    if topic == 'api':
        api = message.payload.decode()
        api_data = json.loads(api)
        
        temperature = api_data["temperature"]
        humidity = api_data["humidity"]
        pressure = api_data["pressure"]

        wind = api_data["wind"]
        city = api_data["city"]
        description = api_data["description"]
        icon = api_data["icon"]
        prediction = api_data["prediction"]
        instuction = api_data["instuction"]
        email = api_data["email"]
        # print(api_data)

    if topic == 'forecast':
        forecast = message.payload.decode()
        forecast_data = json.loads(forecast)

        day = forecast_data["day"]
        night = forecast_data["night"]
        # print(forecast_data)

@app.route('/_stuff', methods = ['GET'])
def stuff():
    global temp, hum, pre
    global temperature, humidity, pressure
    global city, wind, description, icon
    global day, night, prediction, instuction, email
    
    return jsonify( temp=temp, hum=hum, pre=pre, 
                    temperature=temperature, humidity=humidity, pressure=pressure,
                    city=city, wind=wind, description=description, icon=icon,
                    day= day, night=night, prediction=prediction, instuction=instuction, email=email)


@app.route('/cool_form', methods=['GET', 'POST'])
def cool_form():
    return render_template('cool_form.html')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)