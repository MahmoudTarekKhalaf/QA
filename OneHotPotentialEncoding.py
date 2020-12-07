# Encoding a potential on D-Wave quantum computer.
# The method is proposed by the paper named "Quantum Computing for Quantum Tunnelling".
# The purpose of this file is just practicing and no violation of copywrites is committed.

from dwave.system import LeapHybridSampler
from dwave.system import DWaveSampler,EmbeddingComposite
from dimod import BinaryQuadraticModel
from collections import defaultdict
from copy import deepcopy
import neal
import dimod

big_num = 50
num_x = 5
x_upper = 10
delta_x = 2*x_upper/(num_x-1)
num_psi = 5
delta_psi = 1/(num_psi-1)
m = 1; h_par = 1
lamda_chain = 50000

# Encode indices.
def get_index(x_ind,psi_ind):
    return x_ind *big_num  + psi_ind

# Get x and phi indices' values by the index.
def get_x_and_phi_index(index):
    x_ind, psi_ind = divmod(index, big_num)
    return x_ind, psi_ind
# Get x and phi values by the index.
def get_x_and_psi_value(index):
    x_ind, psi_ind = get_x_and_phi_index(index)
    x = -x_upper+delta_x*x_ind
    psi = psi_ind*delta_psi
    return x, psi


h={}
J = {}

#setting the chain
for x in range(num_x):
    index1 = get_index(x,0)
    index2 = get_index(x,num_psi-1)
    if (index1) in h:
        h[index1] = h[index1]-lamda_chain
    else:
        h[index1] = -lamda_chain
    if (index2) in h:
        h[index2] = h[index2]+lamda_chain
    else:
        h[index2] = lamda_chain
    for psi in range(num_psi-1):
        index1 = get_index(x,psi)
        index2 = get_index(x,psi+1)
        if ((index1,index2)) in J:
            J[(index1,index2)] = h[index1]-lamda_chain
        else:
            J[(index1,index2)] = -lamda_chain

#add the potential part:
for x in range(num_x):
    for psi in range(num_psi-1):
        index = get_index(x,psi)
        x_val, psi_val = get_x_and_psi_value(index)
        potential = 0.5 * m * x_val**2
        if (index) in h:
            h[index] = h[index]+potential*psi
        else:
            h[index] = potential*psi


#solve by D-Wave
bqm = BinaryQuadraticModel.from_ising(h,J)
sampler = LeapHybridSampler()
sampler = neal.SimulatedAnnealingSampler()
sampler = dimod.ExactSolver()
results = sampler.sample(bqm)
# Get the results
smpl = results.first.sample

print(smpl)