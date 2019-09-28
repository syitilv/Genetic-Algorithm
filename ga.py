import numpy as np
import random

def f(x1,x2):
    left = (4-2.1 * (x1**2) + (x1**4)/3) * x1**2
    mid = x1*x2
    right = (-4 + (4 * x2**2)) * x2**2 
    return left+mid+right

# def fitness(chromosome):
#     i = 0
#     while i < len(chromosome):
#         chromosome

chromosome = np.random.randint(2,size=(10,6))
chromosomeList = []
info = {}
for i in range (len(chromosome)):
    info['genotype'] = chromosome[i]
    info['f'] = f(chromosome[i][:3], chromosome[i][3:])
    chromosomeList.append(info)
print(chromosome)
print("f si 0: ", f(chromosome[0][:3],chromosome[0][3:]))
print("info si 0: ",info['f'][0])
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

