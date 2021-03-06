# Knapsack Problem-using-Genetic-Algorithms

The Knapsack Problem, using Genetic Algorithms(GA)

How to run the program:

The main steps for the GA algorithm includes:

1. Generate the initial population as the first generation
2. Calculate the fitness for each chromosome
3. Based on their importance value, filter and cull the 50% less important chromosomes from the current generation
4. Using crossover and mutation to generate new generation
5. Repeat the step 2-4 until finding the best chromosomes or fitting the stop constrains

How to do crossover here:
Randomly choose two chromosomes in the current generation, randomly choose a position of those two chromosomes, then crossover their gene fragment to get child chromosomes, traverse all possible parent chromosomes to get child chromosome, and combine all child chromosome to get a new generation.

How to do mutation:
Traverse all chromosomes, if the random generate number p is less than mutation probability, then randomly choose a gene of current chromosomes, switch the gene to 1s if it's 0s originally or to 0s if it's 1s originally. 

Since the result of GA algorithm is very dependent on the choice of parameter values, in order to get the global optimized solution, I did lots of experiments. And finally found the parameter value combination and the global optimized solution whose importance value is 44.
