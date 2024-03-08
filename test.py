from biased_walker import BiasedWalker
import numpy as np


walker = BiasedWalker(False, "R")

summ = 0

for i in range(100):
    for j in range(100):
        walker.move()

    summ += np.linalg.norm(walker.get_location())
    walker.reset()

print(summ / 100)
