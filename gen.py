import numpy as np
import os
import random
from concurrent.futures import ThreadPoolExecutor

from genAiPlayer import *
from prints import *
from playstyles import playGenAIGenAI, playAIgenAI, playAIAI, playGenAIAI

def makeNameList():
    names_list = []
    with open('names.csv', 'r', encoding='utf-8') as file:
        for line in file:
            names_list.append(line.strip())
    return names_list

def create_population(population_size):
    return [genAiPlayer(f"GenAI{i+1}") for i in range(population_size)]



def select_parents(population, fitness_scores, num_parents):
    return [population[i] for i in np.argsort(fitness_scores)[-num_parents:]]

def crossover(parent1, parent2, names_list):
    child_weights = np.zeros_like(parent1.weights)
    for i in range(len(child_weights)):
        child_weights[i] = parent1.weights[i] if np.random.rand() < 0.5 else parent2.weights[i]
    return genAiPlayer(random.choice(names_list), child_weights)

def mutate(ai, base_mutation_rate=0.02, selective_rate=0.1, variance=1):
    # Determine the number of weights to mutate based on selective_rate
    total_weights = ai.weights.size
    num_mutations = random.randint(1, int(selective_rate * total_weights))
    mutation_indices = np.random.choice(range(total_weights), num_mutations, replace=False)

    # Create a mask for selective mutation
    mutation_mask = np.zeros(total_weights, dtype=bool)
    mutation_mask[mutation_indices] = True
    mutation_mask = mutation_mask.reshape(ai.weights.shape)

    # Generate mutations with varying magnitudes
    mutations = np.random.randn(*ai.weights.shape) * np.random.uniform(0, variance, ai.weights.shape)
    
    # Apply mutations selectively
    new_weights = np.where(mutation_mask, ai.weights + mutations * base_mutation_rate, ai.weights)

    # Log the mutation process
    if num_mutations > 0:
        print_colored(f"Mutation occurred on {num_mutations} weights", "red")

    return genAiPlayer(ai.name, new_weights)

def create_next_generation(parents, population_size, num_top_performers, top_parents_num=0.25, names_list=makeNameList()):
    next_generation = []
    
    # Sort parents by fitness and keep the top performers unchanged
    sorted_parents = sorted(parents, key=lambda x: x.fitness, reverse=True)
    next_generation.extend(sorted_parents[:num_top_performers])
    
    # Define the pool of top parents for crossover based on num_parents
    num_parents = max(int(0.5 * population_size), 2)  # Increase from 25% to 50%
    top_parents = sorted_parents[:num_parents]
    
    # Fill the rest of the next generation with children from crossover and mutation
    for i in range(population_size - num_top_performers):
        parent1, parent2 = np.random.choice(top_parents, 2, replace=False)
        child = crossover(parent1, parent2, names_list)
        if np.random.rand() < 0.1:
            child = mutate(child)
        next_generation.append(child)
    
    return next_generation

def save_population(population, name, directory="weights"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    weights = np.array([ai.weights for ai in population])
    names = np.array([ai.name for ai in population])
    np.savez(os.path.join(directory, f"{name}.npz"), weights=weights, names=names)
    
def load_population(name, directory="weights"):
    data = np.load(os.path.join(directory, f"{name}.npz"))
    weights = data["weights"]
    names = data["names"]
    population = [genAiPlayer(name, weights) for name, weights in zip(names, weights)]
    return population

def save_population_weights(population, directory="weights"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    for ai in population:
        np.save(os.path.join(directory, f"{ai.name}.npy"), ai.weights)

import numpy as np
from concurrent.futures import ThreadPoolExecutor

def evaluate_fitness(ai1, ai2, score_limit, iterations):
    games_against_opponent = int(iterations / 2)
    total_games = iterations

    wins_as_first_player_ai1 = playGenAIGenAI(score_limit, games_against_opponent, ai1, ai2)
    wins_as_second_player_ai1 = games_against_opponent - playGenAIGenAI(score_limit, games_against_opponent, ai2, ai1)
    total_wins_ai1 = wins_as_first_player_ai1 + wins_as_second_player_ai1

    wins_as_first_player_ai2 = playGenAIGenAI(score_limit, games_against_opponent, ai2, ai1)
    wins_as_second_player_ai2 = games_against_opponent - playGenAIGenAI(score_limit, games_against_opponent, ai1, ai2)
    total_wins_ai2 = wins_as_first_player_ai2 + wins_as_second_player_ai2

    fitness_ai1 = total_wins_ai1 / total_games if total_games > 0 else 0
    fitness_ai2 = total_wins_ai2 / total_games if total_games > 0 else 0

    return fitness_ai1, fitness_ai2

def evaluate_fitness_parallel(ai, opponents, score_limit, fitness_viability):
    fitness_ai = 0
    for opponent in opponents:
        fitness_ai1, fitness_opponent = evaluate_fitness(ai, opponent, score_limit, fitness_viability)
        fitness_ai += fitness_ai1
    return fitness_ai / len(opponents)

def training_loop(population, num_generations=200, score_limit=50, fitness_viability=2, population_size=2000, names_list=makeNameList(), starting_gen=0):
    if population is None:
        population = create_population(population_size)
    elif len(population) < population_size: 
        for i in range(population_size - len(population)):
            population.append(genAiPlayer(f"GenAI{i+1}"))
    elif len(population) > population_size:
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
        population = sorted_population[:population_size]
         
    num_top_performers = int(0.2 * population_size)  # Keep the top 20% of the population
    
    for generation in range(num_generations):
        print_colored(f"Generation {generation + starting_gen}", "magenta")
        
        with ThreadPoolExecutor() as executor:
            futures = []
            for ai in population:
                opponents = [opponent for opponent in population if opponent != ai]
                futures.append(executor.submit(evaluate_fitness_parallel, ai, opponents, score_limit, fitness_viability))
            
            for i, future in enumerate(futures):
                population[i].fitness = future.result()
                print_colored(f"Fitness of {population[i].name}: {population[i].fitness}", "cyan")
        
        print_colored("Best fitness scores:", "green")
        for ai in sorted(population, key=lambda x: x.fitness, reverse=True)[:num_top_performers]:
            print_colored(f"{ai.name}: {ai.fitness}", "green")
        
        parents = select_parents(population, [ai.fitness for ai in population], num_parents=max(int(0.5 * population_size), 2))
        if generation != num_generations - 1:  
            population = create_next_generation(parents, population_size, num_top_performers, top_parents_num=0.5, names_list=names_list)
        # save each generation
        save_population(population, f"population{population_size}_{generation + starting_gen}")
        
    population = sorted(population, key=lambda x: x.fitness, reverse=True)    
    return population


def load_GenAI(name):
    data = np.load(f"weights/{name}.npz")
    weights = data["weights"]
    name = data["name"]
    return genAiPlayer(name, weights)

def save_GenAI(ai, name, directory="weights"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    np.savez(os.path.join(directory, f"{name}.npz"), weights=ai.weights, name=ai.name)

def winrateVSRandom(ai, num_games):
    total_wins = 0
    num_games_halfed = num_games // 2
    for _ in range(num_games_halfed):
        if playGenAIAI(50, 1, ai, ("basic", "Titouan", "random")) == 1:
            total_wins += 1
        if playAIgenAI(50, 1, ("basic", "Titouan", "random"), ai) == 0:
            total_wins += 1
    return total_wins / num_games

def winrateVSHighestFirst(ai, num_games):
    total_wins = 0
    num_games_halfed = num_games // 2
    for _ in range(num_games_halfed):
        if playGenAIAI(50, 1, ai, ("basic", "Titouan", "highestFirst")) == 1:
            total_wins += 1
        if playAIgenAI(50, 1, ("basic", "Titouan", "highestFirst"), ai) == 0:
            total_wins += 1
    return total_wins / num_games

def GenAIvsGenAI(ai1, ai2, num_games):
    total_winsP1 = 0
    total_winsP2 = 0
    num_games_halfed = num_games // 2
    for _ in range(num_games_halfed):
        if playGenAIGenAI(50, 1, ai1, ai2) == 1:
            total_winsP1 += 1
        else:
            total_winsP2 += 1
        if playGenAIGenAI(50, 1, ai2, ai1) == 1:
            total_winsP2 += 1
        else:
            total_winsP1 += 1
    return total_winsP1/num_games, total_winsP2/num_games

def evaluate_population(populationWithGenerations, score_limit, fitness_viability):
    population = [ai[0] for ai in populationWithGenerations]
    generation = [ai[1] for ai in populationWithGenerations]
    fitness_scores = []
    for i in range(len(population)):
        print_colored(f"Evaluating {population[i].name} from {generation[i]}", "cyan")
        opponents = [opponent for opponent in population if opponent != population[i]]
        fitness_scores.append((evaluate_fitness_parallel(population[i], opponents, score_limit, fitness_viability), generation[i]))
        
    # Assuming fitness_scores is a list of tuples (score, generation, ai)
    fitness_scores = [(score, gen, ai) for (score, gen), ai in zip(fitness_scores, population)]
    print_colored("\nFitness scores:", "green")
    for score, gen, ai in fitness_scores:
        print_colored(f"{ai.name} from {gen}: {score}", "white")
        
### ---------------- MAIN ----------------

# population = None
population = load_population("population1000_34")

population = training_loop(population, num_generations=20, score_limit=50, fitness_viability=2, population_size=1000, starting_gen=35)







# winrate of the 10 best AI from each generation against random and highestFirst
# filenames = []
# while True:
#     try:
#         load_population(f"population1000_{len(filenames)}")
#         filenames.append(f"population1000_{len(filenames)}")
#     except FileNotFoundError:
#         break
    
    
# best_ais = []
# for filename in filenames:
#     population = load_population(filename)
#     for i in range (5):
#         best_ais.append((population[i],f"Generation {filename[-2]}{filename[-1]}"))
    
# evaluate_population(best_ais, 100, 2)


# print("VS RANDOM")
# for ai in best_ais:
#     print(f"{ai[0].name} ({ai[1]}) : {winrateVSRandom(ai[0], 1000)}")
    
# print("VS HIGHEST FIRST")
# for ai in best_ais:
#     print(f"{ai[0].name} ({ai[1]}) : {winrateVSHighestFirst(ai[0], 1000)}")
