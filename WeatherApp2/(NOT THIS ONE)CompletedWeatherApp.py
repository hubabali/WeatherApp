'''
import requests
from dotenv import load_dotenv
import os 

def configure():
    load_dotenv()
    return os.getenv('api_key')


configure()
api_key = configure()

userInput = input("Enter a city: ")

# Get current weather data
weatherResponse = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={userInput}&units=imperial&APPID={os.getenv('api_key')}")

# Print the response for debugging
weatherData = weatherResponse.json()
print("Current Weather Response:", weatherData)

# Check if the response is successful
if weatherResponse.status_code == 200:
    if 'weather' in weatherData and 'main' in weatherData:
        current_weather = weatherData['weather'][0].get('main', 'N/A')
        current_temp = round(weatherData['main'].get('temp', 0))
        
        print(f"\nCurrent weather in {userInput}:")
        print(f"Weather: {current_weather}")
        print(f"Temperature: {current_temp}°F\n")
    else:
        print("Unexpected response format for current weather data.")
else:
    print(f"Error fetching current weather data: {weatherData.get('message', 'Unknown error')}")

# Get 5-day/3-hour forecast data
forecastResponse = requests.get(
    f"https://api.openweathermap.org/data/2.5/forecast?q={userInput}&units=imperial&APPID={os.getenv('api_key')}")

# Print the response for debugging
forecastData = forecastResponse.json()
print("5-Day Forecast Response:", forecastData)

# Check if the response is successful
if forecastResponse.status_code == 200:
    if 'list' in forecastData:
        displayed_days = set()
        for entry in forecastData['list']:
            time = entry.get('dt_txt', '')
            
            # Extract the date and time
            date = time.split(" ")[0]
            hour = time.split(" ")[1]

            # Check if it's 12:00 PM and the day has not been displayed yet
            if hour == "12:00:00" and date not in displayed_days:
                weather = entry.get('weather', [{}])[0].get('main', 'N/A')
                temp = round(entry.get('main', {}).get('temp', 0))
                
                # Print the forecast for that day
                print(f"{date}: Weather: {weather}, Temperature: {temp}°F")
                
                # Add the date to the set of displayed days
                displayed_days.add(date)

            # Stop after 5 days have been displayed
            if len(displayed_days) == 5:
                break
    else:
        print("Unexpected response format for forecast data.")
else:
    print(f"Error fetching forecast data: {forecastData.get('message', 'Unknown error')}")
'''