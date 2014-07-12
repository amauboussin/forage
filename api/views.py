<<<<<<< HEAD
# Create your views here.
from models import Restaurant
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from urllib2 import urlopen
from constants import *
import json


# class Restaurant(models.Model):
#     name = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)
#     address = models.CharField(max_length=200)
#     genre = models.CharField(max_length=100)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     average_rating = models.FloatField(default=0)
#     num_ratings = models.IntegerField(default=0)
#     hours = models.CharField(default="12-10", max_length= 30)
cats = ['afghani', 'african', 'senegalese', 'southafrican', 'newamerican', 'tradamerican', 'arabian', 'argentine', 'armenian', 'asianfusion', 'australian', 'austrian', 'bangladeshi', 'bbq', 'basque', 'belgian', 'brasseries', 'brazilian', 'breakfast_brunch', 'british', 'buffets', 'burgers', 'burmese', 'cafes', 'cafeteria', 'cajun', 'cambodian', 'caribbean', 'dominican', 'haitian', 'puertorican', 'trinidadian', 'catalan', 'cheesesteaks', 'chicken_wings', 'chinese', 'cantonese', 'dimsum', 'shanghainese', 'szechuan', 'comfortfood', 'creperies', 'cuban', 'czech', 'delis', 'diners', 'ethiopian', 'hotdogs', 'filipino', 'fishnchips', 'fondue', 'food_court', 'foodstands', 'french', 'gastropubs', 'german', 'gluten_free', 'greek', 'halal', 'hawaiian', 'himalayan', 'hotdog', 'hotpot', 'hungarian', 'iberian', 'indpak', 'indonesian', 'irish', 'italian', 'japanese', 'ramen', 'korean', 'kosher', 'laotian', 'latin', 'colombian', 'salvadoran', 'venezuelan', 'raw_food', 'malaysian', 'mediterranean', 'falafel', 'mexican', 'mideastern', 'egyptian', 'lebanese', 'modern_european', 'mongolian', 'moroccan', 'pakistani', 'persian', 'peruvian', 'pizza', 'polish', 'portuguese', 'russian', 'salad', 'sandwiches', 'scandinavian', 'scottish', 'seafood', 'singaporean', 'slovakian', 'soulfood', 'soup', 'southern', 'spanish', 'steak', 'sushi', 'taiwanese', 'tapas', 'tapasmallplates', 'tex-mex', 'thai', 'turkish', 'ukrainian', 'uzbek', 'vegan', 'vegetarian', 'vietnamese']

def get_loc(address):
    address = address.replace(' ', '+')
    print address
    try:
        loc_req = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s' % (address)
        jsonurl = urlopen(loc_req)
        data = json.loads(jsonurl.read())
        loc = data['results'][0]['geometry']['location']
        print loc
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


def scrape(request):
    lat = 37.423418
    long = -122.071638
    ywsid = 'nc5nvTckUyLncvvm9Qd8ew'
    yelp_req = 'http://api.yelp.com/business_review_search?term=food&lat=%s&long=%s&radius=10&limit=20&ywsid=%s' % (lat, long, ywsid)
    jsonurl = urlopen(yelp_req)
    data = json.loads(jsonurl.read())

    food_cats = get_food_cats()

    print data

    for b in data['businesses']:
        name = b['name']

        address = ','.join(filter(lambda x : len(x) > 0 , [b['address1'], b['address2'], b['address3'], b['city']]))
        if len(b['address1']) == 0 : continue

        genre = get_genre(b, food_cats)
        if genre is None: continue

        lat, long = get_loc(address)
        average_rating = b['avg_rating']
        num_ratings = b['review_count']
        r = Restaurant(name= name, address= address, average_rating = average_rating,
                   num_ratings = num_ratings,genre = genre, hours = '', latitude = lat, longitude = long)
        print name, genre
        r.save()
    text = 'scraped'

    return render_to_response('test.html', {'message' : text}, context_instance=RequestContext(request))

