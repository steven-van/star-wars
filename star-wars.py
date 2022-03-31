from random import uniform, randint
import csv
import numpy as np
import time

# Lecture du fichier et ranger les données dans un dictionnaire
def read_file(file):
    file_to_read = open(file, 'r')
    reader = list(csv.reader(file_to_read, delimiter = ";"))
    reader.pop(0)
    reader = sorted(reader, key = lambda item: item[0])
    positions = {}
    for element in reader:
        t = float(element[0])
        x = float(element[1])
        y = float(element[2])
        positions[t] = [x, y]
    return positions

# Création d'individus ind = [p1,p2,p3,p4,p5,p6]
def create_ind():
    ind = [uniform(-100,100) for i in range(6)]
    return ind

# Création d'une population de k individus
def create_pop(k):
    pop = [create_ind() for i in range(k)]
    return pop

# Calcul de l'écart entre les coordoonées x, y réels et x,y rapprochés
def gap(ind, t, x, y):
     return np.abs(x -  (ind[0] * np.sin((ind[1] * t)+ ind[2]))) + np.abs(y - (ind[3] * np.sin((ind[4] * t)+ ind[5])))

# Somme des écarts  
def fitness(ind, data):
    return sum( gap(ind, key, data[key][0], data[key][1]) for key in data.keys() )

# Tri de la liste population selon fitness
def evaluate(pop, data):
    return sorted(pop, key = lambda ind : fitness(ind, data))

# Retourne une sous population avec les n premiers elements de la liste pop
def selection(pop, data, n):
    return evaluate(pop, data)[:n]

# Retourne deux individus à partir de deux individus ind1 et ind2 
# (p premières données de ind1 suivies des p dernières de ind2 
# puis p premières données de ind2 suivies des p dernières de ind1)
def crossover(ind1, ind2):
    p = randint(1,4)
    return ind1[:p] + ind2[p:], ind2[:p] + ind1[p:]

# Retourne un individu suite à la mutation de ind
# Il s’agit de prendre un indice aléatoire de l’individu (entre 0 et 5) et 
# la remplacer la donnée correspondante par une nouvelle valeur aléatoire 
def mutation(ind):
    index = randint(0, len(ind)-1)
    ind[index] = uniform(-100,100)
    return ind

def genetic_algo(pop_length, fitness_limit, gen_limit):

    data = read_file("position_sample.csv")
    start = time.time()
    pop = create_pop(pop_length)
    fitness_list = []
   
    for generations in range(gen_limit):
        selected_pop = selection(pop, data, len(pop)//2) 
        minimumFitness = fitness(selected_pop[0],data)
        
        if minimumFitness <= fitness_limit:
            break 
        
        fitness_list += [minimumFitness]
        nextGen = []

        for i in range(0,len(selected_pop),2):
            child1,child2 = crossover(selected_pop[i],selected_pop[i+1])
            nextGen += [child1,child2]

        for i in range(0,len(selected_pop),2): 
            nextGen+=[mutation(selected_pop[i])]

        nextGen += create_pop(pop_length - len(nextGen))
        pop = nextGen
        
    pop = evaluate(pop, data)
    end = time.time()
    runtime = end - start

    return pop[0], generations, runtime, data

if __name__ == "__main__":
    solution, nb_gen, runtime, data = genetic_algo(100,50,20000)
    print(f"x(t) = {solution[0]} * sin({solution[1]} * t + {solution[2]})")
    print(f"y(t) = {solution[3]} * sin({solution[4]} * t + {solution[5]})")
    print(f"number of generations : {nb_gen}")
    print(f"time : {runtime} s")
    print(f"fitness: {fitness(solution, data)}")