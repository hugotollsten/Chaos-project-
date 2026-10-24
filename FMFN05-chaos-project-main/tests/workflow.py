from pathlib import Path

import numpy as np

from chaoticrand import ChaoticShuffle
from bit_extractor import BitExtractor


EPSILON = 0.001
SEED = 0.42
MEGABITS = 1_000_000
GIGABITS = 1_000_000_000

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

def save_bits_as_bin(bits, filename):
    bits = np.asarray(bits, dtype=np.uint8)

    packed = np.packbits(bits)

    output_path = DATA_DIR / filename
    packed.tofile(output_path)

    print(f"Saved {len(bits):,} bits")
    print(f"Saved {len(packed):,} bytes")
    print(f"File: {output_path}")


chaotic = ChaoticShuffle(SEED, EPSILON)
extractor = BitExtractor(chaotic)

bits = [
    extractor.next_bit()
    for _ in range(GIGABITS)
]

save_bits_as_bin(
    bits,
    "chaotic_bits_GB.bin",
)

chaotic_vn = ChaoticShuffle(SEED, EPSILON)
extractor_vn = BitExtractor(chaotic_vn)

von_neumann_bits = [
    extractor_vn.next_von_neumann_bit()
    for _ in range(GIGABITS)
]

save_bits_as_bin(
    von_neumann_bits,
    "chaotic_von_neumann_GB.bin",
)

