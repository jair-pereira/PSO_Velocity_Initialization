import numpy as np
import cocoex
import sys, argparse, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solvers import pso
from src import *


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
    
    ## bbob validation suite ##
    suite = cocoex.Suite("bbob", "", "function_indices:2-7,9-12,14,16-19,21-24 dimensions:10 instance_indices:1-15")
    observer = cocoex.Observer("bbob", "result_folder: " + "PSO_"+str(args.m))
    #minimal_print = cocoex.utilities.MiniPrint()
    
    ## nfe ##
    nfe = 1e+7
    
    ## loop over problems ##
    for problem in suite:
        problem.observe_with(observer)
        sol = pso(args.m, args.n, problem, (problem.lower_bounds[0], problem.upper_bounds[0]), problem.dimension, nfe, args.w, args.c1, args.c2, *m[args.m])
        #minimal_print(problem, final=problem.index == len(suite) - 1)
    return 

if __name__ == "__main__":
   np.warnings.filterwarnings('ignore')
   main(sys.argv[1:])