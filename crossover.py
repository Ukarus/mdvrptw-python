import random


def crossover(ind1, ind2):
        # cxpoint1, cxpoint2 = sorted(random.sample(range(len(ind1)), 2))
        cxpoint1 = 3
        cxpoint2 = 7
        swath = ind1[cxpoint1:cxpoint2+1]

        child = [0 for i in range(len(ind1))]
        child[cxpoint1:cxpoint2+1] = swath

        #find values from parent 2 that are not in the swath
        candidates = []
        for i in range(cxpoint1, cxpoint2 + 1):
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

parent1 = [8, 4, 7, 3, 6, 2, 5, 1, 9, 0]
parent2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

a = crossover(parent1, parent2)
print(a)