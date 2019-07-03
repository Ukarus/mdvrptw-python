import random, string, copy


class DNA:
    
    def __init__(self, target):
        self.genes = [] # cambiar esto a una lista dado que los strings son inmutables en python
        self.fitness = 0
        self.target = target
        letters = string.ascii_lowercase + ' '
        for i in range(len(self.target)):
            self.genes.append(random.choice(letters))
    
    def calculate_fitness(self):
        score = 0
        for i in range(len(self.target)):
            if self.genes[i] == self.target[i]:
                score += 1
        self.fitness = round((score / len(self.target)), 4) #this is a linear approach
        # self.fitness = round ( pow(2, score) / 100, 4) 


    def crossover(self, partner):
        child = DNA(self.target)
        new_genes = []
        midpoint = int(random.choice(range(len(partner.genes))))
        for i in range(len(child.genes)):
            if i > midpoint:
                new_genes.append(self.genes[i])
            else:
                new_genes.append(partner.genes[i])
        child.genes = new_genes
        return child

    def mutate(self, mutation_rate):
        letters = string.ascii_lowercase + ' '
        for i in range(len(self.genes)):
            random_n = round(random.randint(1, 100)/100, 2)
            if (random_n < mutation_rate):
                self.genes[i] = random.choice(letters)

    def getPhenotype(self):
        return ''.join(self.genes)


    


def getNeighboors(population, index):
    newPopulation = population.copy()
    newPopulation.pop(index)
    return newPopulation

def getMinFitness(population):
    minFitness = 2
    for i in population:
        if population[i].fitness < minFitness:
            minFitness = population[i].fitness 
    return minFitness


def intelligent_mutation(state):
    letters = string.ascii_lowercase + ' '
    newNode = copy.deepcopy(state)
    for i in range(len(state.genes)):
        if state.genes[i] != state.target[i]:
            newNode.genes[i] = random.choice(letters)
    newNode.calculate_fitness()
    return newNode

def climbing_hill(population, index):
    currentNode = population[index]
    while currentNode.fitness < 0.99:
        newNode = intelligent_mutation(currentNode)
        print(currentNode.fitness, newNode.fitness)
        if newNode.fitness > currentNode.fitness:
            currentNode = newNode
    return currentNode

def mating_pool(population):
    pool = []
    for i in range(len(population)):
        n = int(population[i].fitness * 100)
        for j in range(n):
            pool.append(population[i])
    return pool

def check_phrase(population, phrase):
    
    for i in range(len(population)):
        if population[i].getPhenotype() == phrase:
            return True
    return False

def reproduction(population, pool, mutation_rate):
    offspring = []
    for i in range(len(population)):
        parent_a = random.choice(pool)
        parent_b = random.choice(pool)
        child = parent_a.crossover(parent_b)
        child.mutate(mutation_rate)
        # child.fitness
        offspring.append(child)
    return offspring

population = []
mutation_rate = 0.02
population_n = 200
phrase = 'the cat ate my source code'
generations = 130
n = 0
max_fitness = 0
best_gen = DNA(phrase)
best_gen.calculate_fitness()
#initialize population
for i in range(population_n):
    dna = DNA(phrase)
    dna.calculate_fitness()
    population.append(dna)
# random_index = random.randint(0, len(population) - 1)
# newAgent = climbing_hill(population, random_index)
# print(newAgent.fitness, newAgent.getPhenotype())
# # print (climbing_hill(population, random.choice(population) ))

#check if in the initial population there is at least one that is a exact match against the phrase
is_target = check_phrase(population, phrase)

while is_target == False:
    #calculate fitness
    for i in range(len(population)):
        population[i].calculate_fitness()

    # build a mating pool
    pool = mating_pool(population) #selection
    population = reproduction(population, pool, mutation_rate)
    is_target = check_phrase(population, phrase)
    n += 1

for i in range(len(population)):
    population[i].calculate_fitness()
    if population[i].fitness > max_fitness:
        best_gen = population[i]
        max_fitness = best_gen.fitness
print('\n')
print(best_gen.genes, best_gen.fitness, n)
# for i in range(len(population)):
#     print (population[i].genes, population[i].fitness)

# parent_a = random.choice(pool)
# parent_b = random.choice(pool)
# print ('\n')
# print(parent_a.genes, parent_a.fitness)
# print(parent_b.genes, parent_b.fitness)
# child = parent_a.crossover(parent_b)
# print (child.genes, child.fitness)
# child.mutate(mutation_rate)
# print (child.genes, child.fitness)

# print(population)

# create a population of n individuals
# def createPopulation(n):
#     population = []
#     for individual in range(n):
#         lowercase_letters = string.ascii_lowercase
#         random_string = random.choice(lowercase_letters) + random.choice(lowercase_letters) + random.choice(lowercase_letters)
#         population.append(random_string)
#     return population


# print(createPopulation(50))

