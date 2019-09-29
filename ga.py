import numpy as np
import random
from decimal import Decimal

def generatePopulation(): ##generate the first population
    chromosome = np.random.randint(2,size=(30,12))
    chromosomeList = []
    info = {}
    size = len(chromosome[0])
    print(size)
    for i in range (len(chromosome)):
        x1 = encoding(chromosome[i][:size//2], -3, 3)
        x2 = encoding(chromosome[i][size//2:], -2, 2)
        info = {'genotype': chromosome[i],
        'x1': x1, 
        'x2': x2,
        'f': f(x1,x2),
        'fitness': fitness(f(x1,x2))}
        chromosomeList.append(info.copy())
        print(chromosomeList[i]['genotype'])
        print(chromosomeList[i]['x1'])
        print(chromosomeList[i]['x2'])
        print(chromosomeList[i]['f'])
        print(chromosomeList[i]['fitness'])
        print("")
    print("INI POPULASI AWAL")
    print(chromosomeList)
    print("")
    return chromosomeList

def findMaxFitness(population): ##find the chromosome that has the largest fitness
    population.sort(key=lambda select:select['fitness'],reverse=True)
    max = population[0]['f']
    return max

def f(x1,x2): ##calculating the value of the f from x1 and x2
    left = (4-(2.1 * (x1**2)) + ((x1**4)/3)) * x1**2
    mid = x1*x2
    right = (-4 + (4 * x2**2)) * x2**2 
    f = left+mid+right
    return f

def encoding(x, rmin, rmax): ##encoding the genotype chromosome into fenotype
    bottom = 0
    right = 0
    for i in range (len(x)):
        bottom = bottom + 2**-(i+1)
    for j in range(len(x)):
        right = right + (x[j] * 2**-(j+1))
    phenotype = rmin + ((rmax - rmin)/bottom) * right
    return phenotype

def fitness(f): ##calculating the fitness of the chromosome
    return (2**(-f))

def ParentSelection(population): #choosing 2 parents from the population
    parents = random.choices(population, k=10)
    parents.sort(key=lambda select:select['fitness'],reverse=True)
    return parents[:2]

def Crossover(parents): #crossover from parents into 2 children
    child = []
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
    probability = np.random.randint(0,100)
    if (probability == 1):
        child[0]['genotype'][np.random.randint(0,len(child[0]['genotype'])-1)] = np.random.randint(0,1)
        child[1]['genotype'][np.random.randint(0,len(child[1]['genotype'])-1)] = np.random.randint(0,1)
    print("INI ANAK")
    print(child)
    print("")
    return child

def Survivor(mutation,population): #new generation with steady state method
    print("INI POPULASI SEBELUM SORT FITNESS")
    print(population)
    print("")
    population.sort(key=lambda select:select['fitness'],reverse=False)
    print("INI POPULASI SETELAH SORT FITNESS")
    print(population)
    print("")
    print(mutation)
    size = len(mutation[0]['genotype'])
    for i in range (len(mutation)):
        x1 = encoding(mutation[i]['genotype'][:size//2], -3, 3)
        x2 = encoding(mutation[i]['genotype'][size//2:], -2, 2)
        mutation[i]['x1'] = x1
        mutation[i]['x2'] = x2
        mutation[i]['f'] = f(x1,x2)
        mutation[i]['fitness'] = fitness(f(x1,x2))
    print("INI ANAK HASIL MUTASI")
    print(mutation[0])
    print(mutation[1])
    population.remove(population[0])
    population.remove(population[0])
    population.append(mutation[0])
    population.append(mutation[1])
    print("")
    print("INI POPULASI SETELAH MUTASI")
    print(population)
    return population

generation = 0
population = generatePopulation()
while generation <= 50: #main function, will stop after reached 100th generation
    print("Generasi ke-", generation)
    print("POPULASI")
    print(population)
    print("")
    max = findMaxFitness(population)
    parents = ParentSelection(population)
    child = Crossover(parents)
    mutation = Mutation(child)
    population = Survivor(mutation, population)
    generation = generation + 1
    print("--------------------best result: ", max)
    print("")