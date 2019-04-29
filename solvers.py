from src import *

def pso(n, my_func, bounds, dimension, max_nfe, w, c1, c2):
    Solution.setProblem(my_func, bounds, dimension, maximize=False)
    Solution.repair = op.repair_random
    X = Solution.initialize(n)
    [Xi.setX(op.init_random(*Solution.bounds, Solution.dimension)) for Xi in X]
    [Xi.getFitness() for Xi in X]
    
    while Solution.nfe < max_nfe:
        #Round 1
        S  = op.select_current(X)
        U  = op.w_pso(S, w, c1, c2)
        X  = U
        
        [Xi.getFitness() for Xi in X]
    return Solution