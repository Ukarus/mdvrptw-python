# -*- coding: utf-8 -*-

import os
import json
import operator
import common
import random

def sortbyPrice(bidList):
    bidList.sort(key= operator.itemgetter(1))
    return bidList

def getcapacities(stringline):
    vehicle_capacity = []
    for i in range(1, len(stringline)):
        vehicle_capacity.append(int(stringline[i]))
    return vehicle_capacity


def getLots(instanceLots):
    lenLots = len(instanceLots)
    lots = {}
    for i in range (0, lenLots):
        product_id = instanceLots[i]['semilla_id']
        demand = instanceLots[i]['cantidad']
        lots['%i' %int(product_id)] = demand
    return lots

def coveredDemand(instanceLots, instanceBids, bidsroute, delivery):
    lots = instanceLots
    for routeid in bidsroute:
        mybids = bidsroute[routeid]
        for bidid, price, amount in mybids:
            lotid = instanceBids[str(bidid)]['lot_id']
            lots['lots'][lotid]['demand']-=amount
    for bidID in delivery:
        lotid = instanceBids[bidID]['lot_id']
        available = delivery[bidID][1]
        lots['lots'][lotid]['demand']-=available
    return lots


#Función para evaluar si queda demanda restante
def demandLeft(lots):
    jsonData = {}
    jsonData['demand_left']=[]
    lenlots = len(lots)
    for aux in range(0,lenlots):
        productid = lots[aux]['product_id']
        missing = lots[aux]['demand']
        if(lots[aux]['demand']>0):
            jsonData['demand_left'].append({
                'semilla_id': productid,
                'missing': missing
            })
    return jsonData


#Función para generar lotes artificiales de ofertas
def bidsGenerator(instanceProducts, instanceLots, nBids, vendors):
    maxPrice = 350
    maxAvailable = 500
    productsID = instanceProducts['product_base'].keys()
    lenLots = len(instanceLots['lots'])
    jsonData = {}
    ct = 0
    for i in range(0,nBids):
        lotID = 0
        randomProduct = random.choice(productsID)
        randomVendor = random.randint(1, vendors)
        randomPrice = random.randint(50, maxPrice)
        randomAvailable = random.randint(100, maxAvailable)
        for auxLot in range(0, lenLots):
            productLotID = instanceLots['lots'][auxLot]['product_id']
            if (randomProduct == productLotID):
                lotID = auxLot
        jsonData['%s' %ct]={
            'vendor_id': str(randomVendor),
            'product_id': randomProduct,
            'lot_id': lotID,
            'price': randomPrice,
            'available': randomAvailable,
            'delivery': random.randint(0,1)
        }
        ct+=1
    return jsonData


#Función para generar lotes artificiales de demanda
def lotsGenerator(instanceProducts, nLots):
    productsID = instanceProducts['product_base'].keys()
    MaxDemand = 500
    jsonData = {}
    jsonData['lots'] = []
    for i in range(0, nLots):
        randomProduct = random.choice(productsID)
        jsonData['lots'].append({
            'product_id': randomProduct,
            'demand': random.randint(0,MaxDemand)
        })
    return jsonData

#Obtener bids asociados a un vendorID
def getBids4ind(vendorID, instanceBids):
    listofBids = []
    lenBids = len(instanceBids)
    for bidid in range(0,lenBids):
        user_id = instanceBids[bidid]['user_id']
        price = instanceBids[bidid]['precio']
        if (str(user_id) == vendorID):
            listofBids.append([bidid,price])
    return listofBids


def generatedelivery(delivery, instanceBids):
    jsonData = {}
    jsonData['delivery'] = []
    for key in delivery:
        vendor_id = instanceBids[int(key)]['user_id']
        jsonData['delivery'].append({
            'bidid': key,
            'vendorid': vendor_id,
            'price': delivery[key][0],
            'amount': delivery[key][1]
        })
    return jsonData

#Generar bids para la ruta
def GenerateRouteData(routes, instanceBids, bidsroute):
    jsonData = {}
    jsonData['routes']=[]
    routeid = 0
    for route in routes:
        routestr = route.replace(" ", "")
        mybids = bidsroute[str(routeid)]
        tobuy = []
        for bidid, price, amount in mybids:
            vendorid = instanceBids[bidid]['user_id']
            semillaid = instanceBids[bidid]['semilla_id']
            tobuy.append({
                'amount': amount,
                'vendorid': vendorid,
                'semilla_id': semillaid,
                'price': price
            })
        jsonData['routes'].append({
            'route':routestr,
            'to_buy':tobuy,
        })
        routeid+=1
    return jsonData

#Escribir al archivo Json
def writeFileJson(jsonData, instName , DataDir):
    jsonFilename = '%s.json' % instName
    jsonFile = os.path.join(DataDir, jsonFilename)
    print 'Writing %s to: %s' %(jsonFilename, DataDir)
    with open(jsonFile, 'w') as f:
        json.dump(jsonData, f, sort_keys=True)
        #json.dump(jsonData, f, indent=4, separators=(',', ': '), sort_keys=True)


def getFile(instName, dataDir):
    myJson = os.path.join(dataDir,'%s.json' %instName)
    with open(myJson) as f:
        instance = json.load(f)
    return instance


def generateCustomerRouteData(myroute, instancecustomers):
    jsonData = {}
    jsonData['routes'] = []
    for subroute in myroute:
        product_deliver = []
        subroute = subroute.replace(" ","")
        for customerID in subroute:
            if customerID !='0' and customerID!='-' and customerID:
                products = instancecustomers["customer_%s"%customerID]["products_deliver"]
                customerid = instancecustomers["customer_%s"%customerID]["id"]
                for productid, amount in products:
                    product_deliver.append({
                        'product_id': productid,
                        'amount': amount,
                        'customer_id':customerid
                    })
        jsonData['routes'].append({
            'route': subroute,
            'deliver': product_deliver
        })
    return jsonData


def getvendors_idsfromjson(instance):
    vendorsid = []
    for key in instance:
        if "customer_" in key:
            fullstring = key.split("_")
            id = fullstring[1]
            vendorsid.append(int(id))
    return vendorsid
            

