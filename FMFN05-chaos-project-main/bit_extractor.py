class BitExtractor:
    def __init__(self, chaotic):
        self.chaotic = chaotic

    def next_bit(self):
        x = self.chaotic.next_chaotic_float()
        while x == 0.5:
            # skip the float that is exactly 0.5
            x = self.chaotic.next_chaotic_float()
        return 0 if x < 0.5 else 1

    def next_von_neumann_bit(self):
        # (01 and 10 give a bit, 00 and 11 are discarded)
        while True:
            bits = (self.next_bit(), self.next_bit())
            if bits == (0, 1):
                return 0
            elif bits == (1, 0):
                return 1


