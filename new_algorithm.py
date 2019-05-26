import random
import json
import math

def euclideanDistance(x1, y1, x2, y2):
    return math.sqrt( pow(x2 - x1, 2) + pow(y2 - y1, 2))

class DNA:
    def __init__(self, depot, route, vehicle_number):
        self.depot = depot
        self.route = route
        self.vehicle_number = vehicle_number



class Solution:

    def __init__(self, n_customers, depots, n_vehicles, instance):
        self.routes = []
        self.instance = instance
        self.random_route = [i for i in range(1, n_customers + 1)]
        random.shuffle(self.random_route)
        
        for depot in depots:
            for vehicle_number in range(1, n_vehicles + 1):
                route = self.generateARoute(depot, self.random_route)
                self.cleanRandomRoute(route, self.random_route)
                self.routes.append(DNA(depot, route, vehicle_number))

    def cleanRandomRoute(self, route, random_route):
        for customer in route:
            random_route.remove(customer)

    def generateARoute(self, depotID, random_route):
        new_route = []
        initialDepot = self.instance["depot_%i" % depotID]
        lastCustomer = self.instance["depot_%i" % depotID]
        elapsedTime = 0
        vehicleLoad = 0
        updatedElapsedTime = 0
        maximumCapacity = 200
        maximumTime = 500
        for i in range(len(random_route)):
            actualCustomer = self.instance["customer_%i" % random_route[i]]
            x1 = lastCustomer["coordinates"]["x"]
            y1 = lastCustomer["coordinates"]["y"]
            x2 = actualCustomer["coordinates"]["y"]
            y2 = actualCustomer["coordinates"]["y"]
            distance = euclideanDistance(x1, y1, x2, y2)
            vehicleLoad += int(actualCustomer["demand"])
            returnTime = euclideanDistance(x2, y2, initialDepot["coordinates"]["x"], initialDepot["coordinates"]["y"])
            updatedElapsedTime = elapsedTime + distance + returnTime
            #check if elapsed time and vehicle load is less than a fixed amount
            if (updatedElapsedTime <= maximumTime and vehicleLoad <= maximumCapacity):
                new_route.append(random_route[i])
                lastCustomer = actualCustomer
                elapsedTime = updatedElapsedTime - returnTime
            else:
                break
        return new_route



def clustering(depots, customers, instance):
    minDistance = 1000
    selectedDepot = 0
    clusters = {}
    random.shuffle(customers)
    for depot in depots:
        clusters[depot] = []

    for customer in customers:
        customerInstance = instance["customer_%i" % customer]
        for depot in depots:
            depotInstance = instance["depot_%i" % depot]
            x1 = depotInstance["coordinates"]["x"]
            y1 = depotInstance["coordinates"]["y"]
            x2 = customerInstance["coordinates"]["y"]
            y2 = customerInstance["coordinates"]["y"]
            distance = euclideanDistance(x1, y1, x2, y2)            
            if distance < minDistance and len(clusters[depot]) < 13:
                # and len(clusters[depot]) < 13 
                selectedDepot = depot
                minDistance = distance
        clusters[selectedDepot].append(customer)
        minDistance = 1000
        selectedDepot = 0
    return clusters



instance = ''
with open('data/c-mdvrptw/pr01.txt.json') as json_file:  
    instance = json.load(json_file)
    
clusters = clustering([49, 50, 51, 52], customers, instance)
solution1 = Solution(48, [49, 50, 51, 52], 2, instance)

customers = [i for i in range(1, 49)]
print(solution1.random_route)
for dna in solution1.routes:
    print(dna.route, dna.depot, dna.vehicle_number)