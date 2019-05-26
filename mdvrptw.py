# -*- coding: utf-8 -*-
import random

from deap import base
from deap import creator
from deap import tools


def ind2route2(individual, instance):
    route = []
    for customer in individual:
        
    return 1

def evaluate2(individual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0):
    route = ind2route2(individual, instance)
    return 0

#Provides a decoded individual
def ind2route(individual, instance):
    route = []
    vehicleCapacity = instance['vehicle_capacity']
    capacityavg = int(sum(vehicleCapacity)/len(vehicleCapacity))
    deportDueTime = instance['deport']['due_time']
    subRoute = []
    vehicleLoad = 0
    elapsedTime = 0
    lastCustomerID = 0
    capacityct = 0
    for customerID in individual:
        if capacityct > len(vehicleCapacity)-1:
            capacityvehicle = capacityavg
        else:
            capacityvehicle = vehicleCapacity[capacityct]
        demand = instance['customer_%s' % customerID]['demand']
        updatedVehicleLoad = vehicleLoad + demand
        serviceTime = instance['customer_%s' % customerID]['service_time']
        returnTime = instance['time_matrix'][customerID][0]
        updatedElapsedTime = elapsedTime + instance['time_matrix'][lastCustomerID][customerID] + serviceTime + returnTime
        if (updatedVehicleLoad <= capacityvehicle) and (updatedElapsedTime <= deportDueTime):
            subRoute.append(customerID)
            vehicleLoad = updatedVehicleLoad
            elapsedTime = updatedElapsedTime - returnTime
        else:
            route.append(subRoute)
            subRoute = [customerID]
            vehicleLoad = demand
            elapsedTime = instance['time_matrix'][0][customerID] + serviceTime
            capacityct+=1
        lastCustomerID = customerID
    if subRoute != []:
        route.append(subRoute)
    return route

def printRoute(route, instance ,merge=False):
    routeStr = '0'
    subRouteCount = 0
    serviceTime = 0
    myRoute = []
    updatedElapsedTime = 0
    for subRoute in route:
        subRouteCount += 1
        subRouteStr = '0'
        elapsedTime = 0
        lastCustomerID = 0
        returnTime = 0
        for customerID in subRoute:
            subRouteStr = subRouteStr + ' - ' + str(customerID)
            routeStr = routeStr + ' - ' + str(customerID)
            serviceTime = instance['customer_%d' % customerID]['service_time']
            returnTime = instance['time_matrix'][customerID][0]
            updatedElapsedTime = elapsedTime + instance['time_matrix'][lastCustomerID][customerID] + serviceTime
            elapsedTime = updatedElapsedTime
            lastCustomerID = customerID
        returnTime = instance['time_matrix'][lastCustomerID][0]
        elapsedTime = elapsedTime + returnTime
        subRouteStr = subRouteStr + ' - 0'
        if not merge:
            print '  Vehicle %d\'s route: %s' % (subRouteCount, subRouteStr)
            print '  Route time: %s seconds' % (elapsedTime)
        routeStr = routeStr + ' - 0'
        myRoute.append(subRouteStr)
    if merge:
        print routeStr
    return myRoute

#Outputs the fitness for an ind
def evalVRPTW(individual, instance, unitCost=1.0, initCost=0, waitCost=0, delayCost=0):
    route = ind2route(individual, instance)
    totalCost = 0
    for subRoute in route:
        subRouteTimeCost = 0
        subRouteDistance = 0
        elapsedTime = 0
        lastCustomerID = 0
        for customerID in subRoute:
            distance = instance['time_matrix'][lastCustomerID][customerID]
            subRouteDistance = subRouteDistance + distance
            arrivalTime = elapsedTime + distance
            timeCost = waitCost * max(instance['customer_%d' % customerID]['ready_time'] - arrivalTime, 0) + delayCost * max(arrivalTime - instance['customer_%d' % customerID]['due_time'], 0)
            subRouteTimeCost = subRouteTimeCost + timeCost
            elapsedTime = arrivalTime + instance['customer_%d' % customerID]['service_time']
            lastCustomerID = customerID
        subRouteDistance = subRouteDistance + instance['time_matrix'][lastCustomerID][0]
        subRouteTranCost = initCost + (unitCost * subRouteDistance)
        subRouteCost = subRouteTimeCost + subRouteTranCost
        totalCost = totalCost + subRouteCost
    fitness = 1.0 / totalCost
    return fitness,


def cxPartialyMatched(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    temp1 = ind1[cxpoint1:cxpoint2+1] + ind2
    temp2 = ind1[cxpoint1:cxpoint2+1] + ind1
    ind1 = []
    for x in temp1:
        if x not in ind1:
            ind1.append(x)
    ind2 = []
    for x in temp2:
        if x not in ind2:
            ind2.append(x)
    return ind1, ind2

#Mutation operator
def mutInverseIndexes(individual):
    start, stop = sorted(random.sample(range(len(individual)), 2))
    individual = individual[:start] + individual[stop:start-1:-1] + individual[stop+1:]
    return individual,


def planner(instName, nCustomers, nDepots, nVehicles,unitCost, initCost, waitCost, delayCost, indSize, popSize, cxPb, mutPb, NGen,
exportCSV=False, customizeData=False):
    #Creation of Classes
    creator.create('FitnessMax', base.Fitness, weights=(1.0,))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    creator.create('Cluster', dict)

    toolbox = base.Toolbox()

    toolbox.register('indexes', random.sample, range(1, indSize + 1), indSize)
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('clusterindexes', range(nCustomers, nCustomers+nDepots+1))
    toolbox.register('initcluster', )
    toolbox.register('evaluate', evalVRPTW, instance=instance, unitCost=unitCost, initCost=initCost, waitCost=waitCost, delayCost=delayCost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cxPartialyMatched)
    toolbox.register('mutate', mutInverseIndexes)

    pop = toolbox.population(n=popSize)
    csvData = []

    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print '  Evaluated %d individuals' % len(pop)
    
    for g in range(NGen):
        print '-- Generation %d --' % g

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxPb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values


        for mutant in offspring:
            if random.random() < mutPb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalidInd = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalidInd)
        for ind, fit in zip(invalidInd, fitnesses):
            ind.fitness.values = fit

        print '  Evaluated %d individuals' % len(invalidInd)

        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print '  Min %s' % min(fits)
        print '  Max %s' % max(fits)
        print '  Avg %s' % mean
        print '  Std %s' % std

        if exportCSV:
            csvRow = {
                'generation': g,
                'evaluated_individuals': len(invalidInd),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
            }
            csvData.append(csvRow)

    print '-- End of (successful) evolution --'

    bestInd = tools.selBest(pop, 1)[0]
    print 'Best individual: %s' % bestInd
    print 'Fitness: %s' % bestInd.fitness.values[0]
    print 'Total cost: %s' % (1 / bestInd.fitness.values[0])
