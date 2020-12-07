#Trying to extract a pattern that gets repeated at least of length 3 bits.

from dimod import BinaryQuadraticModel
from collections import defaultdict
from copy import deepcopy
import neal
from dimod.reference.samplers import ExactSolver
from dwave.system import EmbeddingComposite, DWaveSampler, LeapHybridSampler



given_pattern = [1,1,1,1,0,0,0,1,0,1,1,1,1]

# Coefficients of satisfying terms
sample_length = 4
lamda = -500
penalty = 2

J = defaultdict(int)

# Encoding the bqm by checking whether 3 consecutive qubist are repeated.
add_var_num = len(given_pattern)
for i in range(0,len(given_pattern)-2):
   for j in range(i+sample_length,len(given_pattern)-sample_length+1):
      factor = given_pattern[i]+3*given_pattern[i+1]+5*given_pattern[i+2]+7*given_pattern[i+3]-given_pattern[j]-3*given_pattern[j+1]-5*given_pattern[j+2]-7*given_pattern[j+3]
      if factor == 0:
         J[i, add_var_num] += lamda
         J[i+1, add_var_num] += lamda
         J[i+2, add_var_num] += lamda
         J[i+3, add_var_num] += lamda
         J[add_var_num, add_var_num] += -2*lamda
      else:
         J[i, add_var_num] += -2*penalty
         J[i+1, add_var_num] += -2*penalty
         J[i+2, add_var_num] += -2*penalty
         J[i+3, add_var_num] += -2*penalty
         J[add_var_num, add_var_num] += 3*penalty
         J[i, i+1] += penalty
         J[i, i+2] += penalty
         J[i, i+3] += penalty
         J[i+1, i+2] += penalty
         J[i+1, i+3] += penalty
         J[i+2, i+3] += penalty
      add_var_num = add_var_num + 1
Q = deepcopy(J)

# Send to the solver and solve.
bqm = BinaryQuadraticModel.from_qubo(Q)
sampler = neal.SimulatedAnnealingSampler()
sampler = LeapHybridSampler()
results = sampler.sample(bqm)
smpl = results.first.sample
print(smpl)