import numpy as np
from .solution import *

### INITIALIZATION METHODS ###
def init_random(lb, ub, dimension):
    return np.random.uniform(lb, ub, dimension)
    
def init_zero(lb, ub, dimension):
    return np.zeros(dimension)

def init_small_random(x, f, dimension):
    return np.random.uniform(-f, +f, dimension)

#velocity initialization
def initv_half_dif(x, lb, ub, dimension):
    return (np.random.uniform(lb, ub, dimension) - x)/2
    
### SELECTION METHODS (INPUT) ###
def select_current(X):
    ''' Selects all candidate solutions from X
    :param X: list of candidate solutions
    :returns: A list of references of the selected candidate solutions. '''
    S = [[Xi] for Xi in X]
    return np.array(S)

### OPERATORS ###  
# PSO OPERATOR
#wrapper
def w_pso(S, w, c1, c2):
    ''' 
    PSO operator Wrapper
    :param S: list of selected candidate solutions
    :param w: (inertia) velocity modifier, real value
    :param c1: (cognitive) pbest modifier, real value
    :param c2: (social) gbest modifier, real value
    :returns: list of candidate solutions
    '''
    U = Solution.initialize(len(S))
    v = np.array([pso_velocity(Xi.x, Xi.velocity, type(Xi).best.x, Xi.pbest['x'], w, c1, c2) for Xi in S[:,0]])
    u = np.array([pso_move(S[i,0].x, v[i]) for i in range(len(S))])
    
    for i in range(len(U)): 
        U[i].setX(u[i])
        U[i].setVelocity(v[i])
        U[i].pbest = S[i,0].pbest
    
    return U

#base
def pso_velocity(x, v, gbest, pbest, w, c1, c2):
    ''' 
    Computes the new velocity of 'x'
    :param x: np.array of real values
    :param v: np.array of real values
    :param gbest: np.array of real values
    :param pbest: np.array of real values
    :param w: (inertia) velocity modifier, real value
    :param c1: (cognitive) pbest modifier, real value
    :param c2: (social) gbest modifier, real value
    :returns: np.array of real values
    '''
    r1 = np.random.random(len(x))
    r2 = np.random.random(len(x))
    
    v = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x)
    return v
    
def pso_move(x, v):
    ''' 
    Computes the new position of 'x'
    :param x: np.array of real values
    :param v: np.array of real values
    :returns: np.array of real values
    '''
    u = x + v
    return u
    
### REPAIR OPERATOR ###
def repair_truncate(x, lb, ub):
    '''
    Replaces the values in 'x' higher than 'ub' and lower than 'lb' by 'ub' and 'lb', respectively
    :param x: np.array of real values
    :param lb: lower bound
    :param ub: upper bound
    :returns: np.array of real values
    '''
    u = np.clip(x, lb, ub)
    return u
    
def repair_random(x, lb, ub):
    '''
    Replaces the values in 'x' higher than 'ub' and lower than 'lb' by a random value between lb and ub
    :param x: np.array of real values
    :param lb: lower bound
    :param ub: upper bound
    :returns: np.array of real values
    '''
    u = np.array([xi for xi in x])
    
    mask = (u<lb) + (u>ub)
    u[mask] = np.random.uniform(lb, ub, len(u[mask]))
    return u
   
#repair velocity
def repair_v_zero(v, x, x1, lb, ub):
    u = np.array([xi for xi in x])
    mask = (u<lb) + (u>ub)
    
    w = np.array([vi for vi in v])
    w[mask] = 0

    return w
    
def repair_v_diff(v, x, x1, lb, ub):
    return x1-x