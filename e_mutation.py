import random

def swap_mutation(chromosome: list[int], prob: float = 0.1) -> list[int]:
    if random.random() > prob:
        return chromosome[:]  # sem mutação

    i, j = random.sample(range(len(chromosome)), 2)

    mutant = chromosome[:]
    mutant[i], mutant[j] = mutant[j], mutant[i]

    return mutant

def relocate_mutation(chromosome: list[int], prob: float = 0.1) -> list[int]:
    if random.random() > prob:
        return chromosome[:]

    mutant = chromosome[:]

    i, j = random.sample(range(len(mutant)), 2)

    gene = mutant.pop(i)
    mutant.insert(j, gene)

    return mutant

def light_mutation(chromosome: list[int], prob: float = 0.15) -> list[int]:
    if random.random() > prob:
        return chromosome[:]

    if random.random() < 0.5:
        return swap_mutation(chromosome, prob=1.0)
    else:
        return relocate_mutation(chromosome, prob=1.0)
