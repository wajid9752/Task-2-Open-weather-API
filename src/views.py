from django.shortcuts import render,redirect
from django.http import JsonResponse
import requests
import json
from .models import City
from django.http import JsonResponse
from src.models import City 
from .forms import CustomCityForm

api_key = '12b7467933f9e3c10eb7bccc623bc44f'


def home(request):
    return render(request , "base.html",{'form':CustomCityForm()} )


def get_weather_info(request):
    if request.POST:
        getCity = request.POST.get('city_id')
        if getCity:
            get_city = City.objects.get(id=getCity).city
            resp = weather_api_call(get_city)

            if resp['status'] == "success":
                pass
            return JsonResponse({'data': resp})
        else:
            return JsonResponse({'data': "Please Select City First"})
    
    return JsonResponse({'data': "unexpected"})

### WEATHER  FUNCTIONS and apis call
def _calculate_dew_point(temperature_kelvin, humidity):
    temperature_celsius = temperature_kelvin - 273.15
    return temperature_celsius - ((100 - humidity) / 5)

def _calculate_wind_direction(degrees):
    directions = {
        'N': (0, 22.5),
        'NNE': (22.5, 67.5),
        'NE': (67.5, 112.5),
        'ENE': (112.5, 157.5),
        'E': (157.5, 202.5),
        'ESE': (202.5, 247.5),
        'SE': (247.5, 292.5),
        'SSE': (292.5, 337.5),
        'S': (337.5, 360)
    }
    
    # Iterate over directions and check if degrees fall within the range
    for direction, (lower, upper) in directions.items():
        if lower <= degrees < upper:
            return direction
    # If degrees are not in any defined range, return 'N' (North) as default
    return 'N'

def weather_api_call(city_name):    

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    try:
        response = requests.get(url)

    except Exception as e:
        return "Contact Admin"    


    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        
        # Extract wind details
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        wind_direction = _calculate_wind_direction(wind_deg)
        
        # Extract pressure
        pressure = data['main']['pressure']
        
        # Extract humidity
        humidity = data['main']['humidity']
        
        # Extract UV index
        uv_index = 2  # For simplicity, assuming a constant UV index

        # Extract dew point (assuming the formula for calculating dew point)
        temperature_kelvin = data['main']['temp']
        
        temperature_celsius = temperature_kelvin - 273.15
        dew_point_celsius = _calculate_dew_point(temperature_kelvin, humidity)
        
        # Extract visibility
        visibility = data['visibility'] / 1000  # Convert meters to kilometers
        
        # Print the weather details
        context={
            'status': 'success',
            'city': city_name ,
            'temp' : int(temperature_celsius) ,
            'wind_speed': f'{wind_speed} m/s {wind_direction}',
            'pressure': f'{pressure} hPa' ,
            'humidity': f'{humidity}%' , 
            'uv_index' : uv_index ,
            'dew_point': f'{dew_point_celsius:.1f}°C' ,
            'visibility': f'{visibility:.1f} km'
        }
        return context
    
    else:
        return 'Failed to retrieve weather data'




