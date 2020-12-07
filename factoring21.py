#factoring 21

from dwave.system import LeapHybridSampler
from dwave.system import DWaveSampler,EmbeddingComposite
from dimod import BinaryQuadraticModel
from collections import defaultdict
from copy import deepcopy
import neal

n = 21
while True:
#encoding the bqm for 21 which is got by mathematica file named "bqm".
    bqm = BinaryQuadraticModel({'p1': -76,'p2': 768,'q1': -76, 'q2':-144},{('p2', 'p1'): -512,('p1', 'q1'): 152,('p2', 'q1'): -512,('p1', 'q2'): -144,('p2', 'q2'): 128,('q1', 'q2'): 16},400,'BINARY')
#sending the bqm to the sampler. 
    sampler = neal.SimulatedAnnealingSampler()
    results = sampler.sample(bqm)
    energy = results.first.energy
    smpl = results.first.sample
    q1 = int(smpl['q1'])
    q2 = int(smpl['q2'])
    p1 = int(smpl['p1'])
    q = 1 + 2*q1 + 4*q2
    p = 1 + 2*p1
#Check the answer
    if n == q*p:
        break
    print(f'q is {q}, p is {p} which is not valid')

print(f'q is {q}, p is {p} which is valid')
