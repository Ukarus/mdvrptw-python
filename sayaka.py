# -*- coding: utf-8 -*-
import random
import googlemaps

gmaps = googlemaps.Client(key="AIzaSyD3JcxO0IZ_ek8XSI5fdc0Q7Tuz1ybLbko")

def distance(customer1, customer2):
    #return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5
    c1 = str(customer1['coordinates']['x']) + "," + str(customer1['coordinates']['y'])
    c2 = str(customer2['coordinates']['x']) + "," + str(customer2['coordinates']['y'])
    routes = gmaps.distance_matrix(c1, c2)
    return routes["rows"][0]["elements"][0]["duration"]["value"]

def euclideanDistance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5

jsonData = {
    "customer_50":{
        "coordinates":{
            "x":21.387,
            "y":17.105
        }
    },
    "customer_22":{
        "coordinates":{
            "x":23.767,
            "y":29.083
        }
    }
}
""" print distance(jsonData["customer_50"],jsonData["customer_22"])
 """

print euclideanDistance(jsonData["customer_22"],jsonData["customer_50"])
