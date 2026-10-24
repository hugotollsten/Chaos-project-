import numpy as np
import scipy.stats as stats
import scipy.signal as signal
from scipy.fft import fft
from statsmodels.sandbox.stats.runs import runstest_1samp
import matplotlib.pyplot as plt

class BasicStats:
    def __init__(self, floats, bits):
        self.floats = floats
        self.bits = bits

    def cross_corr(self, other_floats):
        corr_vals = signal.correlate(self.floats, other_floats) / len(self.floats)
        lags = signal.correlation_lags(len(self.floats), len(other_floats))

        return corr_vals, lags

    def auto_corr(self, max_lag=1000):
        data = self.floats

        rhat = np.asarray([
            np.corrcoef(data, data)[0,1] if lag == 0 else np.corrcoef(data[lag:], data[:-lag])[0,1] for lag in range(max_lag + 1)
        ])

        lags = np.arange(max_lag + 1)

        return rhat, lags

    def periodogram(self):
        data0 = self.floats - np.mean(self.floats)

        nfft = 2**26
        nbr_zeros = nfft - len(data0)

        zero_pad_data = np.concatenate((data0, np.zeros(nbr_zeros)))
        X = fft(zero_pad_data)
        N = len(zero_pad_data)

        Rhat = (X*np.conj(X)) / len(data0)
        f = np.arange(N) / N

        return Rhat, f

    def frac_ones(self):
        nbr_ones = sum(self.bits)
        frac_ones = nbr_ones / len(self.bits)

        tolerance = 1 / (2*np.sqrt(len(self.bits)))

        interval = np.array([1/2 - tolerance, 1/2 + tolerance])

        return frac_ones, interval

    
    def test_all(self, logistic_map=False, max_lags=1000):
        fig, axs = plt.subplots(2, 2, figsize=(16,16))

        fig.suptitle("Basic statistical tests", fontsize=20)

        # if logistic_map == True:
        #     x = np.linspace(1e-8,1-1e-8,1000) # Avoid 0 and 1 since the function is not defined there
        #     rho_x = 1 / (np.pi*np.sqrt(x*(1-x))) + 6630

        #     print(rho_x.shape)

        #     axs[0,0].hist(self.floats, bins=100, label="Counts")
        #     axs[0,0].plot(x, rho_x, label="Density function")
        #     axs[0,0].set_title("Histogram with density function", fontsize=14)
        #     axs[0,0].set_xlabel(r"x")
        #     axs[0,0].set_ylabel("Count")
        # else:
        #     axs[0,0].hist(self.floats, bins=100, label="Counts")
        #     axs[0,0].set_title("Histogram", fontsize=14)
        #     axs[0,0].set_xlabel(r"x")
        #     axs[0,0].set_ylabel("Count")

        axs[0,0].hist(self.floats, bins=100, label="Counts")
        axs[0,0].set_title("Histogram", fontsize=14)
        axs[0,0].set_xlabel(r"x")
        axs[0,0].set_ylabel("Count")

        Rhat, f = self.periodogram()
        axs[0,1].plot(f, 10*np.log10(Rhat))
        axs[0,1].set_title("Periodogram", fontsize=14)
        axs[0,1].set_xlabel("Frequency [Hz]")
        axs[0,1].set_ylabel("Power [dB]")
        axs[0,1].set_ylim(-100, 10)
        axs[0,1].set_xlim(0,0.5)

        rhat, lags = self.auto_corr(max_lags)

        axs[1,0].plot(lags, rhat)
        axs[1,0].set_title("Autocorrelation of values", fontsize=14)
        axs[1,0].set_xlabel(r"Lag $k$")
        axs[1,0].set_ylabel(r"Autocorrelation")    

        axs[1,1].plot(lags, rhat)
        axs[1,1].set_title("Autocorrelation of values", fontsize=14)
        axs[1,1].set_xlabel(r"Lag $k$")
        axs[1,1].set_ylabel(r"Autocorrelation")   
        axs[1,1].set_ylim(-15/np.sqrt(len(self.floats)), 15/np.sqrt(len(self.floats)))
        axs[1,1].axhline(1/np.sqrt(len(self.floats)), color="r", linestyle="--", label=r"$1/\sqrt{n}$")
        axs[1,1].axhline(-1/np.sqrt(len(self.floats)), color="r", linestyle="--")
        axs[1,1].axhline(10/np.sqrt(len(self.floats)), color="orange", linestyle="--", label=r"$10/\sqrt{n}$")
        axs[1,1].axhline(-10/np.sqrt(len(self.floats)), color="orange", linestyle="--")
        axs[1,1].legend()

        frac_ones, interval = self.frac_ones()

        print("----------------------------------------------------\n")

        print(f"The fraction of ones in the bitstring is {frac_ones}, and the tolated interval is [{interval[0]}, {interval[1]}]\n")

        print("----------------------------------------------------\n")

        plt.show()