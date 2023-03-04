import requests
import json
import datetime
import mysql.connector
import sys
import os
from dotenv import load_dotenv

# Load .env file and assign variables
load_dotenv()
WEATHERBIT_KEY = os.environ.get("WEATHERBIT_API_KEY")
REMOTE_DB_HOST = os.environ.get("DATABASE_HOST")
REMOTE_DB_USER = os.environ.get("W_DATABASE_USER")
REMOTE_DB_PASS = os.environ.get("W_DATABASE_PASS")
REMOTE_DB_NAME = os.environ.get("DATABASE_NAME")

# set up URL and API key
url = "https://api.weatherbit.io/v2.0/current"

# Setup coordinates
mylat = "60.94367565735641"
mylon = "25.648920948828447"

###SQL connection
mydb = mysql.connector.connect(
  host=REMOTE_DB_HOST,
  user=REMOTE_DB_USER,
  password=REMOTE_DB_PASS,
  database=REMOTE_DB_NAME,
  port="3306"
)

#random variables
dateTimeObj = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
mycursor = mydb.cursor()

#fetch data
#r = requests.get(f'https://api.weatherbit.io/v2.0/current?lat=60.94367565735641&lon=25.648920948828447&key={api_key}&include=minutely')
r = requests.get(f'{url}?lat={mylat}&lon={mylon}&key={WEATHERBIT_KEY}&include=minutely')


#parse response
response = json.loads(r.text)
data = response['data']


# set up variables corresponding json rersponse
r_temp = data[0]['temp']
r_city_name = data[0]['city_name']
r_clouds = data[0]['clouds']
r_ts = data[0]['ts']
r_sunrise = data[0]['sunrise']
r_sunset = data[0]['sunset']
r_pres = data[0]['pres']
r_rh = data[0]['rh']
r_uv = data[0]['uv']
r_ghi = data[0]['ghi']
r_solar_rad = data[0]['solar_rad']
r_elev_angle = data[0]['elev_angle']
r_h_angle = data[0]['h_angle']



#send data
sql = "INSERT INTO local_weather (r_temp, r_city_name, r_clouds, r_ts, r_sunrise, r_sunset, r_pres, r_rh, r_uv, r_ghi, r_solar_rad, r_elev_angle, r_h_angle, text13, text14) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (r_temp, r_city_name, r_clouds, r_ts, r_sunrise, r_sunset, r_pres, r_rh, r_uv, r_ghi, r_solar_rad, r_elev_angle, r_h_angle, "Weather data updated from weatherbit.io", dateTimeObj)
mycursor.execute(sql, val)
mydb.commit()
mycursor.close()
mydb.close()
print(dateTimeObj, r_temp, r_city_name, r_clouds, r_ts, r_sunrise, r_sunset, r_pres, r_rh, r_uv, r_ghi, r_solar_rad, r_elev_angle, r_h_angle, "Weather data updated from weatherbit.io")

#finally:
sys.exit()
