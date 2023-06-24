'''Author: https://github.com/manjunani'''
#This code will fetch the weather details for the given city name.
#It will make use of geopy module to get the location details.
#It will make use of weatherapi.com to get the current weather details of the city.

from geopy.geocoders import Nominatim
from constants import *
import requests
import colorama
from colorama import Fore, Back, Style

url = "https://weatherapi-com.p.rapidapi.com/current.json"
headers = {
	"X-RapidAPI-Key": f"{API_KEY}",
	"X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

def get_location_lat_lon(city_name):
    '''
    This function will return the latitude and longitude of the given city name.
    '''
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(f"{city_name}")
    if location != None:
        return location.latitude, location.longitude
    else:
        raise NameError("Error Occured: Please Enter the City Name Again")

def get_weather_data(url, headers, lat, lon):
    '''
    This function will return the weather details of the given latitude and longitude.
    '''
    querystring = {"q": f"{lat},{lon}"}
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise NameError("Error Occured: Please try Again")

def get_location_details(location):
    '''
    This function will return the location details of the given latitude and longitude.
    '''
    print("Location Details: ".upper())
    print(Fore.WHITE + "*"*20)
    for k, v in location.items():
        if "epoch" in k:
            continue
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == list:
            print(Fore.GREEN + f"{CHANGABLE_KEY_ITEMS[k][0].title()}: {v} {CHANGABLE_KEY_ITEMS[k][1]}")
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == str:
            print(Fore.GREEN + f"{CHANGABLE_KEY_ITEMS[k].title()}: {v}")
        else:
            print(Fore.GREEN + f"{k.capitalize()}: {v}")
    print(Fore.WHITE + "*"*20)

def get_current_weather_details(current):
    '''
    This function will return the current weather details of the given latitude and longitude.
    '''
    print("Current Weather Details: ".upper())
    print(Fore.WHITE + "*"*20)
    for k, v in current.items():
        if "epoch" in k or type(v) == dict:
            continue
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == list:
            print(Fore.GREEN + f"{CHANGABLE_KEY_ITEMS[k][0].title()}: {v} {CHANGABLE_KEY_ITEMS[k][1]}")
        elif k in CHANGABLE_KEY_ITEMS and type(CHANGABLE_KEY_ITEMS[k]) == str:
            print(Fore.GREEN + f"{CHANGABLE_KEY_ITEMS[k].title()}: {v}")
        else:
            print(Fore.GREEN + f"{k.capitalize()}: {v}")
    print(Fore.WHITE + "*"*20)

if __name__ == "__main__":
    '''
    This is the main function which will be called when the program is executed.
    '''
    while True:
        city_name = input(Fore.GREEN + "Please Enter the City Name:")
        try:
            lat,lon = get_location_lat_lon(city_name)
            print("Hey There! You have entered the city name as: ", city_name)
            print("Fetching the Weather Details for the City: ", city_name)
            print(Fore.WHITE + "*"*20)
            my_weather_data = get_weather_data(
                url, headers, lat, lon)
            for key, value in my_weather_data.items():
                if key == 'location':
                    get_location_details(value)
                elif key == 'current':
                    get_current_weather_details(value)
            retry = input("Do you want to continue? (Y/N)")
            if retry.lower() == 'n':
                break
        except NameError as e:
            print(Fore.RED + str(e))
    