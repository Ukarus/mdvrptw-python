# -*- coding: utf-8 -*-
import random
import pprint
import json

# from deap import base
# from deap import creator
# from deap import tools
from collections import defaultdict
from basic.common import *

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def initCluster(indSize, nDepots):
    clusters = {}
    customers = [i for i in range(1, indSize + 1)]
    print (customers)
    customersChunks = chunks(customers, nDepots)
    return customersChunks    

def sayaka(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def clustering (indSize, nDepots, instance):
    minDist = 1000
    clusters= defaultdict(list)
    customers = [i for i in range(1, indSize + 1)]
    for customer in customers:
        for depot in range(indSize + 1, indSize + nDepots + 1 ):
            distance = instance['distance_matrix']["depot_%i"%depot][0][customer]
            if distance < minDist:
                selectedDepot = depot
                minDist = distance
        clusters["%s"%str(selectedDepot)].append(customer)
        minDist = 1000
    return clusters


instName = 'pr01.txt'
rootpath = getrootpath()
jsonDataDir = os.path.join(rootpath,'data', 'c-mdvrptw')
jsonFile = os.path.join(jsonDataDir, '%s.json' % instName)
with open(jsonFile) as f:
    instance = json.load(f)

clusters = clustering(48, 4, instance)
print (clusters)

""" l = [i for i in range(1, 48 + 1)]
asdf = sayaka(l, 12)
print (asdf) """
""" a = initCluster(48, 4)
print (a) 

if selectedDepot in jsonData:
    jsonData["%s"%str(selectedDepot)] = [customer]
else:
    jsonData["%s"%str(selectedDepot)]= [customer]
"""




#Creation of Classes
""" creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)
creator.create('Cluster', dict)

toolbox = base.Toolbox()

toolbox.register('indexes', random.sample, range(1, indSize + 1), indSize)
toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)


toolbox.register('populatecluster', initCluster, creator.Cluster, customers=customers, depots=depots)





toolbox.register('evaluate', evalVRPTW, instance=instance, unitCost=unitCost, initCost=initCost, waitCost=waitCost, delayCost=delayCost)
toolbox.register('select', tools.selRoulette)
toolbox.register('mate', cxPartialyMatched)
toolbox.register('mutate', mutInverseIndexes) """