import csv
import numpy as np
import time

# Lecture du fichier et rangement des données dans un dictionnaire
def read_file(file):
    file_to_read = open(file, 'r')
    reader = list(csv.reader(file_to_read, delimiter = ";"))
    reader.pop(0)
    positions = {}
    for element in reader:
        t = float(element[0])
        x = float(element[1])
        y = float(element[2])
        positions[t] = [x, y]
    return positions

# Création d'individus ind = [p1,p2,p3,p4,p5,p6]
def create_ind():
    ind = [np.random.uniform(-100,100) for i in range(6)]
    return ind

# Création d'une population de k individus
def create_pop(k):
    pop = [create_ind() for i in range(k)]
    return pop

# Calcul de l'écart entre les coordoonées x, y théoriques et x,y approchés
def gap(ind, t, x, y):
     return np.abs(x - (ind[0] * np.sin((ind[1] * t)+ ind[2]))) + np.abs(y - (ind[3] * np.sin((ind[4] * t)+ ind[5])))

# Somme des écarts  
def fitness(ind, data):
    return sum( gap(ind, key, val[0], val[1]) for key, val in data.items() )

# Tri de la liste population selon fitness
def evaluate(pop, data):
    return sorted(pop, key = lambda ind : fitness(ind, data))

# Retourne une sous population avec les n premiers elements de la liste pop
def selection(pop, data, n):
    return evaluate(pop, data)[:n]

# Retourne deux individus à partir de deux individus ind1 et ind2 
# la premiere moitié des données de ind1 suivies de la dernière moitié de ind2 et inversement
def crossover(ind1, ind2):
    return [ind1[:3] + ind2[-3:], ind2[:3] + ind1[-3:]]

# Retourne un individu suite à la mutation de ind
# Il s’agit de prendre un indice aléatoire de l’individu (entre 0 et 5) et 
# la remplacer la donnée correspondante par une nouvelle valeur aléatoire 
def mutation(ind):
    index = np.random.randint(0,5)
    ind[index] = np.random.uniform(-100,100) 
    return ind

def genetic_algo(data, pop_length, fitness_limit):
    start = time.time()
    pop = create_pop(pop_length)
    generation = 0
    minimumFitness = fitness_limit + 1
    while(minimumFitness >= fitness_limit):
        selected_pop = selection(pop, data,pop_length//2) 
        minimumFitness = fitness(selected_pop[0],data)
        crossed_pop = []
        mutated_pop = []
        
        for i in range(0,len(selected_pop),2):
            crossed_pop += crossover(selected_pop[i],selected_pop[i+1])
            mutated_pop += [ mutation(selected_pop[i]) ]

        next_gen = crossed_pop + mutated_pop + create_pop(pop_length)
        pop = next_gen
        print(f"fitness : {minimumFitness} | generation : {generation}")
        generation += 1
        
    pop = evaluate(pop, data)
    end = time.time()
    runtime = end - start

    return pop[0], generation, runtime

if __name__ == "__main__":
    data = read_file("position_sample.csv")
    POP = 500
    FITNESS_LIMIT = 30 # TO CHANGE
    
    solution, nb_gen, runtime = genetic_algo(data, POP,FITNESS_LIMIT)
    print(f"Population : {POP}, Fitness Limit : {FITNESS_LIMIT}")
    print(f"x(t) = {solution[0]} * sin({solution[1]} * t + {solution[2]})")
    print(f"y(t) = {solution[3]} * sin({solution[4]} * t + {solution[5]})")
    print(f"number of generations : {nb_gen}")
    print(f"time : {round(runtime // 60)} min {round(runtime % 60)} s")
    print(f"fitness: {fitness(solution, data)}")