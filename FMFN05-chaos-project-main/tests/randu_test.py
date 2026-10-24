import numpy as np
import scipy.stats as stats
import scipy.signal as signal
from scipy.fft import fft
from statsmodels.sandbox.stats.runs import runstest_1samp
import matplotlib.pyplot as plt

from stats_test import BasicStats

def RandU(x): # standard choise of RANDU parameters, a = 65539, m = 2^(31)
    return ((65539 * x) % (2**31))

def generate_RandU(seed, nbr_vals):
    x0 = seed
    result = np.empty(nbr_vals)

    for i in range(nbr_vals):
        if i == 0:
            x_n1 = RandU(x0)
            result[i] = x_n1
            continue

        x_n1 = RandU(result[i-1]) # x_n is saved at position i-1
        result[i] = x_n1

    return result / (2**31) # Divide by 2**31 to get values [0,1)

vals = generate_RandU(31, 10000000)

bits = [1 if vals[i] > 1/2 else 0 for i in range(vals.size)]

stats = BasicStats(vals, bits)

stats.test_all(logistic_map=False, max_lags=10000)