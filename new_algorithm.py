import random
import json
import math


def crossover(ind1, ind2):
    midpoint = random.choice(range(len(ind2)))
    return ind1[midpoint:] + ind2[:midpoint]

def cxPartiallyMatched(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1


def euclideanCost(individual, instance, depots):
    totalCost = 0
    routeCost = 0
    distance = 0
    for routes in individual:
        depot = routes[0]
        lastCustomer = depot
        for index in range(1, len(routes) - 1):
            distance = instance["distance_matrix"][lastCustomer - 1][routes[index] - 1]
            routeCost += distance
            lastCustomer = routes[index]
        totalCost += routeCost
        routeCost = 0
    return totalCost


def calculateFitness(individual, instance, depots, fitnessObjective):
    routeCost = euclideanCost(individual, instance, depots)
    return fitnessObjective / routeCost



def ind2route(individual, instance, clusters, depots):
    customersDepot = {}
    routes = []
    subRoute = []
    elapsedTime = 0 
    vehicleLoad = 0

    for depot in depots:
        customersDepot[depot] = []

    for depot in depots:
        for customerID in individual:
            if customerID in clusters[depot]:
                customersDepot[depot].append(customerID)

    for depot, customers in customersDepot.items():
        subRoute.append(depot)
        initialDepot = instance["depot_%i" % depot]
        lastCustomer = depot
        maximumTime = initialDepot["max_route_duration"]
        maximumCapacity = initialDepot["max_vehicle_load"]
        for customer in customers:
            actualCustomer = instance["customer_%i" % customer]
            distance = instance["distance_matrix"][lastCustomer - 1][customer - 1]
            waitTime = max(actualCustomer["ready_time"] - ( elapsedTime + distance), 0)
            vehicleLoad += actualCustomer["demand"]
            returnTime = instance["distance_matrix"][depot - 1][customer - 1]
            updatedElapsedTime = elapsedTime + distance + returnTime + waitTime
            #check if elapsed time and vehicle load is less than a fixed amount
            if (updatedElapsedTime <= maximumTime and vehicleLoad <= maximumCapacity):
                subRoute.append(customer)
                lastCustomer = customer
                elapsedTime = updatedElapsedTime - returnTime
            else:
                subRoute.append(depot)
                routes.append(subRoute)
                updatedElapsedTime = 0
                elapsedTime = 0
                vehicleLoad = 0
                subRoute = []
                subRoute.append(depot)
                subRoute.append(customer)
        
        subRoute.append(depot)
        routes.append(subRoute)
        subRoute = []
        updatedElapsedTime = 0
        elapsedTime = 0
        vehicleLoad = 0

    return routes
    

def euclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt( pow(x2 - x1, 2) + pow(y2 - y1, 2)), 3)

class DNA:
    def __init__(self, depot, route, vehicle_number):
        self.depot = depot
        self.route = route
        self.vehicle_number = vehicle_number


class Solution:

    def __init__(self, n_customers, depots, n_vehicles, instance, clusters):
        self.routes = []
        self.instance = instance
        self.random_route = [i for i in range(1, n_customers + 1)]
        self.fitness = 0
        self.nCustomers = n_customers
        self.depots = depots
        self.nVehicles = n_vehicles
        self.clusters = clusters

        random.shuffle(self.random_route)
        customersDepot = {}
        elapsedTime = 0
        vehicleLoad = 0
        updatedElapsedTime = 0
        maximumCapacity = 200
        maximumTime = 500
        subRoute = []
        vehicleNumber = 1

        for depot in depots:
            customersDepot[depot] = []

        for depot in depots:
            for customerID in self.random_route:
                if customerID in clusters[depot]:
                    customersDepot[depot].append(customerID)
        
        for depot, customers in customersDepot.items():
            initialDepot = self.instance["depot_%i" % depot]
            lastCustomer = self.instance["depot_%i" % depot]
            for customer in customers:
                actualCustomer = self.instance["customer_%i" % customer]
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
                    subRoute.append(customer)
                    lastCustomer = actualCustomer
                    elapsedTime = updatedElapsedTime - returnTime
                else:
                    self.routes.append(DNA(depot, subRoute, vehicleNumber))
                    vehicleNumber += 1
                    updatedElapsedTime = 0
                    elapsedTime = 0
                    vehicleLoad = 0
                    subRoute = []
                    subRoute.append(customer)
            self.routes.append(DNA(depot, subRoute, vehicleNumber))
            vehicleNumber = 1
            updatedElapsedTime = 0
            elapsedTime = 0
            vehicleLoad = 0
            subRoute = []
        
        # print(customersDepot)

        # for depot in depots:
        #     for vehicle_number in range(1, n_vehicles + 1):
        #         route = self.generateARoute(depot, self.random_route, clusters)
        #         self.cleanRandomRoute(route, self.random_route)
        #         self.routes.append(DNA(depot, route, vehicle_number))

    def cleanRandomRoute(self, route, random_route):
        for customer in route:
            random_route.remove(customer)

    def calculateFitness(self):
        totalCost = 0
        routeCost = 0
        for dna in self.routes:
            depot = dna.depot
            lastCustomer = self.instance["depot_%i" % depot]
            for customer in dna.route:
                actualCustomer = self.instance["customer_%i" % customer]
                x1 = lastCustomer["coordinates"]["x"]
                y1 = lastCustomer["coordinates"]["y"]
                x2 = actualCustomer["coordinates"]["y"]
                y2 = actualCustomer["coordinates"]["y"]
                distance = euclideanDistance(x1, y1, x2, y2)
                routeCost += distance
                lastCustomer = actualCustomer
            lastCustomer = self.instance["depot_%i" % depot]
            returnTime = euclideanDistance(x2, y2,lastCustomer["coordinates"]["x"], lastCustomer["coordinates"]["y"])
            routeCost += returnTime
            totalCost += routeCost
            routeCost = 0
        self.fitness = 1083.98 / round(totalCost, 3)
    
    #   def __init__(self, n_customers, depots, n_vehicles, instance, clusters):
    #     self.routes = []
    #     self.instance = instance
    #     self.random_route = [i for i in range(1, n_customers + 1)]
    #     self.fitness = 0
    def crossover(self, partner):
        nCustomers = self.nCustomers
        depots = self.depots
        nVehicles = self.nVehicles
        instance = self.instance
        clusters = self.clusters
        child = Solution(nCustomers, depots, nVehicles, instance, clusters)
        new_genes = []
        #si el otro individuo tiene más rutas
        if (len(partner.routes) > len(self.routes)):
            midpoint = int(random.choice(range(len(partner.routes) - 1)))
            lenNewGenes = len(self.routes)
        elif (len(self.routes) > len(partner.routes)):
            midpoint = int(random.choice(range(len(self.routes) - 1)))
            lenNewGenes = len(partner.routes)
        else:
            midpoint = int(random.choice(range(len(self.routes) - 1)))
            lenNewGenes = len(self.routes)
        #el problema es que a veces se elige un punto medio mayor que el largo
        #de la cantidad de rutas
        for i in range(lenNewGenes):
            if i > midpoint:
                new_genes.append(self.routes[i])
            else:
                new_genes.append(partner.routes[i])
        child.routes = new_genes
        return child


    def generateARoute(self, depotID, random_route, clusters):
        new_route = []
        initialDepot = self.instance["depot_%i" % depotID]
        lastCustomer = self.instance["depot_%i" % depotID]
        elapsedTime = 0
        vehicleLoad = 0
        updatedElapsedTime = 0
        maximumCapacity = 200
        maximumTime = 500
        
        for i in range(len(random_route)):

            #si esta dentro del cluster
            if (random_route[i] in clusters[depotID]):
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
        return new_route
    
    def mutate(self, mutationRate):
        mutatedRoute = []
        pivot = 0
        for i in range(len(self.routes)):
            randomNumber = round(random.randint(1, 100) / 100, 2)
            if (randomNumber < mutationRate and len(self.routes[i].route) > 1):
                route = self.routes[i].route
                customersToChange = random.sample(range(0, len(route)), 2)
                #intercambiar el primero con el segundo
                pivot = route[customersToChange[1]]
                route[customersToChange[1]] = route[customersToChange[0]]
                route[customersToChange[0]] = pivot
                self.routes[i].route = route

        # for i in range(len(random_route)):
        #     actualCustomer = self.instance["customer_%i" % random_route[i]]
        #     x1 = lastCustomer["coordinates"]["x"]
        #     y1 = lastCustomer["coordinates"]["y"]
        #     x2 = actualCustomer["coordinates"]["y"]
        #     y2 = actualCustomer["coordinates"]["y"]
        #     distance = euclideanDistance(x1, y1, x2, y2)
        #     vehicleLoad += int(actualCustomer["demand"])
        #     returnTime = euclideanDistance(x2, y2, initialDepot["coordinates"]["x"], initialDepot["coordinates"]["y"])
        #     updatedElapsedTime = elapsedTime + distance + returnTime
        #     #check if elapsed time and vehicle load is less than a fixed amount
        #     if (updatedElapsedTime <= maximumTime and vehicleLoad <= maximumCapacity):
        #         new_route.append(random_route[i])
        #         lastCustomer = actualCustomer
        #         elapsedTime = updatedElapsedTime - returnTime
        #     else:
        #         break
        # return new_route

def reproduction(population, pool, mutation_rate):
    offspring = []
    for i in range(len(population)):
        parentA = random.choice(pool)
        parentB = random.choice(pool)
        child = parentA.crossover(parentB)
        # child.mutate(mutation_rate)
        # child.fitness
        offspring.append(child)
    return offspring

def bestInd(population):
    maxFitness = 0
    bestInd = 0
    for i in range(len(population)):
        if population[i].fitness > maxFitness:
            maxFitness = population[i].fitness
            bestInd = population[i]
    return bestInd

def mating_pool(population):
    pool = []
    for i in range(len(population)):
        n = int(population[i].fitness * 100)
        for j in range(n):
            pool.append(population[i])
    return pool


def clustering(depots, customers, instance):
    minDistance = 1000
    selectedDepot = 0
    clusters = {}
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
            if distance <= minDistance and len(clusters[depot]) < 13:
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

depots = [49, 50, 51, 52]
    
customers = [i for i in range(1, 49)]
clusters = clustering([49, 50, 51, 52], customers, instance)
print(clusters)
random_route = [i for i in range(1, 49)]
random.shuffle(random_route)
print(random_route)
myRoute = ind2route(random_route, instance, clusters, [49, 50, 51, 52])
print (myRoute)
# routeCost = euclideanCost(myRoute, instance, depots)
fitness = calculateFitness(myRoute, instance, depots, 1083.98)
print(fitness)
# print (euclideanCost(myRoute, instance, depots))
# solution1 = Solution(48, [49, 50, 51, 52], 2, instance, clusters)
# print(solution1.fitness())
# for dna in solution1.routes:
#     print(dna.depot, dna.route, dna.vehicle_number)

population = []
nGen = 1
nPop = 125
mutationRate = 0.02

#initialize population
# for i in range(nPop):
#     population.append(Solution(48, [49, 50, 51, 52], 2, instance, clusters))

# for solution in population:
#     for route in solution.routes:
#         print(route.depot, route.route, len(route.route))

while nGen < 100:
    for i in range(len(population)):
        population[i].calculateFitness()
    
    #build a mating pool
    pool = mating_pool(population)
    population = reproduction(population, pool, mutationRate)
    nGen += 1

# for individual in population:
#     individual.calculateFitness()
#     print(individual.fitness)

# bestInd = bestInd(population)
# print(bestInd.fitness)
# for dna in bestInd.routes:
#     print(dna.depot, dna.route, dna.vehicle_number, len(dna.route))


'''
final_route = [9, 42, 46, 39, 15, 25, 26, 23, 36, 32]
routeCost = calculate_euclidean_cost(final_route, 49, instance)
cost += routeCost

final_route = [35, 44, 31, 41, 7, 37]
cost += calculate_euclidean_cost(final_route, 49, instance)
print(cost)
#50
final_route = [34, 10, 45, 6, 27, 3, 48, 11]
cost += calculate_euclidean_cost(final_route, 50, instance)
final_route = [22]
cost += calculate_euclidean_cost(final_route, 50, instance)
#51
final_route = [28, 4, 19, 14, 1, 16, ]
cost += calculate_euclidean_cost(final_route, 51, instance)
final_route = [13, 33, 20, 29, 8, 5, 17, 18]
cost += calculate_euclidean_cost(final_route, 51, instance)
#52
final_route = [30]
cost += calculate_euclidean_cost(final_route, 52, instance)
final_route = [2, 47, 24, 12, 38, 40, 21, 43]
cost += calculate_euclidean_cost(final_route, 52, instance)

print(cost)
print(euclideanDistance(4.163, 13.559, -4.175, -1.569))
'''