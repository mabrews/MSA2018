#Using Yelp Fusion code sample to grab Yelp reviews
#https://github.com/Yelp/yelp-fusion
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import csv
import os



# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode

API_KEY= "OaloKRAWXwFo_Kr0wUVPo8J3S8Emkn2zgAyYRAu3jxY87PwfirY1wtyvsOaNwayvfGmfk-Y-4C_5_xuQzLqFGmSQnmKLsRn9oJ8gGmB_uhpYViSjLLx9rLDeiGY5WnYx"


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'fiction kitchen'
DEFAULT_LOCATION = 'Raleigh, NC'
SEARCH_LIMIT = 1


def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    #review_dict = response.json()
    return response.json()


def search(api_key, term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

#Google Places API info
#Using googleplaces package - python wrapper around Google Places API
#https://github.com/slimkrazy/python-google-places
from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyCbRpPJDFO1sgKQc_GjM_Tt29ljFQTZ5bU'

google_places = GooglePlaces(YOUR_API_KEY)


#looping through our list to grab reviews

list = ["Ajisai", 
"Beasley's Chicken and Honey", 
"Bella Monica", 
"Bida Manda", 
"Big Ed's City Market", 
"Bosphorus", 
"Brixx", 
"Buku: Global Street Food", 
"Cameron Bar and Grill", 
"Capital Club 16", 
"Centro", 
"Chanticleer", 
"chargrill", 
"Chick-fil-A", 
"Chipotle", 
"Chopt", 
"Chubby's Tacos", 
"Cilantro", 
"City Market Sushi", 
"Cookout", 
"Cowfish", 
"Dharani Express", 
"DP Dough", 
"El Centro", 
"Farmer's Market", 
"Fiction Kitchen", 
"Five Guys", 
"Flying Biscuit", 
"garland", 
"Gonza Tacos Y Tequila", 
"Gravy", 
"Guasaca", 
"Humble Pie", 
"Istanbul", 
"Kashin", 
"Kebab and Curry", 
"Kumo Sushi", 
"Linus and Pepper's", 
"Lucky 32", 
"Lynwood Grill", 
"Mateo", 
"Mellow Mushroom", 
"NC Seafood Restaurant", 
"Oak City Meatballs", 
"Oakwood Cafe", 
"Only Burger Food Truck", 
"Parkside", 
"Philly's", 
"Poole's Diner", 
"Remedy Diner", 
"Ruckus", 
"Sitti", 
"Stanbury", 
"Sushi Blues", 
"Taste", 
"Tazza", 
"The Pit", 
"Trophy", 
"Tupelo Honey"
]

data = []

os.chdir('C:/Users/mabre/Google Drive/Analytics/ABC')

out = open( 'all_reviews.csv', 'w' , newline = '' )
writer = csv.writer( out )
writer.writerow( ['Yelp_Restaurant_Name','Yelp_Review_Count','Yelp_Price','Yelp_Rating',
                  'Google_Restaurant_Name', 'Google_Price', 'Google_Rating'])
#out.close()

for i in list:
    #Yelp API Call
    api_call = search(API_KEY, i,'raleigh, NC').get('businesses')[0]
    
    data.append(api_call['name'])
    data.append(api_call['review_count'])
    data.append(api_call['price'])
    data.append(api_call['rating'])
    
    #Google API Call
    api_call = google_places.nearby_search(
        location='Raleigh, NC', name=i,
        radius=25000, types=[types.TYPE_FOOD])
    
    api_call.places[0].get_details()
    
    data.append(api_call.places[0].name)
    try:
        data.append(api_call.places[0].details['price_level'])
    except:
        data.append('NA')
    data.append(float(api_call.places[0].rating))
    
    print(api_call.places[0].name)
    
    writer.writerow(data)
    data = []
    #time.sleep(8)
    
out.close()
