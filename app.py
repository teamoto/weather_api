import os
import requests
from geopy.geocoders import Nominatim
from flask import Flask, request, abort, make_response, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# get env variables
DARK_SKY_API_KEY = os.environ['DARK_SKY_API_KEY']

# create a base url to get weather info:
base_url = 'https://api.darksky.net/forecast'
base_url += '/' + DARK_SKY_API_KEY
# specify options for query results
option = "exclude=currently,minutely,hourly,alerts&amp;units=si"


# define a function to return latitude and longitude
def get_geo_location(location):
    """
    Get location info throuh geopy.
    This function returns latitude, longitude, address in a dictionary
    """
    user_agent = 'weather_aip'
    geo_code = Nominatim(user_agent=user_agent).geocode(str(location.strip()),
                                                        language='en-US')
    if geo_code is not None:
        return {
            'latitude': str(geo_code.latitude),
            'longitude': str(geo_code.longitude),
            'address': geo_code.address
        }
    return None


# define function to get weather info
def get_weather(base_url, option, location):
    # Get weather informaiton
    # get locaiton info (lati + long)
    loc = get_geo_location(location)
    if loc is not None:
        # set date info
        d = datetime.today().strftime('%Y-%m-%d')
        search_date = d + 'T00:00:00'
        # create a request url
        request_url = base_url + '/' + loc['latitude'] + ',' + loc['longitude']
        request_url += ',' + search_date + '?' + option
        # query a request to get wather informaiton
        r = requests.get(request_url)
        # get result in a json format
        json_res = r.json()
        # specify condition to set temp unit
        unit_type = '°F' if json_res['flags']['units'] == 'us' else '°C'
        # organize result
        weather = str(json_res['daily']['data'][0]['summary'])
        temp_max = str(json_res['daily']['data'][0]['apparentTemperatureMax'])
        temp_min = str(json_res['daily']['data'][0]['apparentTemperatureMin'])
        # return a result as a dictionary
        return {
            'location': loc['address'],
            'weather': weather,
            'temp_max': (temp_max + unit_type),
            'temp_min': (temp_min + unit_type)
        }
    return None


@app.route('/<string:location>', methods=['GET'])
def get_weather_info(location):
    try:
        if location:
            weather = get_weather(base_url, option, location)
            if weather is not None:
                return make_response(jsonify(weather))
            raise ValueError('An invalid value provided.')
        else:
            raise ValueError('No values provided.')
    except ValueError:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
