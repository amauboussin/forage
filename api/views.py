# Create your views here.

from django.shortcuts import render_to_response
from django.template.context import RequestContext

def test(request):
    return render_to_response('test.html', {}, context_instance=RequestContext(request))

# returns the ten closest restaurants to (latitude, longitude)
def get_restaurants(restaurants, latitude, longitude):
    restaurants = Restaurant.objects.all()

    def calculate_distance(restaurant):
        rst_lat = restaurant.latitude
        rst_long = restaurant.longitude
        math.hypot(latitude - rst_lat, longitude - rst_long) # pythagorean theorem
        return [distance, restaurant]

    restaurantsWithDistance = map(calculate_distance, restaurants)
    restaurantsWithDistance = sorted(restaurantsWithDistance, key = lambda x : x[0])
    return restaurantsWithDistance[:10]