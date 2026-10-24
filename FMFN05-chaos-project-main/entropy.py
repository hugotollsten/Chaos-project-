from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor
from collections import Counter
import math
import matplotlib.pyplot as plt



class Entropy:
    def __init__(self, bits):
        self.bits = bits

    @staticmethod
    def H(p):
        if p == 0.0:
            return 0.0

        return -p * math.log2(p)


    def shannon_entropy(self):
        number_of_bits = len(self.bits)

        if number_of_bits == 0:
            return 0.0

        ones = sum(self.bits)
        p_ones = ones / number_of_bits
        p_zeros = 1.0 - p_ones

        if p_zeros == 0.0 or p_ones == 0.0:
            return 0.0

        return self.H(p_zeros) + self.H(p_ones)

    def entropy_rate(self, k):
        def block_entropy(k):
            number_of_blocks = len(self.bits) - k + 1

            if number_of_blocks <= 0:
                return 0.0

            counts = Counter(
                tuple(self.bits[i:i + k])
                for i in range(number_of_blocks)
            )

            entropy = 0.0

            for count in counts.values():
                p = count / number_of_blocks
                entropy += self.H(p)

            return entropy

        if k == 1:
            return block_entropy(1)

        return block_entropy(k) - block_entropy(k - 1)


MEGABITS = 1000000




chaotic = ChaoticShuffle(0.42, 0.01)
extractor = BitExtractor(chaotic)

bits_ = [
    extractor.next_bit()
    for _ in range(10 * MEGABITS)
]

entropy_raw = Entropy(bits_)

raw_rates = []

for k in range(1, 17):
    rate = entropy_raw.entropy_rate(k)
    raw_rates.append(rate)
    print(k, rate)


chaotic_vn = ChaoticShuffle(0.42, 0.01)
extractor_vn = BitExtractor(chaotic_vn)

von_neumann_bits = [
    extractor_vn.next_von_neumann_bit()
    for _ in range(10 * MEGABITS)
]

entropy_vn = Entropy(von_neumann_bits)

vn_rates = []

for k in range(1, 17):
    rate = entropy_vn.entropy_rate(k)
    vn_rates.append(rate)
    print(k, rate)




k_values = range(1, 17)

plt.figure(figsize=(9, 6))

plt.plot(
    k_values,
    raw_rates,
    marker="o",
    label="Raw chaotic bits"
)

plt.plot(
    k_values,
    vn_rates,
    marker="o",
    label="Von Neumann bits"
)

plt.xlabel("Block length $k$")
plt.ylabel("Estimated entropy rate $h_k$")

plt.xticks(range(1, 17))

plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig(
    "data/test_results/entropy_rate_comparison.png",
    dpi=300
)

plt.show()