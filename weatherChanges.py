import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from datetime import datetime
from urllib.parse import quote

def get_coordinates(location):
    encoded_location = quote(location)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_location}&format=json&limit=1"
    headers = {
        'User-Agent': 'weatherChanges/1.0 (hasibur959@gmail.com)'  # Replace with your app name and contact email
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        # Check if the response contains location data
        if data:
            lat = float(data[0].get('lat', None))
            lon = float(data[0].get('lon', None))
            print(f"Latitude: {lat}, Longitude: {lon}")  # Debug print
            return lat, lon
        else:
            print("No data found for the specified location.")  # Debug print
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")  # Debug print
        return None, None
    except ValueError as e:
        print(f"Error parsing latitude/longitude: {e}")  # Debug print
        return None, None


# Function to get 7-day weather forecast data using Open-Meteo with provided coordinates
def get_weather_data(latitude, longitude):
    # Form the URL for fetching weather data from Open-Meteo API
    # f"&timezone=America%2FNew_York"
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,weathercode"
        f"&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,"
        f"showers,snowfall,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,sunshine_duration"
        f"&timezone=Asia%2FKolkata"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        weather_data = response.json()
        
        # Debugging: Print response data if needed
        print(f"Weather data received...")  # Debug print
        
        # Check if daily and hourly data is available
        if 'daily' in weather_data and 'hourly' in weather_data:
            return weather_data
        else:
            print("Daily or hourly weather data not available in the response.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")  # Debug print
        return None


# Function to get weather description from the weather code
def get_weather_description(weather_code):
    weather_descriptions = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog", 51: "Light rain", 52: "Moderate rain",
        53: "Heavy rain", 55: "Very heavy rain", 56: "Light freezing rain",
        57: "Heavy freezing rain", 61: "Light showers", 62: "Moderate showers",
        63: "Heavy showers", 65: "Heavy showers", 66: "Light sleet", 67: "Heavy sleet",
        71: "Light snow", 72: "Moderate snow", 73: "Heavy snow", 75: "Heavy snow",
        77: "Snow grains", 80: "Showers of rain", 81: "Heavy showers",
        82: "Violent showers", 85: "Snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with hail"
    }
    return weather_descriptions.get(weather_code, "Unknown")

# Function to convert date to day of the week
def get_day_of_week(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%A")
    except ValueError:
        return "Unknown day"

# Function to update the GUI with weather information
def update_weather():
    location = location_entry.get().strip()
    if location:
        latitude,longitude = get_coordinates(location)
        # print("latitude",latitude)
        # print("longitude",longitude)
        if latitude is not None and longitude is not None:
            weather_data = get_weather_data(latitude, longitude)
            if weather_data and 'daily' in weather_data and 'hourly' in weather_data:
                daily = weather_data['daily']
                hourly = weather_data['hourly']

                for widget in weather_frame.winfo_children():
                    widget.destroy()

                for i in range(len(daily['time'])):
                    date = daily['time'][i]
                    day_of_week = get_day_of_week(date)

                    temp_max = daily.get('temperature_2m_max', [None])[i]
                    temp_min = daily.get('temperature_2m_min', [None])[i]
                    precipitation = daily.get('precipitation_sum', [None])[i]
                    wind_speed = daily.get('wind_speed_10m_max', [None])[i]
                    weather_code = daily.get('weathercode', [None])[i]
                    weather_description = get_weather_description(weather_code)

                    temp_curr = hourly.get('temperature_2m', [None])[i]
                    relative_humidity = hourly.get('relative_humidity_2m', [None])[i]
                    apparent_temperature = hourly.get('apparent_temperature', [None])[i]
                    wind_direction = hourly.get('wind_direction_10m', [None])[i]
                    wind_gusts = hourly.get('wind_gusts_10m', [None])[i]
                    is_day = hourly.get('is_day', [None])[i]
                    sunshine_duration = hourly.get('sunshine_duration', [None])[i]

                    card = tk.Frame(weather_frame, bg="#ffffff", bd=1, relief=tk.RAISED, padx=10, pady=10)
                    card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

                    day_label = tk.Label(card, text=f"{day_of_week}, {date}", font=("Arial", 10, "bold"), bg="#ffffff")
                    day_label.pack(pady=5)

                    if temp_curr is not None:
                        temp_curr_label = tk.Label(card, text=f"Current Temp: {temp_curr} °C", bg="#ffffff")
                        temp_curr_label.pack(pady=5)

                    if temp_max is not None:
                        temp_max_label = tk.Label(card, text=f"Max Temp: {temp_max} °C", bg="#ffffff")
                        temp_max_label.pack(pady=5)

                    if temp_min is not None:
                        temp_min_label = tk.Label(card, text=f"Min Temp: {temp_min} °C", bg="#ffffff")
                        temp_min_label.pack(pady=5)

                    if apparent_temperature is not None:
                        apparent_temp_label = tk.Label(card, text=f"Feels Like: {apparent_temperature} °C", bg="#ffffff")
                        apparent_temp_label.pack(pady=5)

                    if precipitation is not None:
                        precipitation_label = tk.Label(card, text=f"Precipitation: {precipitation} mm", bg="#ffffff")
                        precipitation_label.pack(pady=5)

                    if relative_humidity is not None:
                        humidity_label = tk.Label(card, text=f"Humidity: {relative_humidity} %", bg="#ffffff")
                        humidity_label.pack(pady=5)

                    if wind_speed is not None:
                        wind_speed_label = tk.Label(card, text=f"Wind: {wind_speed} km/h", bg="#ffffff")
                        wind_speed_label.pack(pady=5)

                    if wind_gusts is not None:
                        wind_gust_label = tk.Label(card, text=f"Wind Gusts: {wind_gusts} km/h", bg="#ffffff")
                        wind_gust_label.pack(pady=5)

                    if wind_direction is not None:
                        wind_direction_label = tk.Label(card, text=f"Wind Direction: {wind_direction}°", bg="#ffffff")
                        wind_direction_label.pack(pady=5)

                    if sunshine_duration is not None:
                        sunshine_label = tk.Label(card, text=f"Sunshine Duration: {sunshine_duration} min", bg="#ffffff")
                        sunshine_label.pack(pady=5)

                    if is_day is not None:
                        day_status = "Day" if is_day else "Night"
                        is_day_label = tk.Label(card, text=f"Time of Day: {day_status}", bg="#ffffff")
                        is_day_label.pack(pady=5)

                    if weather_description:
                        weather_description_label = tk.Label(card, text=f"Weather: {weather_description}", bg="#ffffff")
                        weather_description_label.pack(pady=5)

                for i in range(7):
                    weather_frame.grid_columnconfigure(i, weight=1)
            else:
                messagebox.showwarning("Weather Data", "Weather data not available.")
        else:
            messagebox.showwarning("Location Error", "Could not retrieve coordinates for the specified location.")
    else:
        messagebox.showwarning("Input Error", "Please enter a location.")

# Main execution block
if __name__ == "__main__":
    # Set up the GUI
    root = tk.Tk()
    root.title("7-Day Weather Forecast")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Create a frame for the input section
    input_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    input_frame.pack(pady=20)

    location_label = tk.Label(input_frame, text="Enter Location:", font=("Arial", 12), bg="#ffffff")
    location_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    location_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    location_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    get_weather_button = ttk.Button(input_frame, text="Get Weather", command=update_weather)
    get_weather_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Create a frame for displaying the weather cards
    weather_frame = tk.Frame(root, bg="#f0f0f0")
    weather_frame.pack(pady=10, fill="both", expand=True)

    root.mainloop()
