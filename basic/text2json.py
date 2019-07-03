# -*- coding: utf-8 -*-
import random
import os
import json
from basic.common import *

def euclideanDistance(customer1, customer2):
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5


def distance_matrix(depots, customers, jsonData):
    jsonResponse = {}
    distanceMatrix = []
    subDistance = []
    for depot in depots:
        customerswDepot = [depot] + customers
        for customer1 in customerswDepot:
            for customer2 in customerswDepot:
                distance = euclideanDistance(jsonData[customer2], jsonData[customer1])
                subDistance.append(distance)
            distanceMatrix.append(subDistance)
            subDistance = []
        jsonResponse['%s'%depot] = distanceMatrix
        distanceMatrix = []
        customerswDepot = []
    return jsonResponse

def text2json(instance, filePath):
    def __distance(customer1, customer2):
        return ((customer1['coordinates']['x'] - customer2['coordinates']['x'])**2 + (customer1['coordinates']['y'] - customer2['coordinates']['y'])**2)**0.5
    
    textFile = os.path.join(filePath, instance)
    jsonData = {}
    depots = 0
    vehicles = 0
    customers = 0
    depotsCounter = 1
    with open(textFile) as f:
        for lineCount, line in enumerate(f, start=1):
            if lineCount == 1:
                values = line.strip().split()
                vehicles = int(values[1])
                customers = int(values[2])
                nDepots = int(values[3])
                jsonData["vehicles_number"] = vehicles
                jsonData["depots"] = nDepots
                jsonData["customers"] = customers
            elif lineCount in range(2, (nDepots+2)):
                values = line.strip().split()
                jsonData["depot_%s" % str(customers+depotsCounter)] = {
                    "max_duration" : values[0],
                    "capacity" : values[1]
                }
                depotsCounter += 1
            elif lineCount in range( (nDepots+2), (customers+nDepots+2)):
                values = line.strip().split()
                jsonData["customer_%s" %values[0]]={
                    "coordinates":{
                        "x": float(values[1]),
                        "y": float(values[2])
                    },
                    "service_duration": values[3],
                    "demand" : values[4],
                    "earliest_time" : values[11],
                    "latest_time": values[12]
                }
            else:
                values = line.strip().split()
                jsonData["depot_%s" %values[0]].update({
                     "coordinates":{
                        "x": float(values[1]),
                        "y": float(values[2])
                    },
                    "latest_time": values[8]
                })
        depots = ['depot_%d' % x for x in range(customers+1, customers+nDepots+1)]
        customers = ['customer_%d' % x for x in range(1, customers+1)]
        asdf= distance_matrix(depots, customers, jsonData)
        jsonData['distance_matrix'] = asdf
        """ jsonData['distance_matrix'] = [[__distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers] """

        jsonFilename = '%s.json' % instance.split(".")[0]
        jsonFile = os.path.join(filePath, jsonFilename)
        print ('Write to file: %s' % jsonFile)
        makeDirsForFile(jsonFile)
        with open(jsonFile, 'w') as f:
            json.dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': '))