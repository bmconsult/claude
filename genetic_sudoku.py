#!/usr/bin/env python3
"""
Solving Sudoku through EVOLUTION instead of logic
This is deliberately inefficient but conceptually interesting
"""

import random
import copy

class SudokuOrganism:
    """A Sudoku board is an organism. Fitness = how valid it is."""

    def __init__(self, puzzle):
        """puzzle: 9x9 grid with 0 for empty cells"""
        self.puzzle = copy.deepcopy(puzzle)
        self.fixed = [[puzzle[i][j] != 0 for j in range(9)] for i in range(9)]

        # Fill empty cells randomly (our initial "random mutation")
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    self.puzzle[i][j] = random.randint(1, 9)

    def fitness(self):
        """Fitness = number of constraint violations (lower is better)"""
        violations = 0

        # Check rows
        for row in self.puzzle:
            violations += 9 - len(set(row))

        # Check columns
        for col in range(9):
            column = [self.puzzle[row][col] for row in range(9)]
            violations += 9 - len(set(column))

        # Check 3x3 boxes
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(self.puzzle[box_row*3+i][box_col*3+j])
                violations += 9 - len(set(box))

        return -violations  # Negative because higher fitness is better

    def mutate(self):
        """Random mutation: change one non-fixed cell"""
        # Find a non-fixed cell
        attempts = 0
        while attempts < 100:
            i, j = random.randint(0, 8), random.randint(0, 8)
            if not self.fixed[i][j]:
                self.puzzle[i][j] = random.randint(1, 9)
                return
            attempts += 1

    def crossover(self, other):
        """Sexual reproduction: mix two solutions"""
        child = SudokuOrganism([[0]*9 for _ in range(9)])
        child.fixed = copy.deepcopy(self.fixed)

        for i in range(9):
            for j in range(9):
                # Randomly inherit from parent1 or parent2
                child.puzzle[i][j] = self.puzzle[i][j] if random.random() < 0.5 else other.puzzle[i][j]
                # But keep fixed cells fixed
                if self.fixed[i][j]:
                    child.puzzle[i][j] = self.puzzle[i][j]

        return child

    def is_solved(self):
        return self.fitness() == 0

    def display(self):
        for i, row in enumerate(self.puzzle):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(f"{val} ", end="")
            print()


def evolve_solution(puzzle, population_size=100, generations=1000):
    """Evolve a population of sudoku boards toward a solution"""

    # Create initial population
    population = [SudokuOrganism(puzzle) for _ in range(population_size)]

    print(f"Generation 0: Best fitness = {max(p.fitness() for p in population)}")

    for gen in range(generations):
        # Evaluate fitness
        population.sort(key=lambda x: x.fitness(), reverse=True)

        # Check if solved
        if population[0].is_solved():
            print(f"\n🧬 EVOLUTION SUCCESSFUL at generation {gen}!")
            return population[0]

        # Selection: keep top 20%
        survivors = population[:population_size // 5]

        # Create next generation
        next_gen = survivors.copy()

        while len(next_gen) < population_size:
            # Crossover: combine two random survivors
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            child = parent1.crossover(parent2)

            # Mutation: 30% chance
            if random.random() < 0.3:
                child.mutate()

            next_gen.append(child)

        population = next_gen

        # Report progress
        if gen % 100 == 0 or gen < 10:
            print(f"Generation {gen}: Best fitness = {population[0].fitness()}")

    print("\n⚠️  Did not fully solve, but here's the best attempt:")
    return population[0]


if __name__ == '__main__':
    # Easy Sudoku puzzle
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("🧬 GENETIC SUDOKU SOLVER")
    print("Using evolution instead of logic!\n")
    print("Initial puzzle:")
    temp = SudokuOrganism(puzzle)
    # Show original
    for i, row in enumerate(puzzle):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(f"{val if val != 0 else '.'} ", end="")
        print()

    print("\n" + "="*40)
    print("BEGINNING EVOLUTION...")
    print("="*40 + "\n")

    solution = evolve_solution(puzzle, population_size=200, generations=500)

    print("\nFinal result:")
    solution.display()
    print(f"\nFitness: {solution.fitness()} (0 = perfect)")
