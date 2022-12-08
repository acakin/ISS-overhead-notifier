import time

import requests
from datetime import datetime
import smtplib

LAT = 39.766705
LNG = 30.525631

email1 = "xyz@gmail.com"
password1 = "***"


def night():

    parameters ={
        "lat": LAT,
        "lng": LNG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    now = str(datetime.now())

    sunset_hour= float(sunset.split("T")[1].split("+")[0].split(":")[0])
    sunset_minute= float(sunset.split("T")[1].split("+")[0].split(":")[1])

    sunrise_hour = float(sunrise.split("T")[1].split("+")[0].split(":")[0])
    sunrise_minute = float(sunrise.split("T")[1].split("+")[0].split(":")[1])

    now_hour = float(now.split(" ")[1].split(".")[0].split(":")[0])
    now_minute = float(now.split(" ")[1].split(".")[0].split(":")[1])

    if (now_hour > sunset_hour and now_minute > sunset_minute) or (now_hour > sunrise_hour and now_minute > sunrise_minute):
        return True


def pos_iss():

    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
    response1.raise_for_status()

    data_iss = response1.json()
    longitude = float(data_iss["iss_position"]["longitude"])
    latitude = float(data_iss["iss_position"]["latitude"])
    if (LNG - 5 < longitude or longitude < LNG + 5) and (latitude < LAT + 5 or latitude > LAT - 5):
        return True


while True:

    time.sleep(60)
    if pos_iss() and night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=email1, password=password1)
            connection.sendmail(from_addr=email1, to_addrs="xyz@yahoo.com",
                                msg=f"Subject:ISS\n\nLook up!")
