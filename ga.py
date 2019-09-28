import numpy as np
import random
from decimal import Decimal

def generatePopulation():
    chromosome = np.random.randint(2,size=(10,6))
    chromosomeList = []
    info = {}
    for i in range (len(chromosome)):
        x1 = encoding(chromosome[i][:3], -3, 3)
        x2 = encoding(chromosome[i][3:], -2, 2)
        info = {'genotype': chromosome[i],
        'x1': x1, 
        'x2': x2,
        'f': f(x1,x2),
        'fitness': fitness(f(x1,x2))}
        chromosomeList.append(info)
        print(chromosomeList[i]['genotype'])
        print(chromosomeList[i]['x1'])
        print(chromosomeList[i]['x2'])
        print(chromosomeList[i]['f'])
        print(chromosomeList[i]['fitness'])
        print("")
    return chromosomeList

def findMin(population):
    population.sort(key=lambda select:select['f'],reverse=False)
    min = population[0]['f']
    return min


def f(x1,x2):
    left = (4-2.1 * (x1**2) + (x1**4)/3) * x1**2
    mid = x1*x2
    right = (-4 + (4 * x2**2)) * x2**2 
    f = left+mid+right
    return f

def encoding(x, rmin, rmax):
    bottom = 0
    right = 0
    for i in range (len(x)):
        bottom = bottom + 2**(i+1)
    for j in range(len(x)):
        right = right + x[j] * 2**(j+1)
    phenotype = rmin + ((rmax - rmin)/bottom) * right
    return phenotype

def fitness(f):
    return 2**(-f)

def ParentSelection(population):
    parents = random.choices(population, k=5)
    parents.sort(key=lambda select:select['fitness'],reverse=True)
    return parents[:2]

def Crossover(parents):
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

def Mutation(child):
    probability = np.random.randint(0,100)
    if (probability == 1):
        child[0]['genotype'][np.random.randint(0,len(child[0]['genotype'])-1)] = np.random.randint(0,1)
        child[1]['genotype'][np.random.randint(0,len(child[1]['genotype'])-1)] = np.random.randint(0,1)
    return child

def Survivor(mutation,population):
    print(population)
    population.sort(key=lambda select:select['fitness'],reverse=False)
    print(population)
    print("")
    print(mutation)
    for i in range (len(mutation)):
        x1 = encoding(mutation[i]['genotype'][:3], -3, 3)
        x2 = encoding(mutation[i]['genotype'][3:], -2, 2)
        mutation[i]['x1'] = x1
        mutation[i]['x2'] = x2
        mutation[i]['f'] = f(x1,x2)
        mutation[i]['fitness'] = fitness(f(x1,x2))
    print(mutation[0])
    print(mutation[1])
    population[0] = mutation[0]
    population[1] = mutation[1]
    print("")
    print(population)
    return population
    # print(population)
    # newPopulation = population.sort(key=lambda select:select['fitness'],reverse=False)
    # print(newPopulation)
    # return newPopulation

generation = 0
population = generatePopulation()
while generation < 2000:
    min = findMin(population)
    parents = ParentSelection(population)
    child = Crossover(parents)
    mutation = Mutation(child)
    population = Survivor(mutation, population)
    generation = generation + 1

print("ini min", min)

# for i in range (len(chromosome)):
#     info['genotype'] = chromosome[i]
#     info['x1'] = encoding(chromosome[i][:3], -3, 3)
#     info['x2'] = encoding(chromosome[i][3:], -2, 2)
#     info['f'] = f(info['x1'],info['x2'])
#     info['fitness'] = fitness(info['f'])
#     chromosomeList.append(info)
#     print("geno: ", chromosomeList[i]['genotype'])
#     print("x1: ", chromosomeList[i]['x1'])
#     print("x2: ", chromosomeList[i]['x2'])
#     print("f: ", chromosomeList[i]['f'])
#     print("fitness: ", chromosomeList[i]['fitness'])
#     print("")
#     print(chromosomeList)
#     print("")

# print(chromosome[0])
# print(chromosome[1])
# print(chromosomeList[0])
# print(chromosomeList[1])
# ParentSelection(chromosomeList)

# chromes = np.random.randint(2,size=(10,6))
# list_of_dict = []
# b = dict()
# for i in range (len(chromes)):
#     b['genotype'] = chromes[i]
#     x1 = chromes[i][:6]
#     x2 = chromes[i][6:]
#     phen1=GenToPhen(x1,3,6)
#     phen2=GenToPhen(x2,0,3)
#     b['fit'] = fitness(phen1,phen2)
#     list_of_dict.append(b)