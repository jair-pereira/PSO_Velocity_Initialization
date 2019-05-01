import numpy as np
import cocoex
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers import pso
from src import *

### interface between the target-runner and the solvers for irace ###

def main(args):
    ## arguments ##
    parser = argparse.ArgumentParser()
    #parser.add_argument('--nfe'  , dest='nfe'  , type=float, help="Integer   : Number of Function Evaluations")
    parser.add_argument('--n'    , dest='n'    , type=float, help="Integer   : Population size")
    parser.add_argument('--w'    , dest='w'    , type=float, help="Real value: velocity modifier")
    parser.add_argument('--c1'   , dest='c1'   , type=float, help="Real value: pbest modifier")
    parser.add_argument('--c2'   , dest='c2'   , type=float, help="Real value: gbest modifier")
    parser.add_argument('--m'    , dest='m'    , type=int  , help="Real value: 1-8, specifying which PSO to run")
    #parser.add_argument('--bbob', dest='bbob'  , type=str  , help="String    : BBOB suite e.g.:function_indices:1 dimensions:2 instance_indices:1")
    args = parser.parse_args()
    
    ## repair and initialization types ##
    m = [0,
        (op.repair_truncate, op.repairv_zero, op.initv_half_dif),     #1
        (op.repair_random , op.repairv_diff  , op.initv_half_dif),    #2

        (op.repair_truncate, op.repairv_zero, op.initv_random),       #3
        (op.repair_random , op.repairv_diff  , op.initv_random),      #4

        (op.repair_truncate, op.repairv_zero, op.initv_zero),         #5
        (op.repair_random , op.repairv_diff  , op.initv_zero),        #6

        (op.repair_truncate, op.repairv_zero, op.initv_small_random), #7
        (op.repair_random , op.repairv_diff  , op.initv_small_random) #8
        ]
    
    ## bbob training suite ##
    suite = cocoex.Suite("bbob", "", "function_indices:1,8,13,15,20 dimensions:10 instance_indices:1-6")
    
    ## nfe ##
    nfe = 1e+0
    
    ## loop over problems ##
    fitness = 0
    for problem in suite:
        sol = pso(args.m, args.n, problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, nfe, args.w, args.c1, args.c2, *m)
        
        fitness += sol.best.getFitness()
    ## irace get information from standard output ##
    print(fitness)
    return 

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])