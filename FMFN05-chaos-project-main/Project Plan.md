## Idea
Chaos as a noise amplifier. Simulate the logistic map with additive noise of size ε, or a noisy Lorenz flow, and sample one bit at intervals comparable to the Lyapunov time. A perturbation of size ε grows to the size of the attractor in about ln(1/ε)/λ, and after that the bit is no longer determined by the past. Measure the entropy of the bits conditioned on the previous ones as a function of the sampling interval and of ε, and check whether the entropy rate approaches λ. Post-process with the von Neumann extractor (01 and 10 give a bit, 00 and 11 are discarded) and compare the rate with the chaotic lasers of Uchida et al. (2008).

* Start with Logistic map, with $r=4$ and $r<4$ with noise $\varepsilon$ (check in Uchida et al. (2008) for size of $\varepsilon$)
* Experimentally determine $\lambda$ of the Logistic map to look at Lyapunov time $\frac{1}{\underset{ i }{ \text{max} }(\lambda_{i})}$
* Find entropy rate in Uchida et al. (2008)
* Convert output to bits and use von Neumann extractor
* Bit is 1 if $x>1 /2$ and 0 $x< 1/2$, skip if $x=1/2$
* Stick to the Mbit range
* Plot distribution (histogram)
* Test against statistical tests for randomness
* Measure entropy of the bits conditioned on the previous ones as function of $\varepsilon$ (and sampling interval)
* Try $10^{-3}<\varepsilon< 10^{-2}$
* Check that fraction of ones is $1 /2\pm \frac{1}{2\sqrt{ n }}$ for $n$ generated bits
* Check that Shannon entropy of $k$-bit words approach $k$ bits, and that the difference of consecutive block entropies estimates the entropy rate (compare with $\lambda /\ln 2$)
* Check that $\lvert C(\tau) \rvert$ (autocorrelation) is of order $1 /\sqrt{ n }$ for $\tau\neq 0$ and that the spectrum is flat
## TODO
1) Read background theory on:
	1) Shannon entropy (Hien)
	2) Lyapunov time/exponent (Sofie)
	3) Logistic map (All)
	4) Chaotic laser (Hugo)
	5) Random number generation (Hien)
	6) (von Neumann extractor)
	7) Randomness tests/benchmarks (Hien)
	8) Entropy rate (Hien)
	9) Auto correlation of numbers?? (Sofie & Hugo)
2) Code/find:
	1) Bit extractor (own implementation)
	2) Lyapunov estimate
	3) Randomness tests (library??)
	4) Entropy rate (library)
	5) Check fraction of ones in generated bits
	6) Auto correlation and spectrum (library??)
	7) Shannon entropy checker (in block) (library)




Möte 2 8/10:
Plan till nästa möte den 15 /10 
- Bakgrundsteori till stort sett klart
Map och koppling till brus: Hugo
Kort inslag om kaotisk laser: Hugo
Autokorrelation: Sofia
Lyapunov exponent: Sofia
Entropi: Hien
Tester för kontroll av random: Hien




- Påbö
