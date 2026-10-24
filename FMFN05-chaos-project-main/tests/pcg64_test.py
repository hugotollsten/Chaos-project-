import numpy as np
import scipy.stats as stats
import scipy.signal as signal
from scipy.fft import fft
from statsmodels.sandbox.stats.runs import runstest_1samp
import matplotlib.pyplot as plt

from stats_test import BasicStats

rng = np.random.default_rng(np.random.PCG64(seed=123))

random_vals = rng.uniform(low=0, high=1, size=10000000)

bits = [1 if random_vals[i] > 1/2 else 0 for i in range(random_vals.size)]

stats = BasicStats(random_vals, bits)

stats.test_all(logistic_map=False, max_lags=10000)