from src import *
def pso(exp_name, n, my_func, bounds, dimension, max_nfe, w, c1, c2, repair_x, repair_v, init_v):
    ## log init ##
    log = Log("PSO_"+exp_name)
    
    ## set problem ##
    Solution.setProblem(my_func, bounds, dimension, maximize=False)
    Solution.other_stop_condition = my_func.final_target_hit
    
    ## set repair methods ##
    Solution.repair_x = repair_x
    Solution.repair_v = repair_v
    
    ## initialize position ##
    X = Solution.initialize(n)
    [Xi.setX(op.init_random(*Solution.bounds, Solution.dimension)) for Xi in X]
    ## initialize velocity ##
    [Xi.setVelocity(init_v(Xi.x, *Solution.bounds, Solution.dimension)) for Xi in X]
    ## evaluate ##
    [Xi.getFitness() for Xi in X]
    
    ## log write##
    log([Solution.nfe, Solution.count_repair, Solution.best.getFitness()])
    
    while Solution.nfe < max_nfe or Solution.other_stop_condition:
        ## update velocity ##
        [Xi.setVelocity(op.pso_velocity(Xi.x, Xi.velocity, Solution.best.x, Xi.pbest['x'], w, c1, c2))  for Xi in X]
        ## update position ##
        [Xi.setX(op.pso_move(Xi.x, Xi.velocity))  for Xi in X]
        ## evaluate ##
        [Xi.getFitness() for Xi in X]
        
        ## log write ##
        log([Solution.nfe, Solution.count_repair, Solution.best.getFitness()])
    
    ## log close##
    log.close()
    return Solution