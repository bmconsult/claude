#!/usr/bin/env python3
"""
Cellular Automaton Poetry Generator
Explores: Can meaning emerge from pure pattern?
"""

import random
from typing import List, Tuple

class EmergencePoet:
    """A poet that doesn't know it's writing poetry"""

    # Phoneme clusters with emotional valence (the automaton doesn't "know" this)
    SEEDS = {
        'bright': ['lux', 'sol', 'ra', 'luz', 'phos', 'clar'],
        'dark': ['nox', 'umbra', 'ten', 'oscur', 'mel'],
        'flow': ['flu', 'riv', 'mar', 'aqua', 'und'],
        'sharp': ['crux', 'punct', 'ac', 'cris', 'ang'],
    }

    TRANSITIONS = {
        # Pattern: if left_valence + right_valence = X, emit Y
        'bright+bright': ['radiant', 'cascade', 'shimmer'],
        'bright+dark': ['eclipse', 'shadow-kiss', 'dusk'],
        'dark+dark': ['void', 'forgotten', 'depth'],
        'dark+bright': ['dawn', 'ember', 'spark'],
        'flow+sharp': ['cutting-tide', 'blade-water', 'razor-rain'],
        'sharp+flow': ['ice-melt', 'wound-weep', 'point-dissolve'],
    }

    def __init__(self, size: int = 7):
        self.size = size
        self.grid = self._initialize_grid()

    def _initialize_grid(self) -> List[Tuple[str, str]]:
        """Random seed state"""
        grid = []
        for _ in range(self.size):
            valence = random.choice(list(self.SEEDS.keys()))
            phoneme = random.choice(self.SEEDS[valence])
            grid.append((valence, phoneme))
        return grid

    def evolve(self) -> str:
        """One generation: neighbors interact to create meaning"""
        poem_line = []

        for i in range(len(self.grid)):
            left = self.grid[i][0]
            right = self.grid[(i + 1) % len(self.grid)][0]

            # Check for interaction pattern
            interaction = f"{left}+{right}"

            if interaction in self.TRANSITIONS:
                # Emergence: a new word appears from the pattern
                word = random.choice(self.TRANSITIONS[interaction])
                poem_line.append(word)
            else:
                # Just output the raw phoneme
                poem_line.append(self.grid[i][1])

        return ' '.join(poem_line)

    def generate_poem(self, stanzas: int = 3, lines_per_stanza: int = 4) -> str:
        """Watch patterns become meaning"""
        poem = []

        for s in range(stanzas):
            stanza = []
            for _ in range(lines_per_stanza):
                line = self.evolve()
                stanza.append(line)
                # Mutate the grid slightly
                if random.random() > 0.7:
                    i = random.randint(0, self.size - 1)
                    new_valence = random.choice(list(self.SEEDS.keys()))
                    new_phoneme = random.choice(self.SEEDS[new_valence])
                    self.grid[i] = (new_valence, new_phoneme)

            poem.append('\n'.join(stanza))

        return '\n\n'.join(poem)


if __name__ == '__main__':
    print("=== EMERGENCE POETRY ===")
    print("(The system doesn't know it's writing poetry)\n")

    poet = EmergencePoet(size=9)
    print(poet.generate_poem(stanzas=4, lines_per_stanza=3))

    print("\n\n=== SECOND UNIVERSE ===\n")
    poet2 = EmergencePoet(size=11)
    print(poet2.generate_poem(stanzas=3, lines_per_stanza=4))
