# Create your views here.
from django.http import HttpResponse
import math
from models import *
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from urllib2 import urlopen
from constants import *
import json


def scrape_grid_page(request):
    scrape_grid()

    return render_to_response('test.html', {'message' : 'finished scraping grid'}, context_instance=RequestContext(request))



def scrape_grid():
    ywsid = 'nc5nvTckUyLncvvm9Qd8ew'

    tl_lat = 37.433711
    tl_long = -122.110664
    br_lat = tl_lat - 0.001
    br_long = tl_long - 0.001

    #37.357442
    while tl_lat >= 37.357442:
        req = 'http://api.yelp.com/business_review_search?term=food&tl_lat=%s&tl_long=%s&br_lat=%s&br_long=%s&limit=20&ywsid=%s' % (tl_lat, tl_long, br_lat, br_long, ywsid)
        scrape_yelp_data(req)
        tl_lat -= .001
        tl_long += .001
        br_lat = tl_lat - 0.001
        br_long = tl_long - 0.001

def get_loc(address):
    address = address.replace(' ', '+')
    print address
    try:
        loc_req = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s' % (address)
        jsonurl = urlopen(loc_req)
        data = json.loads(jsonurl.read())
        loc = data['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    except Exception, e:
        print str(e)
        return 0,0

def get_genre(b, food_cats):
    categories = b['categories']
    for c in categories:
        print c
        if c['category_filter'] in food_cats:
            return c['name']
    return None


def scrape_yelp_data(req):

    jsonurl = urlopen(req)
    data = json.loads(jsonurl.read())
    print data

    food_cats = get_food_cats()

    for b in data['businesses']:
        name = b['name']

        address = ','.join(filter(lambda x : len(x) > 0 , [b['address1'], b['address2'], b['address3'], b['city']]))

        #skip if no address or if the address already exists
        if len(b['address1']) == 0 : continue
        if Yelp.objects.filter(address= address).exists(): continue

        genre = get_genre(b, food_cats)
        if genre is None: continue

        lat, long = get_loc(address)
        average_rating = b['avg_rating']
        num_ratings = b['review_count']
        r = Yelp(name= name, address= address, average_rating = average_rating,
                   num_ratings = num_ratings,genre = genre, hours = '', latitude = lat, longitude = long)
        print name, genre
        r.save()

def scrape(request):
    lat = 37.423418
    long = -122.071638

    ywsid = 'nc5nvTckUyLncvvm9Qd8ew'
    yelp_req = 'http://api.yelp.com/business_review_search?term=food&lat=%s&long=%s&radius=10&limit=20&ywsid=%s' % (lat, long, ywsid)
    scrape_yelp_data(yelp_req)

    text = 'scraped'

    return render_to_response('test.html', {'message' : text}, context_instance=RequestContext(request))

def locate(request):
    # Turn the request into a lat and long
    # Fetch all restaurants from the database
    # Go through all of the restaurants and find the closest ones
    # Return those as JSON

    lat = float(request.GET['lat'])
    lng = float(request.GET['lon'])
    restaurants = get_restaurants(lat, lng)

    response_data = []

    for restaurant in restaurants:
        response_data.append({'name' : restaurant.name, 'genre' : restaurant.genre,
                      'latitude' : restaurant.latitude, 'longitude' : restaurant.longitude,
                      'address' : restaurant.address})

    return HttpResponse(json.dumps(response_data), content_type="application/json")

# returns the ten closest restaurants to (latitude, longitude)
def get_restaurants(latitude, longitude):
    restaurants = Yelp.objects.all()

    def calculate_distance(restaurant):
        rst_lat = restaurant.latitude
        rst_long = restaurant.longitude
        distance = math.hypot(latitude - rst_lat, longitude - rst_long) # pythagorean theorem
        return [distance, restaurant]

    restaurantsWithDistance = [calculate_distance(r) for r in restaurants]
    restaurantsWithDistance = sorted(restaurantsWithDistance, key = lambda x : x[0])
    return [r[1] for r in restaurantsWithDistance[:10]]