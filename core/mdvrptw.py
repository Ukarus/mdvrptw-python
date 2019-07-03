# Dependencies

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import json, random, math, os

def euclideanDistance(x1, y1, x2, y2):
    return round(math.sqrt( pow(x2 - x1, 2) + pow(y2 - y1, 2)), 3)

class Solution:

    def __init__(self, depots, instance, clusters):
        self.instance = instance
        self.route = [i for i in range(1, instance["number_of_customers"] + 1)]
        self.fitness = 0
        self.depots = depots
        self.nVehicles = instance["number_of_vehicles"]
        self.clusters = clusters
        random.shuffle(self.route) 
   

    # def crossover(self, ind1, ind2):
    #     midpoint = random.choice(range(len(ind2)))
    #     return ind1[midpoint:] + ind2[:midpoint]

    # def crossover(self, ind1, ind2):
    #     size = min(len(ind1), len(ind2))
    #     # print(len(ind1), len(ind2))
    #     cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    #     temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    #     temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    #     ind1 = []
    #     for gene in temp1:
    #         if gene not in ind1:
    #             ind1.append(gene)
    #     # return ind1
    #     ind2 = []
    #     for gene in temp2:
    #         if gene not in ind2:
    #             ind2.append(gene)
    #     print(len(ind1), len(ind2))
    #     return ind1, ind2

    def crossover(self, ind1, ind2):
        cxpoint1, cxpoint2 = sorted(random.sample(range(len(ind1)), 2))
        swath = ind1[cxpoint1:cxpoint2]

        child = [0 for i in range(len(ind1))]
        child[cxpoint1:cxpoint2] = swath
        #find values from parent 2 that are not in the swath
        candidates = []
        for i in range(cxpoint1, cxpoint2):
            if ind2[i] not in swath:
                candidates.append(ind2[i])

        for gene in candidates:
            indexInParent2 = ind2.index(gene)
            valueFromParent1 = ind1[indexInParent2]
            indexInParent2 = ind2.index(valueFromParent1)
            while child[indexInParent2] != 0:
                valueFromParent1 = ind1[indexInParent2]
                indexInParent2 = ind2.index(valueFromParent1)
            child[indexInParent2] = gene
        
        for i in range(len(child)):
            if child[i] == 0:
                child[i] = ind2[i]

        return child
        
    
    def mutate(self):

        start, stop = sorted(random.sample(range(len(individual)), 2))
        newIndividual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
        return newIndividual

    def ind2route(self, clusters):
        customersDepot = {}
        routes = []
        subRoute = []
        elapsedTime = 0 
        vehicleLoad = 0
        instance = self.instance
        individual = self.route
        depots = self.depots

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


    def euclideanCost(self, decodedIndividual):
        totalCost = 0
        routeCost = 0
        distance = 0
        individual = decodedIndividual
        instance = self.instance
        depots = self.depots
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


    def calculateFitness(self, clusters, fitnessObjective):
        routeCost = self.euclideanCost(self.ind2route(clusters))
        fitness = fitnessObjective / routeCost
        self.fitness = fitness



def reproduction(population, pool, mutation_rate, clusters):
    offspring = []
    for i in range(len(population)):
        parentA = random.choice(pool)
        parentB = random.choice(pool)
        child1 = Solution(parentA.depots, parentA.instance, clusters)
        child1.route = parentA.crossover(parentA.route, parentB.route)
        offspring.append(child1)
    return offspring

def bestIndividual(population):
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

def clustering(depots, csvInstance, jsonInstance):
    newClusters = {}
    for depot in depots:
        newClusters[depot] = []

    depotsCoordinates = [ [jsonInstance["depot_%i" % depot]["coordinates"]["x"], 
    jsonInstance["depot_%i" % depot]["coordinates"]["y"]] for depot in depots]
    x = np.array(csvInstance)
    clusters = np.array(depotsCoordinates)
    kmeans = KMeans(n_clusters=len(depots), init=clusters, n_init=1).fit(x)

    labels = kmeans.labels_
    for i in range(len(labels)):
        if i + 1 not in depots:
            newClusters[depots[labels[i]]].append(i + 1)

    return newClusters

def run_mdvrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size,
        pop_size, cx_pb, mut_pb, n_gen, export_csv):

    instance = ''
    fitnessObjective = 1763.07
    nPop = pop_size
    nGen = 1

    with open('data/c-mdvrptw/json/%s' % instance_name) as json_file:  
        instance = json.load(json_file)
    
    number_of_customers = instance["number_of_customers"]
    depots = [i for i in range(number_of_customers + 1, number_of_customers + instance["number_of_depots"] + 1)]
    customers = [i for i in range(1, number_of_customers + 1)]

    # pr01 = pd.read_csv(r'C:\Users\juanj\Documents\Trabajo de Titulo 2\algorithm\pr01_2.csv')
    
    csvPath = r'data/c-mdvrptw/csv/%s.csv' % instance_name.split(".")[0]
    pr01 = pd.read_csv(csvPath)
    depotsCoordinates = [ [instance["depot_%i" % depot]["coordinates"]["x"], 
    instance["depot_%i" % depot]["coordinates"]["y"]] for depot in depots]
    clusters = clustering(depots, pr01, instance)
    # clusters = {49: [7, 9, 31, 32, 35, 36, 37, 41, 42, 44, 46], 50: [3, 6, 10, 11, 22, 27, 34, 45, 48], 
    # 51: [1, 4, 5, 8, 13, 14, 16, 17, 18, 19, 20, 26, 28, 29, 33], 
    # 52: [2, 12, 15, 21, 23, 24, 25, 30, 38, 39, 40, 43, 47]}

    #population initialization
    population = []
    for i in range(nPop):
        population.append(Solution(depots, instance, clusters))
        population[i].calculateFitness(clusters, fitnessObjective)

    #Generational bucle
    while nGen < n_gen:
        print('-- Generation {} --'.format(nGen))
        pool = mating_pool(population)

        offspring = []
        offspring = reproduction(population, pool, mut_pb, clusters)

        for i in range(len(offspring)):
            offspring[i].calculateFitness(clusters, fitnessObjective)

        #replace old population with offspring
        population = offspring

        #stats
        fits = [ind.fitness for ind in population]
        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        print('  Min {}'.format(min(fits)))
        print('  Max {}'.format(max(fits)))
        print('  Avg {}'.format(mean))
        print('  Std {}'.format(std))
        nGen += 1
    
    print('-- End of evolution --')
    for i in range(len(population)):
        cost = population[i].euclideanCost(population[i].ind2route(clusters))


    bestInd = bestIndividual(population)
    print('\n')
    print("Best individual Cost: %s " % bestInd.euclideanCost(bestInd.ind2route(clusters)))
    print("Best individual Fitness: %s " % bestInd.fitness)
    print("Best individual Route: %s " % bestInd.route)

    json_file.close()
