import random, os, json, math
from basic.common import *

def euclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt( pow(x2 - x1, 2) + pow(y2 - y1, 2)), 3)

def nodeToCoordinates(node, depotsID, jsonData):
    x = 0.0
    y = 0.0
    if node in depotsID:
        x = jsonData["depot_%i" % node]["coordinates"]["x"]
        y = jsonData["depot_%i" % node]["coordinates"]["y"]
    else:
        x = jsonData["customer_%i" % node]["coordinates"]["x"]
        y = jsonData["customer_%i" % node]["coordinates"]["y"]
    return x, y
    

def distanceMatrix(depotsID, customersID, jsonData):
    distance_matrix = []
    subDistance = []
    allNodes = customersID + depotsID
    for node1 in allNodes:
        x1, y1 = nodeToCoordinates(node1, depotsID, jsonData)
        for node2 in allNodes:
            x2, y2 = nodeToCoordinates(node2, depotsID, jsonData)
            subDistance.append(euclideanDistance(x1, y1, x2, y2))
        distance_matrix.append(subDistance)
        subDistance = []
    return distance_matrix
        

def text2json(instance, filePath):    
    textFile = os.path.join(filePath, instance)
    jsonData = {}
    numberOfDepots = 0
    numberOfVehicles = 0
    numberOfCustomers = 0
    depotsCounter = 1
    with open(textFile) as f:
        for lineCount, line in enumerate(f, start=1):
            if lineCount == 1:
                values = line.strip().split()
                numberOfVehicles = int(values[1])
                numberOfCustomers = int(values[2])
                numberOfDepots = int(values[3])
                jsonData["number_of_vehicles"] = numberOfVehicles
                jsonData["number_of_customers"] = numberOfCustomers
                jsonData["number_of_depots"] = numberOfDepots
            # desde la linea 2 hasta la cantidad de depositos
            elif lineCount in range(2, (numberOfDepots + 2)):
                values = line.strip().split()
                jsonData["depot_%s" % str(numberOfCustomers + depotsCounter)] = {
                    "max_route_duration" : int(values[0]),
                    "max_vehicle_load" : int(values[1])
                }
                depotsCounter += 1
            elif lineCount in range( ( numberOfDepots + 2), (numberOfCustomers + numberOfDepots + 2)):
                values = line.strip().split()
                jsonData["customer_%s" %values[0]]={
                    "coordinates":{
                        "x": float(values[1]),
                        "y": float(values[2])
                    },
                    "service_duration": int(values[3]),
                    "demand" : int(values[4]),
                    "ready_time" : int(values[11]),
                    "due_time": int(values[12])
                }
            else:
                values = line.strip().split()
                jsonData["depot_%s" %values[0]].update({
                     "coordinates":{
                        "x": float(values[1]),
                        "y": float(values[2])
                    },
                    "latest_time": int(values[8])
                })
        depots = ['depot_%d' % x for x in range(numberOfCustomers + 1, numberOfCustomers + numberOfDepots + 1)]
        customers = ['customer_%d' % x for x in range(1, numberOfCustomers + 1)]
        depotsID =  [x for x in range(numberOfCustomers + 1, numberOfCustomers + numberOfDepots + 1)]
        customersID = [ x for x in range(1, numberOfCustomers + 1)]
        distance_matrix = distanceMatrix(depotsID, customersID, jsonData)
        jsonData['distance_matrix'] = distance_matrix

        jsonFilename = '%s.json' % instance
        jsonFile = os.path.join(filePath, jsonFilename)
        print ('Write to file: %s' % jsonFile)
        makeDirsForFile(jsonFile)
        with open(jsonFile, 'w') as f:
            json.dump(jsonData, f, sort_keys=True, indent=4, separators=(',', ': '))



        # jsonData['distance_matrix'] = [[__distance(jsonData[customer1], jsonData[customer2]) for customer1 in customers] for customer2 in customers]