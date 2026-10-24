import csv
import math
import sys
from pathlib import Path

import numpy as np


# ---------------------------------------------------------
# Import project code
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor


# ---------------------------------------------------------
# Experiment parameters
# ---------------------------------------------------------

SEED = 0.42
EPSILON = 0.001

MAX_ITERATIONS = 20
REALIZATIONS = 10_000

# Used only so the experiment can be reproduced.
NOISE_SEED = 12345


# ---------------------------------------------------------
# Output
# ---------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data" / "test_results"

OUTPUT_FILE = (
    DATA_DIR / "shannon_entropy_by_iteration.csv"
)


# ---------------------------------------------------------
# Shannon entropy
# ---------------------------------------------------------

def binary_shannon_entropy(p_one):
    """
    Shannon entropy of a binary random variable.

    p_one = P(B_N = 1)
    p_zero = P(B_N = 0)

    H(B_N) =
        -p_zero * log2(p_zero)
        -p_one  * log2(p_one)
    """

    p_zero = 1.0 - p_one

    entropy = 0.0

    if p_zero > 0.0:
        entropy -= p_zero * math.log2(p_zero)

    if p_one > 0.0:
        entropy -= p_one * math.log2(p_one)

    return entropy


# ---------------------------------------------------------
# Create generator for one realization
# ---------------------------------------------------------

def new_extractor(seed, epsilon, realization):
    """
    Create the existing chaotic generator and BitExtractor.

    ChaoticShuffle normally performs a 100-step warm-up when
    it is created. For this experiment we want N = 1 to mean
    the FIRST iteration starting from x_0.

    Therefore the state is reset to x_0 after construction.

    The random-number state is also reset after the warm-up,
    so the discarded warm-up noise does not affect the
    experiment.
    """

    chaotic = ChaoticShuffle(
        seed=seed,
        ep=epsilon,
    )

    # Undo the state change caused by the standard warm-up.
    chaotic.x = seed

    # Give each realization its own reproducible noise sequence.
    np.random.seed(NOISE_SEED + realization)

    return BitExtractor(chaotic)


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------

def estimate_entropy_by_iteration(
    seed=SEED,
    epsilon=EPSILON,
    max_iterations=MAX_ITERATIONS,
    realizations=REALIZATIONS,
):
    """
    Estimate H(B_N) for N = 1, ..., max_iterations.

    Every realization starts from exactly the same initial
    condition x_0.

    The only difference between realizations is the Gaussian
    noise.

    For every iteration N we estimate

        P(B_N = 0)
        P(B_N = 1)

    from all realizations and then calculate the Shannon
    entropy H(B_N).
    """

    ones_per_iteration = np.zeros(
        max_iterations,
        dtype=np.int64,
    )

    # -----------------------------------------------------
    # Generate many short independent realizations
    # -----------------------------------------------------

    for realization in range(realizations):

        extractor = new_extractor(
            seed=seed,
            epsilon=epsilon,
            realization=realization,
        )

        for index in range(max_iterations):

            bit = extractor.next_bit()

            ones_per_iteration[index] += bit

    # -----------------------------------------------------
    # Calculate probability distribution and entropy
    # -----------------------------------------------------

    results = []

    for index, number_of_ones in enumerate(
        ones_per_iteration
    ):

        iteration = index + 1

        p_one = (
            number_of_ones / realizations
        )

        p_zero = 1.0 - p_one

        entropy = binary_shannon_entropy(
            p_one
        )

        results.append(
            {
                "iteration": iteration,
                "p_zero": p_zero,
                "p_one": p_one,
                "shannon_entropy": entropy,
            }
        )

    return results


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

def save_results(
    results,
    output_file=OUTPUT_FILE,
):
    """
    Save P(B_N=0), P(B_N=1), and H(B_N)
    for every iteration.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "iteration",
                "p_zero",
                "p_one",
                "shannon_entropy",
            ],
        )

        writer.writeheader()

        writer.writerows(results)


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

def print_results(results):

    print(
        "N    P(B_N=0)    P(B_N=1)    H(B_N) [bit]"
    )

    print("-" * 50)

    for row in results:

        print(
            f"{row['iteration']:2d}   "
            f"{row['p_zero']:.6f}     "
            f"{row['p_one']:.6f}     "
            f"{row['shannon_entropy']:.6f}"
        )


# ---------------------------------------------------------
# Theory
# ---------------------------------------------------------

def theoretical_predictability_horizon(
    epsilon=EPSILON,
):
    """
    For the logistic map at r = 4:

        lambda = ln(2)

    and the theory gives

        N ~ ln(1/epsilon) / lambda
    """

    lyapunov_exponent = math.log(2.0)

    return (
        math.log(1.0 / epsilon)
        / lyapunov_exponent
    )


# ---------------------------------------------------------
# Run experiment
# ---------------------------------------------------------

def main():

    print(
        f"Initial state x_0: {SEED}"
    )

    print(
        f"Noise amplitude epsilon: {EPSILON}"
    )

    print(
        f"Number of realizations: {REALIZATIONS:,}"
    )

    print(
        f"Iterations per realization: {MAX_ITERATIONS}"
    )

    print()

    results = estimate_entropy_by_iteration()

    print_results(results)

    save_results(results)

    theoretical_n = (
        theoretical_predictability_horizon()
    )

    print()

    print(
        "Theoretical predictability horizon:"
    )

    print(
        f"N ≈ {theoretical_n:.2f}"
    )

    print()

    print(
        f"Results saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
