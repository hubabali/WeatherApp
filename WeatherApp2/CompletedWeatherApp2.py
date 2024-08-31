import requests
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()

api_key = os.getenv('api_key')

userInput = input("Enter a city: ")

# Get current weather data
weatherData = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={userInput}&units=imperial&APPID={os.getenv('api_key')}")
current_weather = weatherData.json()['weather'][0]['main']
current_temp = round(weatherData.json()['main']['temp'])

print(f"\nCurrent weather in {userInput}:")
print(f"Weather: {current_weather}")
print(f"Temperature: {current_temp}°F\n")

# Get 5-day/3-hour forecast data
forecastData = requests.get(
    f"https://api.openweathermap.org/data/2.5/forecast?q={userInput}&units=imperial&APPID={api_key}")

forecast = forecastData.json()

print(f"5-Day Forecast for {userInput}:")

# Loop through the forecast data to get weather info for each day at 12:00 PM
displayed_days = set()
for entry in forecast['list']:
    time = entry['dt_txt']
    
    # Extract the date and time
    date = time.split(" ")[0]
    hour = time.split(" ")[1]

    # Check if it's 12:00 PM and the day has not been displayed yet
    if hour == "12:00:00" and date not in displayed_days:
        weather = entry['weather'][0]['main']
        temp = round(entry['main']['temp'])
        
        # Print the forecast for that day
        print(f"{date}: Weather: {weather}, Temperature: {temp}°F")
        
        # Add the date to the set of displayed days
        displayed_days.add(date)

    # Stop after 5 days have been displayed
    if len(displayed_days) == 5:
        break
