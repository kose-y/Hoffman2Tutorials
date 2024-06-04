import sys
import os
import numpy as np

# number of samples per repeat
n = int(sys.argv[1])
# number of repetition
reps = int(sys.argv[2])

# seed
seed = int(sys.argv[3])

# create folder if it does not exist
path = "simresults/"
if not os.path.exists(path):
    os.makedirs(path)

oFile = f"simresults/n_{n}_reps_{reps}_seed_{seed}.txt"

# Simulate `reps` replicates of sample size `n` from distribution `d` using seed `seed`

np.random.seed(seed)
simres = np.zeros((reps, 2))
for r in range(reps):
    x = np.random.randn(n)
    simres[r, 0] = np.mean(x)
    simres[r, 1] = np.std(x)

np.savetxt(oFile, simres, delimiter=",")
