import numpy as np
import random
import csv

def generatePopulation(): ##generate the first population
    chromosome = np.random.randint(2,size=(3,28))
    chromosomeList = []
    
    for i in range (len(chromosome)):
        info = {}
        infoRule = {}
        ruleList = []
        ruleNum = len(chromosome[i])//14
        for j in range(ruleNum):
            
            found = False

            while not found:
                temp = chromosome[i][j*14:(j+1)*14][:3]
                if list([0,0,0]) == list(temp):
                    chromosome[i] = np.random.randint(2,size=(1,28))
                    found = True
                time = chromosome[i][j*14:(j+1)*14][3:7]
                if list(time) == list([0,0,0,0]):
                    chromosome[i] = np.random.randint(2,size=(1,28))
                    found = True
                sky = chromosome[i][j*14:(j+1)*14][7:11]
                if list(sky) == list([0,0,0,0]):
                    chromosome[i] = np.random.randint(2,size=(1,28))
                    found = True
                humidity = chromosome[i][j*14:(j+1)*14][11:14]
                if list(humidity) == list([0,0,0]):
                    chromosome[i] = np.random.randint(2,size=(1,28))
                    found = True
                found = True
            infoRule = {'chromosome': chromosome[i][j*14:(j+1)*14],
            'temp': chromosome[i][j*14:(j+1)*14][:3],
            'time': chromosome[i][j*14:(j+1)*14][3:7],
            'sky': chromosome[i][j*14:(j+1)*14][7:11],
            'humidity': chromosome[i][j*14:(j+1)*14][11:14]
            }
            ruleList.append(infoRule.copy())
        info = {'rule': ruleNum,
        'rule list': ruleList,
        'chromosome':  chromosome[i]
        }
        chromosomeList.append(info.copy())
    return chromosomeList

def findMaxFitness(population): ##find the chromosome that has the largest fitness
    population.sort(key=lambda population:population['fitness'],reverse=True)
    max = population[0]
    return max

def readData(location): ##read data from .txt file
    f = open(location, 'r')
    row = f.readlines()

    attribute = []
    dataTrain = []

    y = 0

    while y < len(row):
        attribute.append(row[y].split())
        y = y + 1
    
    info = {}

    for i in range(len(attribute)):
        temp = decoding(attribute[i][0],3)
        time = decoding(attribute[i][1],4)
        sky = decoding(attribute[i][2],4)
        humidity = decoding(attribute[i][3],3)
        fly = attribute[i][4]
        info = {'rule': attribute[i],
        'temp': temp,
        'time': time,
        'sky': sky,
        'humidity': humidity,
        'fly': fly
        }
        dataTrain.append(info.copy())
    return dataTrain

def decoding(x, bitNum):
    chromosome = []
    for i in range(bitNum):
        chromosome.append(int(0))
    chromosome[int(x)] = int(1)
    return chromosome

def fitness(dataTrain, decisionTree): ##count fitness from decision tree
    for i in range(len(decisionTree)):
        truthFinal = []
        truthChromosome = []
        for j in range(decisionTree[i]['rule']):
            truthRule = []
            for k in range(len(dataTrain)):
                truthCol = []
                for l in range(len(dataTrain[k]['rule'])-1):
                    if l == 0:
                        attribute = "temp"
                    elif l == 1:
                        attribute = "time"
                    elif l == 2 :
                        attribute = "sky"
                    elif l == 3 :
                        attribute = "humidity"
                    
                    if decisionTree[i]['rule list'][j][attribute][int(dataTrain[k]['rule'][l])] == 1:
                        truthCol.append(1)
                    else:
                        truthCol.append(0)
                if False in truthCol:
                    truthRule.append(0)
                else:
                    truthRule.append(1)
            truthChromosome.append(truthRule)
        for m in range(len(dataTrain)):
            found = False
            n = 0
            while n < len(truthChromosome):
                if int(truthChromosome[n][m]) == 1:
                    found = True
                n = n + 1
            if found:
                truthFinal.append(1)
            elif not found:
                truthFinal.append(0)

        error = 0
        fitness = 0
        p = 0
        totalData = len(dataTrain)
        while p < totalData:
            # print("row", p)
            if (truthFinal[p] != int(dataTrain[p]['fly'])):
                error = error + 1
            p = p + 1
        fitness = (totalData - error)/totalData
        decisionTree[i]['fitness'] = fitness
    for i in range (len(decisionTree)):
        print("fitness ",decisionTree[i]['fitness'])
    return decisionTree

def ParentSelection(population): #choosing 2 parents from the population with tournament selection
    parents = random.choices(population, k=3)
    parents.sort(key=lambda parents:parents['fitness'],reverse=True)
    return parents[:2]

def Crossover(parents): #crossover from parents making 2 children with 70% probability
    probability = np.random.randint(0,100)
    child = []
    point = 0
    point2 = 0
    temp = 0
    genChild = []
    genChild2 = []
    if (probability <= 70):
        infoChild = {}
        point = np.random.randint(1,len(parents[0]['chromosome'])-1)
        # point2 = random.randint(1,len(parents[1]['chromosome'])-1)
        # while abs(point-point2) == 0:
        #     point = np.random.randint(1,len(parents[0]['chromosome']))
        #     point2 = random.randint(1,len(parents[1]['chromosome']))
        if(point > 14):
            point2 = point%14
        else:
            point2 = point

        genChild = np.append(parents[0]['chromosome'][:point2], parents[1]['chromosome'][point:])
        print("genchild: ",genChild)
        genChild2 = np.append(parents[0]['chromosome'][:point], parents[1]['chromosome'][point2:])
        print("genchild2: ",genChild2)

        # genChild = parents[0]['chromosome']
        # temp = point
        # while temp < point2:
        #     genChild[temp] = parents[1]['chromosome'][temp]
        #     temp = temp+1
 
        # genChild2 = parents[1]['chromosome']
        # temp = point
        # while temp < point2:
        #     genChild2[temp] = parents[0]['chromosome'][temp]
        #     temp = temp+1
        # genChild2 = np.append(genChild2,[parents[0]['chromosome'][:14]])

        infoChild = {
            'chromosome': genChild,
        }
        child.append(infoChild)

        infoChild = {
            'chromosome': genChild2,
        }
        child.append(infoChild)
    print(child)
    return child

def Mutation(child):
    if (child != []):
        probability = np.random.randint(0,100)
        if (probability == 1):
            num1 = np.random.randint(0,len(child[0]['chromosome'])-1)
            num2 = np.random.randint(0,len(child[1]['chromosome'])-1)
            if child[0]['chromosome'][num1] == 0:
                child[0]['chromosome'][num1] = 1
            else:
                child[0]['chromosome'][num1] = 0
            if child[1]['chromosome'][num2] == 0:
                child[1]['chromosome'][num2] = 1
            else:
                child[1]['chromosome'][num2] = 0
    return child

def Survivor(mutation,population): #creating new generation with steady state method
    if (mutation != []):
        population.sort(key=lambda population:population['fitness'],reverse=False)
        for i in range (len(mutation)):
            ruleNum = len(mutation[i])//14
            for j in range(ruleNum):
            
                found = False

                while not found:
                    temp = mutation[i][j*14:(j+1)*14][:3]
                    if list([0,0,0]) == list(temp):
                        mutation[i] = np.random.randint(2,size=(1,28))
                        found = True
                    time = mutation[i][j*14:(j+1)*14][3:7]
                    if list(time) == list([0,0,0,0]):
                        mutation[i] = np.random.randint(2,size=(1,28))
                        found = True
                    sky = mutation[i][j*14:(j+1)*14][7:11]
                    if list(sky) == list([0,0,0,0]):
                        mutation[i] = np.random.randint(2,size=(1,28))
                        found = True
                    humidity = mutation[i][j*14:(j+1)*14][11:14]
                    if list(humidity) == list([0,0,0]):
                        mutation[i] = np.random.randint(2,size=(1,28))
                        found = True
                    found = True
                mutation[i]['rule list']['chromosome'] = mutation[i][j*14:(j+1)*14]
                mutation[i]['rule list']['temp'] = mutation[i][j*14:(j+1)*14][:3]
                mutation[i]['rule list']['time'] = mutation[i][j*14:(j+1)*14][3:7]
                mutation[i]['rule list']['sky'] = mutation[i][j*14:(j+1)*14][7:11]
                mutation[i]['rule list']['humidity'] = mutation[i][j*14:(j+1)*14][11:14]
            mutation[i]['rule'] = ruleNum
            mutation[i]['chromosome'] = mutation[i]
        population.remove(population[0])
        population.remove(population[0])
        population.append(mutation[0])
        population.append(mutation[1])
    return population

def readDataTest(location): ##read data from .txt file
    f = open(location, 'r')
    row = f.readlines()

    attribute = []
    dataTest = []

    y = 0

    while y < len(row):
        attribute.append(row[y].split())
        y = y + 1
    
    info = {}

    for i in range(len(attribute)):
        temp = decoding(attribute[i][0],3)
        time = decoding(attribute[i][1],4)
        sky = decoding(attribute[i][2],4)
        humidity = decoding(attribute[i][3],3)
        info = {'rule': attribute[i],
        'temp': temp,
        'time': time,
        'sky': sky,
        'humidity': humidity
        }
        dataTest.append(info.copy())
    return dataTest

def test(dataTest, decisionTree):
    truthFinal = []
    for i in range(len(decisionTree)):
        truthChromosome = []
        for j in range(decisionTree[i]['rule']):
            truthRule = []
            for k in range(len(dataTrain)):
                truthCol = []
                for l in range(len(dataTrain[k]['rule'])-1):
                    if l == 0:
                        attribute = "temp"
                    elif l == 1:
                        attribute = "time"
                    elif l == 2 :
                        attribute = "sky"
                    elif l == 3 :
                        attribute = "humidity"
                    
                    if decisionTree[i]['rule list'][j][attribute][int(dataTrain[k]['rule'][l])] == 1:
                        truthCol.append(1)
                    else:
                        truthCol.append(0)
                if False in truthCol:
                    truthRule.append(0)
                else:
                    truthRule.append(1)
            truthChromosome.append(truthRule)
        for m in range(len(dataTrain)):
            found = False
            n = 0
            while n < len(truthChromosome):
                if int(truthChromosome[n][m]) == 1:
                    found = True
                n = n + 1
            if found:
                truthFinal.append(1)
            elif not found:
                truthFinal.append(0)
    print("final: ",truthFinal)
    return truthFinal

generation = 0
population = generatePopulation()
dataTest = readDataTest('/Users/syiti/Documents/Repository/Genetic-Algorithm/data_uji_opsi_2.txt')
dataTrain = readData('/Users/syiti/Documents/Repository/Genetic-Algorithm/data_latih_opsi_2.txt')
while generation < 3:
    print("Generasi ke-", generation)
    population = fitness(dataTrain,population)
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
test(dataTest, population)