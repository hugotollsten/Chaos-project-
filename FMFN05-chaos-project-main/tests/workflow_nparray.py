import numpy as np

import sys
from pathlib import Path

# Add the project root to Python's import path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor
from stats_test import BasicStats

# 0.001 < epsilon < 0.01

SEED = 0.42
EPSILON = 0.001
MEGABITS = 1000000


chaotic_floats = ChaoticShuffle(
    seed=SEED,
    ep=EPSILON
)

floats = [
    chaotic_floats.next_chaotic_float()
    for _ in range(MEGABITS)
]

chaotic_bits = ChaoticShuffle(
    seed=SEED,
    ep=EPSILON
)

extractor = BitExtractor(
    chaotic_bits
)

# bits = [
#     extractor.next_bit()
#     for _ in range(10*MEGABITS)
# ]


# stats = BasicStats(
#     floats=floats,
#     bits=bits
# )

# ""

# stats.test_all(
#     logistic_map=True,
#     max_lags=10000
# )





von_neumann_bits = [
    extractor.next_von_neumann_bit()
    for _ in range(10*MEGABITS)
]



stats = BasicStats(
    floats=floats,
    bits=von_neumann_bits
)

stats.test_all(
    logistic_map=False,
    max_lags=10000
)
