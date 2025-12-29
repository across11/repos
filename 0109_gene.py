import random
import string

# --- Configuration ---
TARGET_PHRASE = "To be, or not to be, that is the question."
POPULATION_SIZE = 500
MUTATION_RATE = 0.01
ELITISM_COUNT = 2 # Number of top individuals to carry over to the next generation

# --- Helper Functions ---
def create_random_gene():
    """Creates a single random character (gene)."""
    return random.choice(string.printable)

def create_random_chromosome():
    """Creates a random string (chromosome) of the same length as the target."""
    return ''.join(create_random_gene() for _ in range(len(TARGET_PHRASE)))

def calculate_fitness(chromosome):
    """Calculates the fitness score of a chromosome.
    Fitness is the number of characters that match the target phrase at the correct position.
    """
    score = sum(1 for i, char in enumerate(chromosome) if char == TARGET_PHRASE[i])
    return score

def crossover(parent1, parent2):
    """Performs single-point crossover to create a child."""
    crossover_point = random.randint(1, len(TARGET_PHRASE) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(chromosome):
    """Mutates a chromosome by changing some of its genes."""
    mutated_chromosome = list(chromosome)
    for i in range(len(mutated_chromosome)):
        if random.random() < MUTATION_RATE:
            mutated_chromosome[i] = create_random_gene()
    return ''.join(mutated_chromosome)

# --- Main Genetic Algorithm ---
def genetic_algorithm():
    """The main function to run the genetic algorithm."""
    # 1. Initialize Population
    population = [create_random_chromosome() for _ in range(POPULATION_SIZE)]
    generation = 0

    while True:
        # 2. Calculate Fitness for the entire population
        population_with_fitness = [(ind, calculate_fitness(ind)) for ind in population]
        
        # Sort population by fitness (highest first)
        population_with_fitness.sort(key=lambda x: x[1], reverse=True)
        
        best_individual, best_fitness = population_with_fitness[0]
        
        # 3. Check for termination condition
        print(f"Generation {generation:4d} | Best: '{best_individual}' | Fitness: {best_fitness}/{len(TARGET_PHRASE)}")
        
        if best_individual == TARGET_PHRASE:
            print("\nTarget phrase reached!")
            break

        # 4. Selection and Reproduction
        next_generation = []

        # Elitism: Carry over the best individuals directly to the next generation
        for i in range(ELITISM_COUNT):
            next_generation.append(population_with_fitness[i][0])

        # Create the rest of the new generation through crossover and mutation
        while len(next_generation) < POPULATION_SIZE:
            # Select two parents (using "roulette wheel" selection)
            total_fitness = sum(fit for ind, fit in population_with_fitness)
            # A small value to prevent division by zero if all fitness are 0
            if total_fitness == 0:
                total_fitness = 1 
            
            parent1 = random.choices(
                population_with_fitness,
                weights=[fit / total_fitness for ind, fit in population_with_fitness],
                k=1
            )[0][0]

            parent2 = random.choices(
                population_with_fitness,
                weights=[fit / total_fitness for ind, fit in population_with_fitness],
                k=1
            )[0][0]
            
            # Create a child through crossover and mutation
            child = mutate(crossover(parent1, parent2))
            next_generation.append(child)
        
        # 5. Replace the old population with the new one
        population = next_generation
        generation += 1

if __name__ == "__main__":
    genetic_algorithm()
