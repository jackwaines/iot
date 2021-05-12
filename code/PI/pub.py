# import libs
import paho.mqtt.client as mqtt
import os
import time
import random
from time import strftime
from datetime import datetime
import requests
import json
import schedule

import numpy as np
import tensorflow as tf

# load the AI model
model2 = tf.keras.models.load_model('./my_model')

# MQTT Functions
def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

# gettiing dict with temperature, date and icon for forecast
def day_forecast():
    temp_day = []
    for i in forecast_response['list']:
        foo = '12:00:00'
        if foo in i['dt_txt']:
            dictor = {
                'date': i['dt'],
                'temp': i['main']['temp'],
                'icon': i['weather'][0]['icon'],
                'date_txt': i['dt_txt']
            }
            temp_day.append(dictor)

    # This for loop is selecting all DT from respoonse and making list of it
    temport = []
    for d in temp_day:
        temport.append(d['date'])

    # This loop converting timestamp DT format to week days names and making list of it
    dates_formated = []
    for value in temport:
        dates_formated.append(
            datetime.utcfromtimestamp(value).strftime('%A'))
    
    return [temp_day, dates_formated]

def night_forecast():
    temp_night = []
    for i in forecast_response['list']:
        foo = '03:00:00'
        if foo in i['dt_txt']:
            dictor = {
                'date': i['dt_txt'],
                'temp': i['main']['temp'],
            }
            temp_night.append(dictor)
    return temp_night

# send email function
def send_mail(city, temperature, humidity, pressure, wind, description):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    mail= MIMEMultipart()

    sender_email = "sender@gmail.com" # replace with sender mail
    rec_email = "reciver@gmail.com" # replace with reciver mail
    password = "Passwd" # replace with sender mail password

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)

    mail['From']='Weather Notification System'
    mail['To'] = rec_email
    mail['Subject']='Weather App – Alert'

    city = city
    temperature = str(temperature)+ " C"
    humidity = str(humidity) + " %"
    pressure = str(pressure) + " hPa"
    wind = str(wind) + " m/s"
    description = description

    body=" City: "+str(city)+"\n Temperature: "+str(temperature)+"\n Humidity: "+str(humidity)+"\n Pressure: "+str(pressure)+"\n Wind: "+str(wind)+"\n Description: "+ str(description)

    mail.attach(MIMEText(body,'plain')) 
    msg=mail.as_string()
    server.sendmail(sender_email, rec_email, msg)
    print('Mail Sent')

email = "Email Will Send Your Mail."

def email12():
    global email
    email = "Email Send At 12PM. Please Check Your Mail."
    
def email06():
    global email
    email = "Email Send At 06PM. Please Check Your Mail."

# schedule mail send time
schedule.every().day.at("00:00").do(lambda: send_mail(city_float, temp_float, hum_float, pre_float, wind_float, des_float))
schedule.every().day.at("18:00").do(lambda: send_mail(city_float, temp_float, hum_float, pre_float, wind_float, des_float))

schedule.every().day.at("00:00").do(email12)
schedule.every().day.at("18:00").do(email06)

# generate random sensor values
def generate_sensor_data():
    global temp, hum, pre

    temp = random.randint(20, 30)
    hum = random.randint(60, 90)
    pre = random.randint(1000, 1120)

# AI prediction
def predict(temp_float, hum_float, pre_float):
    input = np.array([[temp_float, hum_float, pre_float]])
    pred = model2.predict_classes(input)
    suggestion = 0

    if pred == [1]:
        suggestion = "Most Probably Today Will Rain. So, Don't Miss Your Jacket."
    if pred == [2]:
        suggestion = "Most Probably Today Will Snow."
    else:
        suggestion = "I Cannot Predict Whether Rain or Snow."
    return suggestion

# check out and in temp
def check_temp(temp_float, temp):
    instuction = 0
    if temp_float > temp:
        instuction = "Outside Temperature Higher Than Inside."
    else:
        instuction = "Inside Temperature Higher Than Outside."
    return instuction

try:
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_publish = on_publish

    # Connect
    mqttc.username_pw_set("user_name", "passwd")  # Replace with mqtt username and passwd
    mqttc.connect('IP_Adress', 1883, 60) # Replace your AWS E2C IP_address

    # Continue the network loop, exit when an error occurs
    while True :
        global temp_float, hum_float, pre_float, wind_float, city_float, des_float

        generate_sensor_data()

        API_KEY = '30ad27b312182fa9f7569003a337536b'

        # Replace your city name
        city = 'Middlesbrough'
        # getting api
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'

        response = requests.get(url).json()

        # If name of city is wrong spell or unknown
        if response.get('cod') != 200:
            message = response.get('message', '')

        weather = {
            'city': city,
            'temperature': response['main']['temp'],
            'humidity': response['main']['humidity'],
            'pressure': response['main']['pressure'],
            'wind': response['wind']['speed'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        temp_float = weather.get('temperature')
        hum_float = weather.get('humidity')
        pre_float = weather.get('pressure')
        wind_float = weather.get('wind')
        city_float = weather.get('city')
        des_float = weather.get('description')
        temp_int = round(temp_float)

        # This api is showing forecast for five days with days/nights
        url_forecast = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={API_KEY}'

        forecast_response = requests.get(url_forecast).json()

        day = day_forecast()
        night = night_forecast()

        prediction = predict(temp_float, hum_float, pre_float)
        instuction = check_temp(temp_float, temp)

        # print(prediction)

        sensor = {
            "temp": temp,
            "hum": hum,
            "pre": pre
        }

        api = {
            "temperature": temp_int,
            "humidity": weather.get('humidity'),
            "pressure": weather.get('pressure'),
            "wind": weather.get('wind'),
            "city" :weather.get('city'),
            "description": weather.get('description'),
            "icon": weather.get('icon'),
            "prediction": prediction,
            "instuction": instuction,
            "email": email
        }

        forecast = {
            "day": day,
            "night": night
        }

        # send MQTT data
        mqttc.publish("sensor", (json.dumps(sensor)))
        mqttc.publish("api", (json.dumps(api)))
        mqttc.publish("forecast", (json.dumps(forecast)))
        print('published')
        schedule.run_pending()
        time.sleep(1)

except:
    exit
