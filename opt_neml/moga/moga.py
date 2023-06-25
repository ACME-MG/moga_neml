"""
 Title:         Multi-Objective Genetic Algorithm
 Description:   For parameter optimisation
 Author:        Janzen Choi

"""

# Libraries
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.sampling.lhs import LHS
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.optimize import minimize
from opt_neml.moga.problem import Problem

# The Multi-Objective Genetic Algorithm (MOGA) class
class MOGA:
    
    # Constructor
    def __init__(self, problem:Problem, num_gens:int, init_pop:int, offspring:int, crossover:float, mutation:float):
        
        # Initialise
        self.problem    = problem
        self.num_gens   = num_gens
        self.init_pop   = init_pop
        self.offspring  = offspring
        self.crossover  = crossover
        self.mutation   = mutation

        # Define algorithm
        self.algo = NSGA2(
            pop_size     = init_pop,
            n_offsprings = offspring,
            sampling     = LHS(),                               # latin hypercube sampling
            crossover    = SBX(prob=crossover, prob_var=1.0),   # simulated binary crossover 
            mutation     = PolynomialMutation(prob=mutation),   # polynomial mutation
            eliminate_duplicates = True
        )

    # Runs the genetic optimisation
    def optimise(self) -> None:
        minimize(self.problem, self.algo, ("n_gen", self.num_gens), verbose=False, seed=None)