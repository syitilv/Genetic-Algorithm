import numpy as np
import random

def generatePopulation(): ##generate the first population
    chromosome = np.random.randint(2,size=(30,12))
    chromosomeList = []
    info = {}
    size = len(chromosome[0])
    for i in range (len(chromosome)):
        x1 = encoding(chromosome[i][:size//2], -3, 3)
        x2 = encoding(chromosome[i][size//2:], -2, 2)
        info = {'genotype': chromosome[i],
        'x1': x1, 
        'x2': x2,
        'f': f(x1,x2),
        'fitness': fitness(f(x1,x2))}
        chromosomeList.append(info.copy())
    return chromosomeList

def findMaxFitness(population): ##find the chromosome that has the largest fitness
    population.sort(key=lambda population:population['fitness'],reverse=True)
    max = population[0]
    return max

def encoding(x, rmin, rmax): ##encoding the genotype chromosome into fenotype
    bottom = 0
    right = 0
    for i in range (len(x)):
        bottom = bottom + 2**-(i+1)
    for j in range(len(x)):
        right = right + (x[j] * 2**-(j+1))
    phenotype = rmin + ((rmax - rmin)/bottom) * right
    return phenotype

def f(x1,x2): ##calculating the value of the f from x1 and x2
    left = (4-(2.1 * (x1**2)) + ((x1**4)/3)) * x1**2
    mid = x1*x2
    right = (-4 + (4 * x2**2)) * x2**2 
    f = left+mid+right
    return f

def fitness(f): ##calculating the fitness of the chromosome
    return (-f)

def ParentSelection(population): #choosing 2 parents from the population with tournament selection
    parents = random.choices(population, k=10)
    parents.sort(key=lambda parents:parents['fitness'],reverse=True)
    return parents[:2]

def Crossover(parents): #crossover from parents making 2 children with 70% probability
    probability = np.random.randint(0,100)
    child = []
    if (probability <= 70):
        infoChild = {}
        point = np.random.randint(1,len(parents[0]['genotype']))
        genChild = np.append([parents[0]['genotype'][:point]],[parents[1]['genotype'][point:]])
        infoChild = {
            'genotype': genChild,
        }
        child.append(infoChild)
        genChild2 = np.append([parents[1]['genotype'][:point]],[parents[0]['genotype'][point:]])
        infoChild = {
            'genotype': genChild2,
        }
        child.append(infoChild)
    return child

def Mutation(child): #mutation of the children with 1% probability
    if (child != []):
        probability = np.random.randint(0,100)
        if (probability == 1):
            num1 = np.random.randint(0,len(child[0]['genotype'])-1)
            num2 = np.random.randint(0,len(child[1]['genotype'])-1)
            if child[0]['genotype'][num1] == 0:
                child[0]['genotype'][num1] = 1
            else:
                child[0]['genotype'][num1] = 0
            if child[1]['genotype'][num2] == 0:
                child[1]['genotype'][num2] = 1
            else:
                child[1]['genotype'][num2] = 0
    return child

def Survivor(mutation,population): #creating new generation with steady state method
    if (mutation != []):
        population.sort(key=lambda population:population['fitness'],reverse=False)
        size = len(mutation[0]['genotype'])
        for i in range (len(mutation)):
            x1 = encoding(mutation[i]['genotype'][:size//2], -3, 3)
            x2 = encoding(mutation[i]['genotype'][size//2:], -2, 2)
            mutation[i]['x1'] = x1
            mutation[i]['x2'] = x2
            mutation[i]['f'] = f(x1,x2)
            mutation[i]['fitness'] = fitness(f(x1,x2))
        population.remove(population[0])
        population.remove(population[0])
        population.append(mutation[0])
        population.append(mutation[1])
    return population

generation = 0
population = generatePopulation()
while generation <= 300: #main function, will stop after reached 300th generation
    print("Generasi ke-", generation)
    max = findMaxFitness(population)
    parents = ParentSelection(population)
    child = Crossover(parents)
    mutation = Mutation(child)
    population = Survivor(mutation, population)
    generation = generation + 1
    print("--------------------")
    print("BEST RESULTS: ")
    print(max)
    print("--------------------")
    print("")