import requests
#import os
from datetime import datetime

api_key = '87d845b0b6cf29baa1a73cc34b067a95'
location = input("Enter the city name: ")

complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+api_key
api_link = requests.get(complete_api_link)
api_data = api_link.json()

#create variables to store and display data
temp_city = ((api_data['main']['temp']) - 273.15)
weather_desc = api_data['weather'][0]['description']
hmdt = api_data['main']['humidity']
wind_spd = api_data['wind']['speed']
date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

#print ("-------------------------------------------------------------")
#print ("Weather Stats for - {}  || {}".format(location.upper(), date_time))
#print ("-------------------------------------------------------------")

#print ("Current temperature is: {:.2f} deg C".format(temp_city))
#print ("Current weather desc  :",weather_desc)
#print ("Current Humidity      :",hmdt, '%')
#print ("Current wind speed    :",wind_spd ,'kmph')

data = '''-------------------------------------------------------------\n
Weather Stats for - {}  || {}\n
-------------------------------------------------------------\n
Current temperature is: {:.2f} deg C\n
Current weather desc  :{}\n
Current Humidity      :{} %\n
Current wind speed    :{} kmph\n
'''.format(location.upper(),date_time,temp_city,weather_desc,hmdt,wind_spd)

filename =datetime.now().strftime("%d-%b-%Y-%I-%M")


#Create and write to txt file

f = open("{}-{}.txt".format(location,filename), "w")
f.write(data)
f.close

