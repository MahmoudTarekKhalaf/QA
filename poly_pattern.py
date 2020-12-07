#Trying to extract a pattern that gets repeated at least of length 5 bits.


import dimod 
from collections import defaultdict
from copy import deepcopy
import neal
from dimod.reference.samplers import ExactSolver
from dwave.system import EmbeddingComposite, DWaveSampler, LeapHybridSampler

given_pattern = [1,1,1,1,1,0,0,0,0,0,1,1,1,1,1]

#coefficients of satisfying terms
sample_length = 5
lamda = -500
penalty = 5

Q = {}

# Encoding the bqm by checking whether 5 consecutive qubist are repeated.
for i in range(0,len(given_pattern)-2*sample_length):
    for j in range(i+sample_length,len(given_pattern)-sample_length+1):
        factor = 0
        power = 0
        for k in range(i,i+sample_length):
            factor+= 2**power * given_pattern[k]
            power+=1
            
        power = 0
        for k in range(j,j+sample_length):
            factor-= 2**power * given_pattern[k]
            power+=1

        if factor == 0: 
            if (i,i+1,i+2,i+3,i+4) in Q:
                Q[(i,i+1,i+2,i+3,i+4)] += lamda
            else:
                Q[(i,i+1,i+2,i+3,i+4)] = lamda
        else:
            if (i,i+1,i+2,i+3,i+4) in Q:
                Q[(i,i+1,i+2,i+3,i+4)] += penalty
            else:
                Q[(i,i+1,i+2,i+3,i+4)] = penalty

# Send to the poly solver            
sampler = dimod.HigherOrderComposite(neal.SimulatedAnnealingSampler())
sampleset = sampler.sample_hubo(Q,num_reads=10)

smpl = sampleset.first.sample
print(smpl)