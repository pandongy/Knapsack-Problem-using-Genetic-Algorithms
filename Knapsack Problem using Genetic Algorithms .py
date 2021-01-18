#!/usr/bin/env python
# coding: utf-8

# In[72]:


import random
from copy import deepcopy

# the information of boxes from the problem statement
inf = {1: [20, 6], 2: [30, 5], 3: [60, 8], 4: [90, 7], 5: [50, 6], 6: [70, 9],
       7: [30, 4], 8: [30, 5], 9: [70, 4], 10: [20, 9], 11: [20, 2], 12: [60, 1]}

threshold = 3 # use to define when can we stop iterate
weight_max = 250 # the max weight the bag can carry
chromosome_size = 12 # length of each chromosome
population_size = 4000 # size of population
last_max_imp = 0 
last_imp_diff = 10000
mutation_probability = 0.9  

# generate the initial popualtion with 100 chromosomes
def init_population():
    init_pop = []
    p_size = 1
    component = [0,1]
    # the random chromosomes are deterministic  
    random.seed(1)
    
    while p_size < population_size+1:
        chromosome = ''
        c_size = 1
        
        # Each chromosome is randomly composed of twelve 0 and 1
        while c_size < chromosome_size+1:
            chromosome += str(random.choice(component)) 
            c_size += 1
            
        # we define the backpack cannot be empty
        if chromosome != '000000000000':
            init_pop.append(chromosome) 
            p_size += 1
        else:
            p_size = p_size
            
    return init_pop # init_pop is the initial population


# define the sum of weight and the sum of importance for each chromosome as its fitnes function 
def fitness(init_pop):
    fitnesses = []
    
    for chromosome in init_pop: 
        weight_sum = 0  # the weight sum for a chromosome chain
        imp_sum = 0 # the importance sum for a chromosome chain
        
        for i, c in enumerate(chromosome): # traverse the component and its index of one chromosome
            if int(c) == 1: # c is 1 means this box will be carried, i is the index of the box
                weight_sum += inf[i + 1][0] 
                imp_sum += inf[i + 1][1]
                
        # for those chromosomes whose sum of weights are larger than max weight the bag can carry, 
        # set their sum of importances as 0
        if weight_sum > weight_max: 
            imp_sum = 0
        
        fitnesses.append([imp_sum, weight_sum]) 
    return fitnesses


# define when we get the best result
def is_best(fitnesses):
    global last_max_imp
    global last_imp_diff
    
    # the largest importance value for the current generation 
    current_max_imp = 0
    
    # find the largest importance value
    for i in fitnesses:
        if i[0] > current_max_imp:
            current_max_imp = i[0]
             
    # the difference between the max importantce in current generation and the max importance in last generation
    current_imp_diff = current_max_imp - last_max_imp
    
    # if the differences of last generation and the differences of current generation are both less than threshold,
    # stop iterate
    if current_imp_diff < threshold and last_imp_diff <threshold:     
        return True
    else:
        last_imp_diff = current_imp_diff
        last_max_imp = current_max_imp
        return False
    
    
# cull the 50% less fit chromosome chains and remove them
def filter_cull(init_pop, fitnesses):
    
    # combine each chromosome with its importance value
    init_pop = list(zip(init_pop, fitnesses))
    
    # sort the initial population from large to small based on their importance value
    init_pop = sorted(init_pop, reverse = True, key = lambda x: x[1][0])
    
    # remove the 50% population which have lower importance values
    init_pop = init_pop[:round(0.5*len(init_pop))]
    
    # release the combination, only keep the filtered chromosome chain
    init_pop = [x[0] for x in init_pop]
 
    return init_pop


# defining the crossover: randomly choose two chromosomes in the current generation, randomly choose a position of 
# those two chromosomes, then crossover their gene fragment to get child chromosomes, traverse all possible parent
# chromosomes to get child chromosome, and combine all child chromosome to get a new generation
def crossover(init_pop):    
    new_chroms = []
    index = len(init_pop)-1
    
    # randomly choose the parent chromosomes, which cannot be the same
    while index >= 0:
        copy1 = deepcopy(init_pop)
        chrom1 = copy1.pop(index)
        chrom2 = random.choice(copy1)
        
        # randomly choose the position to do crossover
        r = random.choice(list(range(len(chrom1))))
        
        # do crossvoer get the new child chromosome
        new_chrom = chrom1[:r]+chrom2[r:]
        
        # the child chromosome in next generation cannot be totally same
        if new_chrom in new_chroms:
            index = index
        else:
            new_chroms.append(new_chrom)
            index -= 1

    return new_chroms # get a new population


# define mutation: traverse all chromosomes, if the random generate number p is less than mutation probability, 
# then randomly choose a gene of current chromosomes, switch the gene to 1s if it's 0s originally or to 0s if it's
# 1s originally. 
def mutation(new_chroms, mutation_probability):
    new_pop = []
    
    for i in new_chroms:
        p = random.random()
        
        # if random probability r is less than the mutation_probability, chromosome i needs to do mutation
        if p < mutation_probability:
            
            # randomly choose a gene 
            r = random.choice(list(range(len(i))))
            
            # switch the gene
            change = 1 - int(i[r])
            
            # generate the new chromosome
            new_chrom2 = i[:r] + str(change) + i[r+1:]
            new_pop.append(new_chrom2)
        else:
            new_pop.append(i)
                
    #return the muatated new generation 
    return new_pop


# choose the best chromosome in the final generation
def best_chromosome(new_pop):
    max_imp = 0
        
    for i in new_pop:
        if max_imp < i[1][0]:
            max_imp = i[1][0]
            best_chrom = i[0]
            weight = i[1][1]
            
    best_chromosome = [best_chrom, [max_imp, weight]]
    return best_chromosome

    
# Print the solution.
def print_solution(best_chromosome):
    print('==================================================')
    print('The best chromosome is: %s' %best_chromosome[0])
    print('The total weight is: %d' %best_chromosome[1][1])
    print('The importance value for this solution is: %d' %best_chromosome[1][0])
    print('==================================================')    


    
    
if __name__ == '__main__':
    # iterate times
    n = 100  
    
    # generate the initial population
    population = init_population() 
   
    while n > 0:
        n -= 1
        
        # calculate the fitness  
        fitnesses = fitness(population)
        
        # judge if the iteration can be stopped 
        if is_best(fitnesses):
            break 
        
        # find the cull the 50% less important chromosomes 
        population = filter_cull(population, fitnesses)
        
        # do crossover to get new chromosomes
        population = crossover(population)
        
        # do mutation to get the next generation
        population = mutation(population, mutation_probability)       
    
    # calculate the fitness for the final generation
    fitnesses = fitness(population)
    
    # find the best chromosome which has the max importance value
    solution = best_chromosome(list(zip(population,fitnesses)))
    
    # print the result 
    print_solution(solution)
    

