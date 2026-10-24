import numpy as np

class ChaoticShuffle:
    def __init__(self, seed=0.99999, ep=0.01 ):
        if not (0 < seed < 1):
            raise ValueError("Seed must be between 0 and 1.")

        self.epsilon = ep
        self.x = seed
        self.warm_up(100)

    def next_chaotic_float(self):
        k = 4.0 #k > 3 for chaos!!!
        noise = np.random.normal(loc=0.0, scale=self.epsilon)
        self.x = k * self.x * (1.0 - self.x) + noise

        #print(self.x)
        # noise = some random uniform within range of (-epsilon, epsilon)

        self.x = min(max(self.x, 0.0), 1.0)
        
        return self.x

    def warm_up(self, steps):
        if steps == 0:
            return
        self.next_chaotic_float()
        self.warm_up(steps - 1)

    def pseudo_random_integer(self, minimum, maximum):
        #Converting the chaotic decimal into an integer.

        value = self.next_chaotic_float()
        span = maximum - minimum + 1
        result = minimum + int(value * span)

        return min(result, maximum)

    def shuffle(self, items):
        #help function
        self.shuffling(items, len(items) - 1)

    def shuffling(self, items, i):
        #Fisher-Yates shuffle.

        if i <= 0:
            return
        j = self.pseudo_random_integer(0, i)

        items[i], items[j] = items[j], items[i]
        self.shuffling(items, i - 1)