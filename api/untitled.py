import json
from urllib2 import urlopen

def get_details(place_id):
    places_api_key = 'AIzaSyCtQScpB0zS0M4cUfp_Q9g2OrUZaXn8soY'
    details_req = 'https://maps.googleapis.com/maps/api/place/details/json?key=%s&placeid=%s' % (places_api_key, place_id)
    jsonurl = urlopen(details_req)
    data = json.loads(jsonurl.read())['result']
    price = int(data['price_level'])
    if True or price <= 2:
        persist_google_entity(place_id, data)

def persist_google_entity(place_id, data):
    name = data['name']
    address = data['vicinity']
    latLong = data['geometry']['location']#.getCenter()
    # latitude = latLong.lat()
    # longitude = latLong.lng()
    rating = data['rating']
    price = data['price_level']

    # r = GPlace(place_id = place_id, name = name, address = address, latitude = latitude, longitude = longitude,
    #             average_rating = rating, hours = '', price = price)
    # r.save()
    print place_id
    print name
    print address
    print latLong['lat']
    print rating
    print price


def main():
    get_details('ChIJo_FP-D26j4ARMNWiRFrcZsE')

if __name__ == '__main__':
    main()